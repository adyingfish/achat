<script setup lang="ts">
import ConvHeader from '@/views/chat/ConvHeaderView.vue'
import ConvChat from '@/views/chat/ConvChatView.vue'
import ConvInput from '@/views/chat/ConvInputView.vue'
</script>

<template>
  <div class="flex flex-col h-screen">
    <div class="shrink-0 h-[60px]">
      <ConvHeader />
    </div>
    <div class="flex-1 overflow-y-auto pb-[1.5rem] justify-center">
      <ConvChat />
    </div>
    <div class="shrink-0">
      <ConvInput />
    </div> 
  </div>
</template>