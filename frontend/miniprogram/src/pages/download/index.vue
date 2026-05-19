<template>
  <view class="container">
    <view class="header">
      <text class="title">📥 离线缓存</text>
    </view>

    <view v-if="tasks.length === 0" class="empty">
      <text>暂无下载任务</text>
    </view>

    <view v-else class="task-list">
      <view v-for="task in tasks" :key="task.task_id" class="task-item">
        <view class="task-info">
          <text class="task-id">{{ task.task_id.slice(0, 8) }}</text>
          <text class="task-status" :class="task.status">{{ task.status }}</text>
        </view>
        <view class="progress-bar">
          <view class="progress-fill" :style="{ width: task.progress + '%' }" />
        </view>
        <text v-if="task.error_message" class="error">{{ task.error_message }}</text>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useVideoStore } from '@/stores/video'

const videoStore = useVideoStore()
const tasks = ref<any[]>([])

onMounted(async () => {
  const data = await videoStore.getDownloadList()
  tasks.value = data || []
})
</script>

<style lang="scss">
.container {
  padding: 20px;
}

.header {
  margin-bottom: 20px;
}

.title {
  font-size: 24px;
  font-weight: bold;
  color: #fff;
}

.empty {
  text-align: center;
  padding: 60px 0;
  color: rgba(255, 255, 255, 0.6);
}

.task-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.task-item {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 12px;
  padding: 16px;
}

.task-info {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
}

.task-id {
  font-size: 14px;
  color: #333;
}

.task-status {
  font-size: 12px;
  padding: 2px 8px;
  border-radius: 10px;
}

.task-status.pending {
  background: #e6a23c;
  color: #fff;
}

.task-status.downloading {
  background: #409eff;
  color: #fff;
}

.task-status.completed {
  background: #67c23a;
  color: #fff;
}

.task-status.failed {
  background: #f56c6c;
  color: #fff;
}

.progress-bar {
  height: 6px;
  background: #ebeef5;
  border-radius: 3px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(135deg, #667eea, #764ba2);
  border-radius: 3px;
  transition: width 0.3s;
}

.error {
  font-size: 12px;
  color: #f56c6c;
  margin-top: 8px;
  display: block;
}
</style>
