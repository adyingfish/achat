<script setup lang="ts">
import { ref, computed, onMounted, watchEffect } from 'vue'
import { useSidebarStore } from '@/store/sidebar'
import HandleBtnMain from '@/components/aside/HandleBtnMain.vue'
import ModelSelect from '@/components/sidebar/ModelSelect.vue'
const sidebarStore = useSidebarStore();
const isSidebarVisible = computed(() => sidebarStore.isSidebarVisible); // 监听侧边栏状态
</script>

<template>
<div>
  <div class="flex items-center space-x-1 pt-[.5rem]">
    <div v-show="!isSidebarVisible" class=" pl-2">
      <HandleBtnMain />
    </div>
    <div >
      <ModelSelect />
    </div>
  </div>
</div>
</template>
