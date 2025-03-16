<script setup lang="ts">
import { ref, computed} from 'vue'
import { useSidebarStore  } from '@/store/sidebar'
import { Fold, Expand, Edit } from '@element-plus/icons-vue' // 引入图标
import axios from 'axios';
const isSidebarVisible = computed(() => sidebarStore.isSidebarVisible);

import { useChatStore } from '@/store/chatStore'
const chatStore = useChatStore()

const sidebarStore = useSidebarStore();
const toggleSidebar = () => {
  sidebarStore.toggleSidebar(); // 切换侧边栏状态
};

</script>

<template>
  <div class="flex items-center justify-center space-x-1"> 
    <div class="button-container"> 
      <button @click="toggleSidebar" class="btn btn-square border-none">
        <svg class="w-6 h-6" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024"><path fill="currentColor" d="M128 192h768v128H128zm0 256h512v128H128zm0 256h768v128H128zm576-352 192 160-192 128z"></path></svg>
      </button>
    </div>
    <div class="button-container">
      <button @click="chatStore.newChat" class="btn btn-square border-none">
        <svg class="w-6 h-6" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024"><path fill="currentColor" d="M832 512a32 32 0 1 1 64 0v352a32 32 0 0 1-32 32H160a32 32 0 0 1-32-32V160a32 32 0 0 1 32-32h352a32 32 0 0 1 0 64H192v640h640z"></path><path fill="currentColor" d="m469.952 554.24 52.8-7.552L847.104 222.4a32 32 0 1 0-45.248-45.248L477.44 501.44l-7.552 52.8zm422.4-422.4a96 96 0 0 1 0 135.808l-331.84 331.84a32 32 0 0 1-18.112 9.088L436.8 623.68a32 32 0 0 1-36.224-36.224l15.104-105.6a32 32 0 0 1 9.024-18.112l331.904-331.84a96 96 0 0 1 135.744 0z"></path></svg>
      </button>
    </div>
  </div>
</template>
  
<style scoped>
</style>
  