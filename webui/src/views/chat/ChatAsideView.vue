<script setup lang="ts">
import AsideHeader from '@/views/chat/AsideHeaderView.vue'
import AsideMain from '@/views/chat/AsideMainView.vue'
import AsideFooter from '@/views/chat/AsideFooterView.vue'

import { ref, computed, onMounted, watch } from 'vue'
import { useSidebarStore } from '@/store/sidebar'
const sidebarStore = useSidebarStore();
const isSidebarVisible = computed(() => sidebarStore.isSidebarVisible); // 监听侧边栏状态
const sidebarContainer = computed(() => ({
  activeSidebar: sidebarStore.isSidebarVisible,
  inactiveSidebar: !sidebarStore.isSidebarVisible
}));
</script>

<template>
  <div class="flex flex-col h-screen" :class="sidebarContainer">
    <div class="min-h-[100px] shrink-0 px-2">
      <AsideHeader />
    </div>
    <div class="flex-1 overflow-y-auto overscroll-x-none">
      <AsideMain />
    </div>
    <div class="flex-none">
      <AsideFooter />
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
</style>