<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import ChatAside from '@/views/chat/ChatAsideView.vue'
import ChatMain from '@/views/chat/ChatMainView.vue'
// import ChatMain from '@/components/ChatStreamZhipuTest.vue'
import { useSidebarStore } from '@/store/sidebar'
const sidebarStore = useSidebarStore();
const chatContainer = computed(() => ({
  activeChat: sidebarStore.isSidebarVisible,
  inactiveChat: !sidebarStore.isSidebarVisible
}));
const asideContainer = computed(() => ({
  active: sidebarStore.isSidebarVisible,
  inactive: !sidebarStore.isSidebarVisible
}));
</script>

<template>
  <div :class="chatContainer">
    <div :class="asideContainer">
      <ChatAside />
    </div>
    <div class="main-container">
      <ChatMain />
    </div>
  </div>
</template>

<style scoped>
.activeChat{
  display: flex;
  height: 100vh;
}
.inactiveChat{
  display: flex;
  height: 100vh;
}
.active {
  flex: 0 0 260px;
}
.inactive {
  flex: 0 0 0;
}
.main-container{
  flex: 1; /* 主内容区域自适应剩余空间 */
  width: 100%;
  height: 100vh;
}
</style>
