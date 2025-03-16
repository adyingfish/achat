// src/stores/chatStore.ts
import { defineStore } from 'pinia'
import { ref } from 'vue'

export interface Message {
  message_id: string;
  message_role: 'user' | 'assistant';
  reasoning_content: string;
  message_content: string;
  // timestamp: string;
}

export interface ChatRequest {
  message_id: string;
  user_message: string;
  chat_id: string;
  llm_model: string;
}

export interface ChatHistory {
  chat_id: string;
  chat_topic: string;
  // timestamp: string;
}

export const useChatStore = defineStore('chat', () => {
  
  
  const messages = ref<Message[]>([])  // 明确指定类型为 Message[]
  const chatRequests = ref<ChatRequest[]>([])  // 聊天请求列表

  const activeChatId = ref('')
  const chatHistoryList = ref<ChatHistory[]>([])

  const user_message = ref('')
  const curr_chat_id = ref('')
  const curr_llm_model = ref('')

  const responseData = ref<string | null>(null) // 后端响应数据
  const isLoading = ref(false)                // 加载状态

  

  // 使用 const 定义箭头函数：获取聊天记录
  const selectChat = async (chatId: string) => {
    curr_chat_id.value = chatId
    try {
      const response = await fetch(`http://localhost:8000/api/v1/chat/chat_history_id_get/?chat_id=${chatId}`)
      if (!response.ok) {
        throw new Error('网络错误')
      }
      const data = await response.json()
      messages.value = data
    } catch (error) {
      console.error('获取消息列表失败:', error)
      messages.value = [] // 出错时清空消息列表
    }
  }
  // 使用 const 定义箭头函数：发送消息
  const sendMessage = async () => {
    // 如果输入框为空，不发送请求
    if (!user_message.value.trim()) return
    // 当前聊天chat_id不存在时，创建新聊天
    if (!curr_chat_id.value.trim())
      {
        curr_chat_id.value= window.crypto.randomUUID();
        chatHistoryList.value.push({
          chat_id: curr_chat_id.value,
          chat_topic: curr_llm_model.value
        })
      }
    // 每次用户新消息固定生成一个新的message_id
    const new_user_message_id = window.crypto.randomUUID();
    // 将用户新消息同步到前端客户端消息列表
    messages.value.push({
      message_id: new_user_message_id,
      message_role: 'user',
      reasoning_content: '',
      message_content: user_message.value,
    });
    isLoading.value = true
    try {
      const response = await fetch('http://localhost:8000/api/v1/chat/chat_stream', {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          message_id: new_user_message_id,
          user_message: user_message.value,
          chat_id: curr_chat_id.value,
          llm_model: curr_llm_model.value
        }),
      })
      user_message.value = ''    // 清空输入框
      if (!response.ok) {
        throw new Error(`网络错误:${response.status},${response.statusText}`)
      }

    // 处理流式响应
    const reader = response.body ? response.body.getReader() : null;
    if (!reader) throw new Error("读取响应失败");
    const decoder = new TextDecoder();
    let buffer = '';  // 用于暂存不完整的数据块
    responseData.value = '';  // 清空之前的响应数据

    // 持续读取数据流
    while (true) {
      const { value, done } = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, { stream: true });
      
      // SSE 格式中，每个事件以 \n\n 分隔
      const events = buffer.split("\n\n");
      // 保留最后一段不完整的内容
      buffer = events.pop() || '';

      for (const event of events) {
        if (event.startsWith("data: ")) {
          const jsonStr = event.slice(6).trim();
          try {
            const eventData = JSON.parse(jsonStr);
            // 根据后端返回的字段更新响应数据
            if (eventData.assistant_message_id) {
              messages.value.push({
                message_id: eventData.assistant_message_id,
                message_role: 'assistant',
                reasoning_content: '',
                message_content: '',
              });
            }
            if (eventData.reasoning_content) {
              messages.value[messages.value.length - 1].reasoning_content += eventData.reasoning_content;
            }
            if (eventData.content) {
              messages.value[messages.value.length - 1].message_content += eventData.content;
            }
          } catch (error) {
            console.error("JSON 解析失败:", error);
          }
        }
      }
    }
    } catch (error) {
      console.error('请求失败:', error)
    } finally {
      isLoading.value = false
    }
  }

  const fetchChatHistory = async (chatId: string) => {
    try {
      const response = await fetch(`http://localhost:8000/api/v1/chat/chat_history_list_get`, {
        method: 'GET',
        credentials: 'include'
      })
      if (response.ok) {
        chatHistoryList.value = await response.json()
      } else {
        console.error("Failed to fetch chat history")
      }
    } catch (error) {
      console.error("Error fetching chat history:", error)
    }
  }

  const newChat =  async () => {
    curr_chat_id.value = "";
    messages.value = []
  }

  return {
    chatHistoryList,
    curr_chat_id,
    curr_llm_model,
    messages,
    user_message,
    responseData,
    isLoading,
    selectChat,
    sendMessage,
    fetchChatHistory,
    newChat
  }
})
