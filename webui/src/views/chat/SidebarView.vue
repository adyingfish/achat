<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useSidebarStore } from '@/store/sidebar'
import AsideBtn from '@/components/AsideButton.vue'
import Setting from '@/components/sidebar/Setting.vue'
import { MoreFilled } from '@element-plus/icons-vue'
import axios from 'axios'
import { useRoute } from 'vue-router'

</script>

<template>
  <div class="sidebarContainer">
    <div class="sidebar-header">
      <AsideBtn />
    </div>
    <!-- 菜单区域 -->
    <div class="menu-container">
      <div 
        v-for="(menuItem, index) in menuItems" 
        :key="index" 
        :class="['menu-item', {active: activeMenu === menuItem.index }]"
        @click="activeMenu = menuItem.index"
        @mouseover="hoveredMenuIndex = menuItem.index"
        @mouseleave="hoveredMenuIndex = null"
      >
        <div>
          <span>{{ menuItem.label }}</span>
        </div>
        <ElTooltip content="选项" placement="top">
        <div v-show="hoveredMenuIndex === menuItem.index">

          <ElPopover trigger="click" placement="bottom" width="150">
            <template #reference>
              <button class="settings-button" @click.stop>
                <el-icon :size="20"><MoreFilled /></el-icon>
              </button>
            </template>
            <div class="popover-content">
              <button class="popover-button" @click="handleRename(menuItem.index)">重命名</button>
              <button class="popover-button" @click="handleDelete(menuItem.index)">删除</button>
            </div>
          </ElPopover>
        
        </div>
      </ElTooltip>
      </div>
    </div>
    <div class="sidebar-footer">
      <div class="setting-container">
        <Setting/>
      </div>
    </div>
  </div>
</template>

<style scoped>
.activeSidebar {
  width: 260px;
  height: 100vh;
}
.inactiveSidebar {
  display:none;
}

.sidebar-container {
  display: grid;
  grid-template-rows: 260px 1fr;
  width: 260px;
  height: 100vh;
}

.sidebar-content {
  display: grid;
  grid-template-rows: 140px 1fr 140px;
  padding-left:1rem; /* 上 右 下 左 */
  padding-right:1rem;
}
.sidebar-header {
  padding-left:1rem; /* 上 右 下 左 */
  padding-right:1rem;
}


/* 菜单区域 */
.menu-container {
  width: 260px;
  height: calc(100vh - 280px); /* 高度设置为减去按钮高度 */
  padding-right: .5rem;
  margin-right: -0.5rem;
  overflow-y: scroll;
}
.menu-item {
  display: flex;
  justify-content:space-between;
  align-items: center;
  padding: .5rem 1rem;
  cursor: pointer;
  border-radius: 10px;
  cursor: pointer;
  transition: background-color 0.3s;
}
.menu-item:hover {
  background-color: #f0f0f0; /* 添加hover效果 */
}
.menu-item.active {
  background-color: #f5f5f5;
}
.menu-item i {
  margin-right: 1rem;
}


/* 设置按钮样式 */
.settings-button {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.2rem;
  color: #030303;
  transition: color 0.3s;
}
.settings-button:hover {
  color: #333;
}

/* 弹出框按钮样式 */
.popover-button {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.5rem 1rem;
  width: 100%;
  text-align: left;
  color: #333;
  transition: background-color 0.3s;
}
.popover-button:hover {
  background-color: #f0f0f0;
}
</style>
