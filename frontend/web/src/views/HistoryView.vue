<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useVideoStore } from '@/stores/video'
import VideoCard from '@/components/VideoCard.vue'
import type { VideoInfo } from '@/types'

const videoStore = useVideoStore()
const historyList = ref<VideoInfo[]>([])

onMounted(() => {
  const stored = localStorage.getItem('parse_history')
  if (stored) {
    try {
      historyList.value = JSON.parse(stored)
    } catch {
      historyList.value = []
    }
  }
})

function clearHistory() {
  historyList.value = []
  localStorage.removeItem('parse_history')
}
</script>

<template>
  <div class="history-page">
    <div class="page-header">
      <h2>📋 解析历史</h2>
      <el-button v-if="historyList.length > 0" type="danger" size="small" @click="clearHistory">
        清空历史
      </el-button>
    </div>

    <div v-if="historyList.length === 0" class="empty">
      <el-empty description="暂无解析历史">
        <el-button type="primary" @click="$router.push('/')">去解析视频</el-button>
      </el-empty>
    </div>

    <div v-else class="history-list">
      <VideoCard v-for="video in historyList" :key="video.video_id" :video="video" />
    </div>
  </div>
</template>

<style scoped>
.history-page {
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

.history-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
</style>
