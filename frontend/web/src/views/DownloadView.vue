<script setup lang="ts">
import { onMounted, onUnmounted, ref } from 'vue'
import { useVideoStore } from '@/stores/video'
import { ElMessage, ElMessageBox } from 'element-plus'

const videoStore = useVideoStore()
const refreshTimer = ref<number | null>(null)

onMounted(() => {
  videoStore.getDownloadList()
  refreshTimer.value = window.setInterval(() => {
    videoStore.getDownloadList()
  }, 3000)
})

onUnmounted(() => {
  if (refreshTimer.value) {
    clearInterval(refreshTimer.value)
  }
})

async function handlePause(taskId: string) {
  try {
    await videoStore.pauseDownload(taskId)
    ElMessage.success('已暂停')
  } catch {
    ElMessage.error('操作失败')
  }
}

async function handleResume(taskId: string) {
  try {
    await videoStore.resumeDownload(taskId)
    ElMessage.success('已继续')
  } catch {
    ElMessage.error('操作失败')
  }
}

async function handleCancel(taskId: string) {
  try {
    await ElMessageBox.confirm('确定要取消该下载任务吗？', '提示', {
      type: 'warning',
    })
    await videoStore.cancelDownload(taskId)
    ElMessage.success('已取消')
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error('操作失败')
    }
  }
}

function getStatusType(status: string): string {
  const map: Record<string, string> = {
    pending: 'warning',
    downloading: 'primary',
    paused: 'info',
    completed: 'success',
    failed: 'danger',
  }
  return map[status] || 'info'
}

function getStatusText(status: string): string {
  const map: Record<string, string> = {
    pending: '等待中',
    downloading: '下载中',
    paused: '已暂停',
    completed: '已完成',
    failed: '失败',
  }
  return map[status] || status
}

function formatFileSize(bytes?: number): string {
  if (!bytes) return '-'
  if (bytes < 1024) return bytes + ' B'
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
  if (bytes < 1024 * 1024 * 1024) return (bytes / 1024 / 1024).toFixed(2) + ' MB'
  return (bytes / 1024 / 1024 / 1024).toFixed(2) + ' GB'
}
</script>

<template>
  <div class="download-page">
    <div class="page-header">
      <h2>📥 下载中心</h2>
      <el-button @click="videoStore.getDownloadList()" circle>
        <el-icon><Refresh /></el-icon>
      </el-button>
    </div>

    <div v-if="videoStore.downloadTasks.length === 0" class="empty">
      <el-empty description="暂无下载任务">
        <el-button type="primary" @click="$router.push('/')">去解析视频</el-button>
      </el-empty>
    </div>

    <div v-else class="task-list">
      <el-card v-for="task in videoStore.downloadTasks" :key="task.task_id" class="task-card">
        <div class="task-header">
          <div class="task-title">
            <span class="task-id">#{{ task.task_id.slice(0, 8) }}</span>
            <el-tag :type="getStatusType(task.status)" size="small">
              {{ getStatusText(task.status) }}
            </el-tag>
          </div>
          <div class="task-actions">
            <el-button
              v-if="task.status === 'downloading'"
              size="small"
              @click="handlePause(task.task_id)"
            >
              <el-icon><VideoPause /></el-icon>
              暂停
            </el-button>
            <el-button
              v-if="task.status === 'paused'"
              size="small"
              type="primary"
              @click="handleResume(task.task_id)"
            >
              <el-icon><VideoPlay /></el-icon>
              继续
            </el-button>
            <el-button
              v-if="!['completed', 'failed'].includes(task.status)"
              size="small"
              type="danger"
              @click="handleCancel(task.task_id)"
            >
              <el-icon><Close /></el-icon>
              取消
            </el-button>
          </div>
        </div>

        <el-progress
          :percentage="Math.round(task.progress)"
          :status="task.status === 'failed' ? 'exception' : task.status === 'completed' ? 'success' : ''"
          :stroke-width="8"
        />

        <div class="task-meta">
          <span v-if="task.speed" class="speed">
            <el-icon><Download /></el-icon>
            {{ task.speed }}
          </span>
          <span v-if="task.file_size" class="size">
            {{ formatFileSize(task.file_size) }}
          </span>
          <span v-if="task.error_message" class="error">
            <el-icon><Warning /></el-icon>
            {{ task.error_message }}
          </span>
        </div>
      </el-card>
    </div>
  </div>
</template>

<style scoped>
.download-page {
  max-width: 800px;
  margin: 0 auto;
  padding: 40px 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

h2 {
  color: #fff;
  font-size: 24px;
}

.empty {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 16px;
  padding: 60px 20px;
}

.task-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.task-card {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 12px;
}

.task-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.task-title {
  display: flex;
  align-items: center;
  gap: 10px;
}

.task-id {
  font-size: 14px;
  font-weight: 500;
  color: #303133;
  font-family: monospace;
}

.task-actions {
  display: flex;
  gap: 8px;
}

.task-meta {
  display: flex;
  gap: 16px;
  margin-top: 10px;
  font-size: 12px;
  color: #909399;
}

.speed, .size, .error {
  display: flex;
  align-items: center;
  gap: 4px;
}

.error {
  color: #f56c6c;
}
</style>
