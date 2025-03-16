<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useChatStore } from '@/store/chatStore'

const chatStore = useChatStore()

onMounted(() => {
  chatStore.fetchChatHistory();
});

// 点击菜单项处理函数
const handleSelect = (chatId: string) => {
  chatStore.curr_chat_id = chatId
  chatStore.selectChat(chatId)
}

// const activeMenu = ref('20');
// const chatHistoryList = ref([
//   { chatId: '2', label: '历史消息' },
//   { chatId: '1', label: '历史消息' },
// ]);
// const messagesList = ref([]) // 新增消息列表存储
// const isLoading = ref(false) // 加载状态
// // 新增获取消息列表函数
// async function fetchMessages(chatId: string) {
//   try {
//     isLoading.value = true;
//     const response = await axios.get(
//       `http://localhost:8000/api/v1/chat/chat_history_id_get/?chat_id=${chatId}`,
//     );
//     messagesList.value = response.data;
//   } catch (error) {
//     console.error("Failed to fetch messages:", error);
//   } finally {
//     isLoading.value = false;
//   }
// }
</script>

<template>
  <div class="chat-history" >
    <ul class="menu menu-lg bg-base-200 rounded-box w-[240px] space-y-1 p-2">
      <li v-for="chat in chatStore.chatHistoryList"
        :key="chat.chat_id"
        @click="handleSelect(chat.chat_id)"
      >
        <a class="rounded-xl" :class="{'menu-active':  chat.chat_id === chatStore.curr_chat_id}" >
          {{chat.chat_topic}}
        </a>
      </li>
    </ul>
  </div>
</template>
