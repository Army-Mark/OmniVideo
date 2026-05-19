<template>
  <view class="container">
    <view class="header">
      <view class="avatar">👤</view>
      <text class="username">未登录</text>
    </view>

    <view class="menu-list">
      <view class="menu-item" @tap="showToast('功能开发中')">
        <text>📋 解析历史</text>
        <text class="arrow">›</text>
      </view>
      <view class="menu-item" @tap="showToast('功能开发中')">
        <text>⭐ 我的收藏</text>
        <text class="arrow">›</text>
      </view>
      <view class="menu-item" @tap="showToast('功能开发中')">
        <text>⚙️ 设置</text>
        <text class="arrow">›</text>
      </view>
      <view class="menu-item" @tap="showToast('功能开发中')">
        <text>ℹ️ 关于</text>
        <text class="arrow">›</text>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
function showToast(msg: string) {
  wx.showToast({ title: msg, icon: 'none' })
}
</script>

<style lang="scss">
.container {
  padding: 20px;
}

.header {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 40px 0;
}

.avatar {
  width: 80px;
  height: 80px;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 40px;
  margin-bottom: 12px;
}

.username {
  font-size: 18px;
  color: #fff;
  font-weight: bold;
}

.menu-list {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 16px;
  overflow: hidden;
}

.menu-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid #f0f0f0;
  font-size: 15px;
  color: #333;
}

.menu-item:last-child {
  border-bottom: none;
}

.arrow {
  font-size: 20px;
  color: #ccc;
}
</style>
