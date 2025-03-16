<script setup lang="ts">
  import { ref, onMounted } from 'vue'
  import { useChatStore } from '@/store/chatStore'
  const chatStore = useChatStore()

  const activeModel = ref('DeepSeek-V3');
  const modelList = ref([
    { label: 'DeepSeek-V3', llm_model: 'deepseek-chat' },
    { label: 'DeepSeek-R1', llm_model: 'deepseek-reasoner' },
  ]);
  // 更新 setActiveModel  的方法
  const setActiveModel = (label: string, llm_model: string) => {
    activeModel .value = label;
    chatStore.curr_llm_model = llm_model
  };

onMounted(() => {
  setActiveModel('DeepSeek-V3', 'deepseek-chat');
});
</script>

<template>
  <div class="flex items-center justify-center">
    <div class="dropdown" style="border-radius: 12px; border: none;">
      <div tabindex="0" role="button" class="btn" style=" border-radius: 12px; border: none;">    
        {{ activeModel  }}
        <svg class="w-4 h-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024"><path fill="currentColor" d="M831.872 340.864 512 652.672 192.128 340.864a30.592 30.592 0 0 0-42.752 0 29.12 29.12 0 0 0 0 41.6L489.664 714.24a32 32 0 0 0 44.672 0l340.288-331.712a29.12 29.12 0 0 0 0-41.728 30.592 30.592 0 0 0-42.752 0z"></path></svg>
      </div>
      <div tabindex="0" class="dropdown-content">
        <div v-for="(item, index) in modelList" :key="index">
          <button class="btn btn-block border-none" @click="setActiveModel(item.label,item.llm_model)">{{ item.label }}</button>
        </div>
      </div>
    </div>
  </div>
</template>
