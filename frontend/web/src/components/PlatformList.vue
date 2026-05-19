<script setup lang="ts">
import { onMounted } from 'vue'
import { useVideoStore } from '@/stores/video'

const videoStore = useVideoStore()

onMounted(() => {
  videoStore.getPlatforms()
})
</script>

<template>
  <div class="platform-list">
    <div
      v-for="platform in videoStore.platforms"
      :key="platform.id"
      class="platform-item"
      :class="platform.status"
    >
      <span class="platform-name">{{ platform.name }}</span>
      <span v-if="platform.status === 'coming_soon'" class="badge">即将支持</span>
    </div>
  </div>
</template>

<style scoped>
.platform-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: center;
  margin-bottom: 30px;
}

.platform-item {
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 8px 16px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 20px;
  color: #fff;
  font-size: 14px;
  backdrop-filter: blur(10px);
}

.platform-item.active {
  background: rgba(255, 255, 255, 0.3);
}

.platform-item.coming_soon {
  opacity: 0.6;
}

.badge {
  font-size: 10px;
  padding: 2px 6px;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 10px;
}
