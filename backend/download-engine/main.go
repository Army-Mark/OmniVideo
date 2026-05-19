package main

import (
	"context"
	"fmt"
	"io"
	"net/http"
	"os"
	"path/filepath"
	"sync"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/google/uuid"
)

type DownloadTask struct {
	ID        string    `json:"id"`
	URL       string    `json:"url"`
	Status    string    `json:"status"`
	Progress  float64   `json:"progress"`
	Speed     string    `json:"speed"`
	SpeedRaw  float64   `json:"speed_raw"`
	FilePath  string    `json:"file_path"`
	FileSize  int64     `json:"file_size"`
	Error     string    `json:"error,omitempty"`
	CreatedAt time.Time `json:"created_at"`
	UpdatedAt time.Time `json:"updated_at"`
}

type DownloadRequest struct {
	URL      string `json:"url" binding:"required"`
	Filename string `json:"filename,omitempty"`
}

type DownloadManager struct {
	tasks    map[string]*DownloadTask
	ctxs     map[string]context.Context
	cancels  map[string]context.CancelFunc
	mu       sync.RWMutex
}

var dm = &DownloadManager{
	tasks:   make(map[string]*DownloadTask),
	ctxs:    make(map[string]context.Context),
	cancels: make(map[string]context.CancelFunc),
}

func main() {
	gin.SetMode(gin.ReleaseMode)
	r := gin.Default()

	r.GET("/health", func(c *gin.Context) {
		c.JSON(200, gin.H{"status": "healthy", "service": "download-engine"})
	})

	r.POST("/download", createDownload)
	r.GET("/download/:id", getDownloadStatus)
	r.POST("/download/:id/pause", pauseDownload)
	r.POST("/download/:id/resume", resumeDownload)
	r.DELETE("/download/:id", cancelDownload)
	r.GET("/downloads", listDownloads)

	r.Run(":8080")
}

func createDownload(c *gin.Context) {
	var req DownloadRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(400, gin.H{"error": err.Error()})
		return
	}

	taskID := uuid.New().String()
	ctx, cancel := context.WithCancel(context.Background())

	task := &DownloadTask{
		ID:        taskID,
		URL:       req.URL,
		Status:    "pending",
		Progress:  0,
		CreatedAt: time.Now(),
		UpdatedAt: time.Now(),
	}

	dm.mu.Lock()
	dm.tasks[taskID] = task
	dm.ctxs[taskID] = ctx
	dm.cancels[taskID] = cancel
	dm.mu.Unlock()

	go processDownload(task, req.Filename)

	c.JSON(200, gin.H{
		"code":    200,
		"message": "下载任务已创建",
		"data":    task,
	})
}

func getDownloadStatus(c *gin.Context) {
	id := c.Param("id")

	dm.mu.RLock()
	task, exists := dm.tasks[id]
	dm.mu.RUnlock()

	if !exists {
		c.JSON(404, gin.H{"error": "任务不存在"})
		return
	}

	c.JSON(200, gin.H{"code": 200, "data": task})
}

func pauseDownload(c *gin.Context) {
	id := c.Param("id")

	dm.mu.Lock()
	task, exists := dm.tasks[id]
	if exists {
		task.Status = "paused"
		task.UpdatedAt = time.Now()
	}
	dm.mu.Unlock()

	if !exists {
		c.JSON(404, gin.H{"error": "任务不存在"})
		return
	}

	c.JSON(200, gin.H{"code": 200, "message": "已暂停"})
}

func resumeDownload(c *gin.Context) {
	id := c.Param("id")

	dm.mu.Lock()
	task, exists := dm.tasks[id]
	if exists {
		task.Status = "downloading"
		task.UpdatedAt = time.Now()
	}
	dm.mu.Unlock()

	if !exists {
		c.JSON(404, gin.H{"error": "任务不存在"})
		return
	}

	c.JSON(200, gin.H{"code": 200, "message": "已继续"})
}

func cancelDownload(c *gin.Context) {
	id := c.Param("id")

	dm.mu.Lock()
	task, exists := dm.tasks[id]
	if exists {
		task.Status = "failed"
		task.Error = "用户取消"
		task.UpdatedAt = time.Now()
	}
	cancel, hasCancel := dm.cancels[id]
	dm.mu.Unlock()

	if !exists {
		c.JSON(404, gin.H{"error": "任务不存在"})
		return
	}

	if hasCancel {
		cancel()
	}

	c.JSON(200, gin.H{"code": 200, "message": "已取消"})
}

func listDownloads(c *gin.Context) {
	dm.mu.RLock()
	defer dm.mu.RUnlock()

	result := make([]*DownloadTask, 0, len(dm.tasks))
	for _, task := range dm.tasks {
		result = append(result, task)
	}

	c.JSON(200, gin.H{"code": 200, "data": result})
}

func processDownload(task *DownloadTask, filename string) {
	task.Status = "downloading"
	task.UpdatedAt = time.Now()

	downloadDir := "./downloads"
	os.MkdirAll(downloadDir, 0755)

	if filename == "" {
		filename = fmt.Sprintf("%s.mp4", task.ID[:8])
	}

	filePath := filepath.Join(downloadDir, filename)
	task.FilePath = filePath

	dm.mu.RLock()
	ctx := dm.ctxs[task.ID]
	dm.mu.RUnlock()

	req, err := http.NewRequestWithContext(ctx, "GET", task.URL, nil)
	if err != nil {
		task.Status = "failed"
		task.Error = err.Error()
		task.UpdatedAt = time.Now()
		return
	}

	req.Header.Set("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

	client := &http.Client{Timeout: 0}
	resp, err := client.Do(req)
	if err != nil {
		task.Status = "failed"
		task.Error = err.Error()
		task.UpdatedAt = time.Now()
		return
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		task.Status = "failed"
		task.Error = fmt.Sprintf("HTTP %d", resp.StatusCode)
		task.UpdatedAt = time.Now()
		return
	}

	file, err := os.Create(filePath)
	if err != nil {
		task.Status = "failed"
		task.Error = err.Error()
		task.UpdatedAt = time.Now()
		return
	}
	defer file.Close()

	task.FileSize = resp.ContentLength

	var written int64
	buf := make([]byte, 64*1024)
	lastUpdate := time.Now()
	lastWritten := int64(0)

	for {
		select {
		case <-ctx.Done():
			task.Status = "failed"
			task.Error = "用户取消"
			task.UpdatedAt = time.Now()
			return
		default:
		}

		dm.mu.RLock()
		currentTask := dm.tasks[task.ID]
		dm.mu.RUnlock()
		if currentTask != nil && currentTask.Status == "paused" {
			for {
				time.Sleep(500 * time.Millisecond)
				dm.mu.RLock()
				t := dm.tasks[task.ID]
				dm.mu.RUnlock()
				if t == nil || t.Status != "paused" {
					break
				}
				select {
				case <-ctx.Done():
					task.Status = "failed"
					task.Error = "用户取消"
					task.UpdatedAt = time.Now()
					return
				default:
				}
			}
		}

		n, err := resp.Body.Read(buf)
		if n > 0 {
			file.Write(buf[:n])
			written += int64(n)

			if task.FileSize > 0 {
				task.Progress = float64(written) / float64(task.FileSize) * 100
			}

			now := time.Now()
			if now.Sub(lastUpdate) > time.Second {
				elapsed := now.Sub(lastUpdate).Seconds()
				speed := float64(written-lastWritten) / elapsed
				task.SpeedRaw = speed
				task.Speed = formatSpeed(speed)
				task.UpdatedAt = now
				lastUpdate = now
				lastWritten = written
			}
		}

		if err == io.EOF {
			break
		}
		if err != nil {
			task.Status = "failed"
			task.Error = err.Error()
			task.UpdatedAt = time.Now()
			return
		}
	}

	task.Status = "completed"
	task.Progress = 100
	task.UpdatedAt = time.Now()
}

func formatSpeed(bytesPerSec float64) string {
	if bytesPerSec < 1024 {
		return fmt.Sprintf("%.1f B/s", bytesPerSec)
	} else if bytesPerSec < 1024*1024 {
		return fmt.Sprintf("%.1f KB/s", bytesPerSec/1024)
	} else if bytesPerSec < 1024*1024*1024 {
		return fmt.Sprintf("%.2f MB/s", bytesPerSec/1024/1024)
	}
	return fmt.Sprintf("%.2f GB/s", bytesPerSec/1024/1024/1024)
}
