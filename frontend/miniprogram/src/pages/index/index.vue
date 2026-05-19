<template>
  <view class="container">
    <view class="header">
      <text class="title">🎬 OmniVideo</text>
      <text class="subtitle">多平台视频解析工具</text>
    </view>

    <view class="search-box">
      <input
        v-model="inputUrl"
        class="input"
        placeholder="粘贴视频链接"
        placeholder-style="color: #999"
      />
      <button class="btn-primary" :loading="loading" @tap="handleParse">
        解析
      </button>
    </view>

    <view class="platforms">
      <view
        v-for="p in platforms"
        :key="p.id"
        class="platform-tag"
        :class="p.status"
      >
        {{ p.name }}
      </view>
    </view>

    <view v-if="videoInfo" class="video-card">
      <image v-if="videoInfo.cover_url" :src="videoInfo.cover_url" class="cover" mode="aspectFill" />
      <view class="info">
        <text class="video-title">{{ videoInfo.title }}</text>
        <text v-if="videoInfo.author" class="author">👤 {{ videoInfo.author }}</text>
        <view class="stats">
          <text v-if="videoInfo.like_count">👍 {{ videoInfo.like_count }}</text>
          <text v-if="videoInfo.comment_count">💬 {{ videoInfo.comment_count }}</text>
        </view>
      </view>
      <view class="actions">
        <button v-if="videoInfo.video_url" class="btn-download" @tap="handleDownload">
          下载视频
        </button>
        <button v-if="videoInfo.video_url" class="btn-play" @tap="handlePlay">
          在线播放
        </button>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useVideoStore } from '@/stores/video'

const videoStore = useVideoStore()
const inputUrl = ref('')
const loading = ref(false)
const videoInfo = ref<any>(null)

const platforms = [
  { id: 'douyin', name: '抖音', status: 'active' },
  { id: 'bilibili', name: 'B站', status: 'active' },
  { id: 'xiaohongshu', name: '小红书', status: 'active' },
  { id: 'kuaishou', name: '快手', status: 'coming_soon' },
]

async function handleParse() {
  if (!inputUrl.value.trim()) {
    wx.showToast({ title: '请输入视频链接', icon: 'none' })
    return
  }
  loading.value = true
  try {
    const data = await videoStore.parseVideo(inputUrl.value.trim())
    videoInfo.value = data
    wx.showToast({ title: '解析成功', icon: 'success' })
  } catch (error) {
    wx.showToast({ title: '解析失败', icon: 'none' })
  } finally {
    loading.value = false
  }
}

async function handleDownload() {
  if (!videoInfo.value?.video_url) return
  try {
    await videoStore.createDownload(videoInfo.value.video_url, videoInfo.value.video_id)
    wx.showToast({ title: '已添加到下载', icon: 'success' })
  } catch (error) {
    wx.showToast({ title: '下载失败', icon: 'none' })
  }
}

function handlePlay() {
  if (!videoInfo.value?.video_url) return
  wx.navigateTo({
    url: `/pages/player/index?url=${encodeURIComponent(videoInfo.value.video_url)}`,
  })
}
</script>

<style lang="scss">
.container {
  padding: 30px 20px;
}

.header {
  text-align: center;
  margin-bottom: 40px;
}

.title {
  font-size: 32px;
  font-weight: bold;
  color: #fff;
  display: block;
}

.subtitle {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.8);
  margin-top: 8px;
  display: block;
}

.search-box {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.input {
  flex: 1;
  height: 44px;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 22px;
  padding: 0 20px;
  font-size: 14px;
}

.btn-primary {
  width: 80px;
  height: 44px;
  background: #fff;
  color: #667eea;
  border-radius: 22px;
  font-size: 14px;
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: center;
}

.platforms {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  justify-content: center;
  margin-bottom: 20px;
}

.platform-tag {
  padding: 6px 14px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 16px;
  color: #fff;
  font-size: 12px;
}

.platform-tag.coming_soon {
  opacity: 0.5;
}

.video-card {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 16px;
  padding: 16px;
}

.cover {
  width: 100%;
  height: 200px;
  border-radius: 12px;
  background: #f0f0f0;
}

.info {
  margin-top: 12px;
}

.video-title {
  font-size: 16px;
  font-weight: bold;
  color: #333;
  display: block;
}

.author {
  font-size: 13px;
  color: #666;
  margin-top: 6px;
  display: block;
}

.stats {
  display: flex;
  gap: 15px;
  margin-top: 8px;
  font-size: 12px;
  color: #999;
}

.actions {
  display: flex;
  gap: 10px;
  margin-top: 16px;
}

.btn-download {
  flex: 1;
  height: 40px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: #fff;
  border-radius: 20px;
  font-size: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-play {
  flex: 1;
  height: 40px;
  background: #f0f2f5;
  color: #667eea;
  border-radius: 20px;
  font-size: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
