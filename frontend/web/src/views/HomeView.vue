<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useVideoStore } from '@/stores/video'
import { ElMessage } from 'element-plus'
import VideoCard from '@/components/VideoCard.vue'
import PlatformList from '@/components/PlatformList.vue'

const videoStore = useVideoStore()
const inputUrl = ref('')

async function handleParse() {
  if (!inputUrl.value.trim()) {
    ElMessage.warning('请输入视频链接')
    return
  }
  try {
    await videoStore.parseVideo(inputUrl.value.trim())
    ElMessage.success('解析成功')
  } catch (error: any) {
    ElMessage.error(error.message || '解析失败，请检查链接是否正确')
  }
}

async function handlePaste() {
  try {
    const text = await navigator.clipboard.readText()
    if (text) {
      inputUrl.value = text.trim()
      ElMessage.info('已粘贴链接，点击解析按钮开始解析')
    }
  } catch {
  }
}

onMounted(() => {
  videoStore.getPlatforms()
})
</script>

<template>
  <div class="home">
    <div class="header">
      <h1 class="title">🎬 OmniVideo</h1>
      <p class="subtitle">多平台视频解析与下载工具</p>
    </div>

    <div class="search-box">
      <div class="input-wrapper">
        <el-input
          v-model="inputUrl"
          placeholder="粘贴视频链接，支持抖音、B站、小红书等平台"
          size="large"
          clearable
          @keyup.enter="handleParse"
        />
        <div class="input-actions">
          <el-button @click="handlePaste" title="从剪贴板粘贴">
            <el-icon><DocumentCopy /></el-icon>
            粘贴
          </el-button>
          <el-button type="primary" :loading="videoStore.loading" @click="handleParse">
            <el-icon><Search /></el-icon>
            解析
          </el-button>
        </div>
      </div>
    </div>

    <PlatformList />

    <VideoCard v-if="videoStore.currentVideo" :video="videoStore.currentVideo" />

    <div v-if="!videoStore.currentVideo && !videoStore.loading" class="tips">
      <el-card class="tip-card">
        <template #header>
          <span>💡 使用说明</span>
        </template>
        <ul>
          <li>复制抖音、B站、小红书等平台的视频链接</li>
          <li>粘贴到上方输入框，点击"解析"按钮</li>
          <li>解析完成后可下载无水印视频或在线播放</li>
        </ul>
      </el-card>
    </div>
  </div>
</template>

<style scoped>
.home {
  max-width: 800px;
  margin: 0 auto;
  padding: 40px 20px;
}

.header {
  text-align: center;
  margin-bottom: 40px;
}

.title {
  font-size: 48px;
  color: #fff;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
  margin-bottom: 10px;
}

.subtitle {
  font-size: 18px;
  color: rgba(255, 255, 255, 0.8);
}

.search-box {
  margin-bottom: 30px;
}

.input-wrapper {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.input-actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
}

:deep(.el-input__wrapper) {
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15) !important;
}

.tips {
  margin-top: 30px;
}

.tip-card {
  background: rgba(255, 255, 255, 0.95);
}

.tip-card ul {
  padding-left: 20px;
  line-height: 2;
  color: #606266;
}
</style>
