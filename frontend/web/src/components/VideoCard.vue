<script setup lang="ts">
import { ElMessage } from 'element-plus'
import { useVideoStore } from '@/stores/video'
import type { VideoInfo } from '@/types'

const props = defineProps<{
  video: VideoInfo
}>()

const videoStore = useVideoStore()

async function handleDownload() {
  if (!props.video.video_url) {
    ElMessage.warning('该视频无法下载')
    return
  }
  try {
    await videoStore.createDownload(props.video.video_url, props.video.video_id)
    ElMessage.success('下载任务已创建，请在下载中心查看进度')
  } catch (error) {
    ElMessage.error('创建下载任务失败')
  }
}

function handlePlay() {
  if (props.video.video_url) {
    window.open(props.video.video_url, '_blank')
  }
}

function handleCopyUrl() {
  if (props.video.video_url) {
    navigator.clipboard.writeText(props.video.video_url)
    ElMessage.success('视频链接已复制到剪贴板')
  }
}

function getPlatformIcon(platform: string): string {
  const icons: Record<string, string> = {
    douyin: '🎵',
    bilibili: '📺',
    xiaohongshu: '📕',
    kuaishou: '⚡',
    youtube: '▶️',
    pipixia: '🦐',
    haokan: '👁️',
  }
  return icons[platform] || '🎬'
}

function getPlatformName(platform: string): string {
  const names: Record<string, string> = {
    douyin: '抖音',
    bilibili: '哔哩哔哩',
    xiaohongshu: '小红书',
    kuaishou: '快手',
    youtube: 'YouTube',
    pipixia: '皮皮虾',
    haokan: '好看视频',
  }
  return names[platform] || platform
}

function formatDuration(seconds?: number): string {
  if (!seconds) return ''
  const m = Math.floor(seconds / 60)
  const s = seconds % 60
  return `${m}:${s.toString().padStart(2, '0')}`
}

function formatCount(count?: number): string {
  if (!count) return '0'
  if (count >= 10000) {
    return (count / 10000).toFixed(1) + '万'
  }
  return count.toString()
}
</script>

<template>
  <el-card class="video-card">
    <div class="video-content">
      <div class="cover-wrapper">
        <div class="cover">
          <img v-if="video.cover_url" :src="video.cover_url" :alt="video.title" crossorigin="anonymous" />
          <div v-else class="no-cover">
            <el-icon><Picture /></el-icon>
            <span>暂无封面</span>
          </div>
        </div>
        <span v-if="video.duration" class="duration">{{ formatDuration(video.duration) }}</span>
      </div>

      <div class="info">
        <div class="platform-tag">
          <span class="icon">{{ getPlatformIcon(video.platform) }}</span>
          <span>{{ getPlatformName(video.platform) }}</span>
        </div>

        <h3 class="title" :title="video.title">{{ video.title }}</h3>

        <p v-if="video.description" class="description" :title="video.description">
          {{ video.description }}
        </p>

        <div v-if="video.author" class="author">
          <el-avatar v-if="video.author_avatar" :src="video.author_avatar" :size="24" crossorigin="anonymous" />
          <el-icon v-else><User /></el-icon>
          <span>{{ video.author }}</span>
        </div>

        <div class="stats">
          <span v-if="video.like_count" class="stat-item">
            <el-icon><StarFilled /></el-icon>
            {{ formatCount(video.like_count) }}
          </span>
          <span v-if="video.comment_count" class="stat-item">
            <el-icon><ChatDotRound /></el-icon>
            {{ formatCount(video.comment_count) }}
          </span>
          <span v-if="video.share_count" class="stat-item">
            <el-icon><Share /></el-icon>
            {{ formatCount(video.share_count) }}
          </span>
        </div>
      </div>
    </div>

    <div class="actions">
      <el-button v-if="video.video_url" type="primary" @click="handleDownload">
        <el-icon><Download /></el-icon>
        下载视频
      </el-button>
      <el-button v-if="video.video_url" @click="handlePlay">
        <el-icon><VideoPlay /></el-icon>
        在线播放
      </el-button>
      <el-button v-if="video.video_url" @click="handleCopyUrl">
        <el-icon><Link /></el-icon>
        复制链接
      </el-button>
    </div>
  </el-card>
</template>

<style scoped>
.video-card {
  background: rgba(255, 255, 255, 0.95);
  margin-top: 20px;
  border-radius: 16px;
  overflow: hidden;
}

.video-content {
  display: flex;
  gap: 20px;
}

.cover-wrapper {
  position: relative;
  flex-shrink: 0;
}

.cover {
  width: 240px;
  height: 160px;
  border-radius: 12px;
  overflow: hidden;
  background: #f0f0f0;
}

.cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.no-cover {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #909399;
  gap: 8px;
}

.duration {
  position: absolute;
  bottom: 8px;
  right: 8px;
  background: rgba(0, 0, 0, 0.7);
  color: #fff;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 12px;
}

.info {
  flex: 1;
  min-width: 0;
}

.platform-tag {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 4px 10px;
  background: #f0f2f5;
  border-radius: 12px;
  font-size: 12px;
  color: #606266;
  margin-bottom: 10px;
}

.title {
  font-size: 18px;
  color: #303133;
  margin-bottom: 8px;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.description {
  font-size: 13px;
  color: #909399;
  margin-bottom: 10px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.author {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 10px;
  font-size: 14px;
  color: #606266;
}

.stats {
  display: flex;
  gap: 16px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  color: #909399;
}

.actions {
  display: flex;
  gap: 10px;
  margin-top: 20px;
  padding-top: 16px;
  border-top: 1px solid #ebeef5;
}

@media (max-width: 600px) {
  .video-content {
    flex-direction: column;
  }

  .cover {
    width: 100%;
    height: 200px;
  }
}
</style>
