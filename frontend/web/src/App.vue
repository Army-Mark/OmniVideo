<script setup lang="ts">
import { RouterView, RouterLink, useRoute } from 'vue-router'
import { computed } from 'vue'

const route = useRoute()

const navItems = [
  { path: '/', label: '首页', icon: 'HomeFilled' },
  { path: '/download', label: '下载', icon: 'Download' },
  { path: '/history', label: '历史', icon: 'Clock' },
]

const isActive = (path: string) => route.path === path
</script>

<template>
  <div class="app-layout">
    <nav class="navbar">
      <div class="nav-brand">
        <span class="brand-icon">🎬</span>
        <span class="brand-text">OmniVideo</span>
      </div>
      <div class="nav-links">
        <RouterLink
          v-for="item in navItems"
          :key="item.path"
          :to="item.path"
          class="nav-link"
          :class="{ active: isActive(item.path) }"
        >
          <el-icon><component :is="item.icon" /></el-icon>
          <span>{{ item.label }}</span>
        </RouterLink>
      </div>
    </nav>

    <main class="main-content">
      <RouterView />
    </main>

    <footer class="footer">
      <p>OmniVideo © 2024 - 多平台视频解析工具</p>
    </footer>
  </div>
</template>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
}

.app-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.navbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 40px;
  height: 60px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  position: sticky;
  top: 0;
  z-index: 100;
}

.nav-brand {
  display: flex;
  align-items: center;
  gap: 10px;
}

.brand-icon {
  font-size: 24px;
}

.brand-text {
  font-size: 20px;
  font-weight: bold;
  color: #fff;
}

.nav-links {
  display: flex;
  gap: 8px;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  border-radius: 8px;
  color: rgba(255, 255, 255, 0.7);
  text-decoration: none;
  font-size: 14px;
  transition: all 0.3s;
}

.nav-link:hover {
  background: rgba(255, 255, 255, 0.15);
  color: #fff;
}

.nav-link.active {
  background: rgba(255, 255, 255, 0.25);
  color: #fff;
  font-weight: 500;
}

.main-content {
  flex: 1;
}

.footer {
  text-align: center;
  padding: 20px;
  color: rgba(255, 255, 255, 0.5);
  font-size: 13px;
}
</style>
