// src/stores/currChatMsgStore.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

// 定义消息类型（若未创建可在此处直接定义）
interface ChatMsg {
  message_id: string
  content: string
  role: 'user' | 'assistant'
  timestamp: number
  status?: 'loading' | 'complete' | 'error'
}

export const useCurrChatMsgStore = defineStore('currChatMsg', () => {
  // ​**State 定义**
  const currChatMsgList = ref<ChatMsg[]>([]) // 当前会话消息列表
  const chatId = ref<string | null>(null)       // 当前会话ID

  const loadHistory = (messages: ChatMsg[], id: string) => {
    currChatMsgList.value = messages; // 直接替换消息列表
    chatId.value = id;
  }
  // 追加新消息
  const appendMessage = (message: ChatMsg) => {
    currChatMsgList.value.push(message); // 直接追加到列表
  }
  // 更新消息状态
  const updateMessage = (messageId: string, updates: Partial<ChatMsg>) => {
    const index = currChatMsgList.value.findIndex(m => m.message_id === messageId);
    if (index >= 0) {
      currChatMsgList.value[index] = { 
        ...currChatMsgList.value[index], 
        ...updates 
      };
    }
  }

  // 清空当前会话
  const clearSession = () => {
    currChatMsgList.value = []; // 重置消息列表
    chatId.value = null;       // 重置会话ID
  }

  // ​**Getters 计算属性**
  // 格式化时间戳的格式化消息列表
  const formattedMessages = computed(() => 
    currChatMsgList.value.map(msg => ({
      ...msg,
      timestamp: new Date(msg.timestamp).toLocaleString()
    }))
  );

  // 获取最后一条未完成的消息（"loading" 状态）
  const lastPendingMessage = computed(() => 
    currChatMsgList.value.findLast(msg => msg.status === 'loading')
  );

  // ​**暴露给组件使用的接口**
  return {
    currChatMsgList,
    chatId,
    loadHistory,
    appendMessage,
    updateMessage,
    clearSession,
    formattedMessages,
    lastPendingMessage
  }
})