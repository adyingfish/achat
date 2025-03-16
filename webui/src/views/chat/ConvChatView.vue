<script setup lang="ts">
import { ref } from 'vue';
import { useChatStoreSingle } from '@/store/chatStoreSingle'
const store = useChatStoreSingle()

import { useChatStore } from '@/store/chatStore'
const chatStore = useChatStore()

// 引入 marked 库
import { marked } from 'marked'

// 定义一个方法，用于将 markdown 转换为 HTML
const renderMarkdown = (content: string) => {
  return marked(content);
};
</script>

<template>
  <div class="flex h-full flex-col overflow-y-auto">
    <div class="max-w-[800px] mx-auto">
      <div 
        v-for="message in chatStore.messages" 
        :key="message.message_id"
        :class="message.message_role === 'user' ? 'flex justify-end' : 'flex justify-start'"
      >
      <div>
        <div 
          class="max-w-full p-3 mb-4 text-base-content/50"
          v-if="message.reasoning_content"
          v-html="renderMarkdown(message.reasoning_content)"
        ></div>
        <div 
          class="max-w-full p-3 mb-4"
          :class="message.message_role === 'user' 
            ? 'rounded-xl bg-base-300 text-base-content' 
            : ''"
          v-html="renderMarkdown(message.message_content)"
        ></div>
      </div>
        <!-- <div v-html="renderMarkdown(message.message_role)"></div>
        <div v-if="message.reasoning_content" v-html="renderMarkdown(message.reasoning_content)"></div>
        <div v-html="renderMarkdown(message.message_content)"></div> -->
      </div>
    </div>
  </div>
</template>