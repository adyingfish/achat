<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import Setting from '@/components/sidebar/Setting.vue'
import HandleBtnAside from '@/components/sidebar/HandleBtnAside.vue'
import { useSidebarStore } from '@/store/sidebar'
import { useRoute } from 'vue-router'
import axios from 'axios'

const sidebarStore = useSidebarStore();
const isSidebarVisible = computed(() => sidebarStore.isSidebarVisible); // 监听侧边栏状态
const sidebarContainer = computed(() => ({
  activeSidebar: sidebarStore.isSidebarVisible,
  inactiveSidebar: !sidebarStore.isSidebarVisible
}));

const activeMenu = ref('18');
const chatHistoryList = ref([
  { chatId: '18', label: '历史消息' },
  { chatId: '17', label: '历史消息' },
  { chatId: '16', label: '历史消息' },
  { chatId: '15', label: '历史消息' },
  { chatId: '14', label: '历史消息' },
  { chatId: '13', label: '历史消息' },
  { chatId: '12', label: '历史消息' },
  { chatId: '11', label: '历史消息' },
  { chatId: '10', label: '历史消息' },
  { chatId: '9', label: '历史消息' },
  { chatId: '8', label: '历史消息' },
  { chatId: '7', label: '历史消息' },
  { chatId: '6', label: '历史消息' },
  { chatId: '5', label: '历史消息' },
  { chatId: '4', label: '历史消息' },
  { chatId: '3', label: '历史消息' },
  { chatId: '2', label: '历史消息' },
  { chatId: '1', label: '历史消息' },
]);

const openSettingsDialog = (menuItemIndex: string) => {
  // 打开设置对话框，例如显示删除或重命名等选项
  console.log('打开设置对话框:', menuItemIndex);
};
const handleRename = (menuItemIndex: string) => {
  console.log('重命名:', menuItemIndex);
};
const handleDelete = (menuItemIndex: string) => {
  console.log('删除:', menuItemIndex);
};

const route = useRoute()
const data = ref(null)
// const fetchChatHistory = async () => {
//   try {
//     const authed_user_id = localStorage.getItem('authed_user_id')
//     console.log('authed_user_id:', authed_user_id)
//     const response = await axios.get(`http://localhost:8000/api/chat/chathistoryget/${authed_user_id}`)
//     data.value = response.data
//   } catch (err) {
//     error.value = err.response?.data?.message || '请求失败'
//   } finally {
//     loading.value = false
//   }
// }
// onMounted(fetchData)
</script>

<template>
  <div :class="sidebarContainer">
    <div class="sidebar-content">
      <div class="sidebar-header">
        <HandleBtnAside />
        <div>
          <label class="swap swap-rotate">
            <!-- this hidden checkbox controls the state -->
            <input type="checkbox" class="theme-controller" value="light" />
            <!-- sun icon -->
            <svg
              class="swap-off h-8 w-8 fill-current"
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24">
              <path
                d="M5.64,17l-.71.71a1,1,0,0,0,0,1.41,1,1,0,0,0,1.41,0l.71-.71A1,1,0,0,0,5.64,17ZM5,12a1,1,0,0,0-1-1H3a1,1,0,0,0,0,2H4A1,1,0,0,0,5,12Zm7-7a1,1,0,0,0,1-1V3a1,1,0,0,0-2,0V4A1,1,0,0,0,12,5ZM5.64,7.05a1,1,0,0,0,.7.29,1,1,0,0,0,.71-.29,1,1,0,0,0,0-1.41l-.71-.71A1,1,0,0,0,4.93,6.34Zm12,.29a1,1,0,0,0,.7-.29l.71-.71a1,1,0,1,0-1.41-1.41L17,5.64a1,1,0,0,0,0,1.41A1,1,0,0,0,17.66,7.34ZM21,11H20a1,1,0,0,0,0,2h1a1,1,0,0,0,0-2Zm-9,8a1,1,0,0,0-1,1v1a1,1,0,0,0,2,0V20A1,1,0,0,0,12,19ZM18.36,17A1,1,0,0,0,17,18.36l.71.71a1,1,0,0,0,1.41,0,1,1,0,0,0,0-1.41ZM12,6.5A5.5,5.5,0,1,0,17.5,12,5.51,5.51,0,0,0,12,6.5Zm0,9A3.5,3.5,0,1,1,15.5,12,3.5,3.5,0,0,1,12,15.5Z" />
            </svg>
            <!-- moon icon -->
            <svg
              class="swap-on h-8 w-8 fill-current"
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24">
              <path
                d="M21.64,13a1,1,0,0,0-1.05-.14,8.05,8.05,0,0,1-3.37.73A8.15,8.15,0,0,1,9.08,5.49a8.59,8.59,0,0,1,.25-2A1,1,0,0,0,8,2.36,10.14,10.14,0,1,0,22,14.05,1,1,0,0,0,21.64,13Zm-9.5,6.69A8.14,8.14,0,0,1,7.08,5.22v.27A10.15,10.15,0,0,0,17.22,15.63a9.79,9.79,0,0,0,2.1-.22A8.11,8.11,0,0,1,12.14,19.73Z" />
            </svg>
          </label>
          主题
        </div>
      </div>
      <!-- 菜单区域 -->
      <div class="menu-container">
        <!-- <div 
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
        </div> -->
        <div class="chat-history" >
          <ul class="menu menu-lg bg-base-200 rounded-box w-56 space-y-1">
          <li v-for="(chatHistory, index) in chatHistoryList"
            :key="chatHistory.chatId"
            @click="activeMenu = chatHistory.chatId"
            ><a class="rounded-xl" :class="{'menu-active': chatHistory.chatId === activeMenu}" >对话记录{{chatHistory.chatId}}</a>
          </li>
        </ul>
        </div>
      </div>
      <div class="sidebar-footer">
        <div class="setting-container">
          <Setting/>
        </div>
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
