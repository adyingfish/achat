<script setup lang="ts">
import { ref, computed, onMounted, watchEffect } from 'vue'
import { useSidebarStore } from '@/store/sidebar'
import { ElMessage } from 'element-plus'
import { UploadFilled, Top, Close } from '@element-plus/icons-vue'
import MarkdownIt from 'markdown-it'
import 'github-markdown-css/github-markdown-light.css'

import HandleBtnMain from '@/components/sidebar/HandleBtnMain.vue'
import ModelSelect from '@/components/sidebar/ModelSelect.vue'
const sidebarStore = useSidebarStore();
const isSidebarVisible = computed(() => sidebarStore.isSidebarVisible); // 监听侧边栏状态



const md = new MarkdownIt()

interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  files?: File[];
}

interface UploadedFile extends File {
  type: string;
  preview?: string;
}
const allowedFileTypes = [
  'application/json'// 这就是 .txt 文件的 MIME 类型
];
const userInput = ref<string>('')
const chatList = ref<ChatMessage[]>([])
const uploadedFiles = ref<UploadedFile[]>([]); // 存储上传的文件

const div1Height = ref<string>('0px');
const div2 = ref<HTMLElement | null>(null);

const onSearchClick = (): void => {
  const fileInput = document.createElement('input');
  fileInput.type = 'file';
  fileInput.multiple = true;
  fileInput.onchange = (event: Event) => {
    const target = event.target as HTMLInputElement;
    if (target.files) {
      const files = Array.from(target.files) as UploadedFile[];
      const validFiles: UploadedFile[] = [];
      const invalidFiles: string[] = [];

      files.forEach(file => {
        if (allowedFileTypes.includes(file.type)) {
          if (file.type.startsWith('image/')) {
            const reader = new FileReader();
            reader.onload = (e) => {
              file.preview = e.target?.result as string;
            };
            reader.readAsDataURL(file);
          }
          validFiles.push(file);
        } else {
          invalidFiles.push(file.name);
        }
      });
      if (invalidFiles.length > 0) {
        ElMessage.error(`该文件格式暂不受支持: ${invalidFiles.join(', ')}`);
      }
      if (validFiles.length > 0) {
        uploadedFiles.value.push(...validFiles);
      }
    }
  };
  fileInput.click();
}

const getFileIcon = (file: UploadedFile): string => {
  if (file.type.startsWith('image/')) {
    return 'image-icon';
  } else if (file.type.startsWith('video/')) {
    return 'video-icon';
  } else if (file.type.startsWith('audio/')) {
    return 'audio-icon';
  } else if (file.type === 'application/pdf') {
    return 'pdf-icon';
  } else if (file.type.includes('word')) {
    return 'word-icon';
  } else if (file.type.includes('spreadsheet') || file.type.includes('excel')) {
    return 'excel-icon';
  } else {
    return 'file-icon';
  }
}

const removeFile = (index: number): void => {
  uploadedFiles.value.splice(index, 1);
}

const selectvalue = ref<string>('Option1')

const options = [
  { selectvalue: 'Option1', selectlabel: '田小猪' },
  { selectvalue: 'Option2', selectlabel: 'Option2' },
  { selectvalue: 'Option3', selectlabel: 'Option3' },
  { selectvalue: 'Option4', selectlabel: 'Option4' },
  { selectvalue: 'Option5', selectlabel: 'Option5' },
]

const sendHumanMessage = async (): Promise<void> => {
  if (userInput.value.trim() === '' && uploadedFiles.value.length === 0) return

  const inputText = userInput.value
  const files = uploadedFiles.value
  userInput.value = ''
  uploadedFiles.value = []

  chatList.value.push({ role: 'user', content: inputText, files })

  const assistantMessage: ChatMessage = { role: 'assistant', content: '' }
  chatList.value.push(assistantMessage)

  try {
    const response = await fetch('http://localhost:8000/api/llm/llm_server/chat_stream', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ user_input: inputText })
    })

    if (!response.body) throw new Error('No response body')

    const reader = response.body.getReader()
    const decoder = new TextDecoder()

    let AIMessage = ''
    
    while (true) {
      const { done, value } = await reader.read()
      if (done) break

      const chunk = decoder.decode(value, { stream: true })
      AIMessage += chunk
      chatList.value[chatList.value.length - 1].content = AIMessage
    }
  } catch (error) {
    console.error('请求失败:', error)
    chatList.value[chatList.value.length - 1].content = '对不起，发生了错误。'
  }
}

const parseMarkdown = (text: string | undefined): string => md.render(text || '')

onMounted((): void => {
  watchEffect(() => {
    if (div2.value) {
      const div2Height = div2.value.offsetHeight;
      div1Height.value = `calc(100vh - ${div2}px)`;
    }
  });
});
</script>

<template>
<div class="chat-main-container">
  <div ref="div2" class="chat-footer">
    <div class="input-container">
      <div class="input-container-inner">
        <div class="chat-btn-left">
          <el-button :icon="UploadFilled" @click="onSearchClick" circle />
        </div>
        <div class="input-field-container">
          <div class="uploaded-files">
            <!-- 单独文件气泡 -->
            <div v-for="(file, index) in uploadedFiles" :key="file.name" class="file-bubble">
              <img v-if="file.type.startsWith('image/')" :src="file.preview" class="file-preview" />
              <span v-else :class="getFileIcon(file)" class="file-icon"></span>
              <span class="file-name">{{ file.name }}</span>
              <el-button :icon="Close" @click="removeFile(index)"  circle size="mini" />
            </div>
          </div>
          <div>
            <el-input v-model="userInput" class="inputz" type="textarea" :autosize="{ minRows: 1, maxRows: 10 }" resize="none" placeholder="请输入内容" @keydown.enter.stop.prevent="sendHumanMessage"></el-input>
          </div>
        </div>
        <div class="chat-btn-right">
          <el-button :icon="Top" @click="sendHumanMessage" circle />
        </div>
      </div>
    </div>
    <div class="text-prompt">
      <span>以上内容均由AI生成,仅供参考和借鉴</span>
    </div>
  </div>
</div>
</template>

<style scoped>
.chat-main-container {
  height: 100vh;
  width: 100%;
  display: flex;
  flex-direction: column;
  position: relative;
}
.chat-container {
  width: 100%;
  padding-bottom: 2.25rem;
  overflow-y: scroll;
  flex: 1 1 0;
}
.chat-header {
  width: 100%;
  height: 3.5rem;
  padding: .75rem;
  align-items: center;
  justify-content: flex-start;
  display: flex;
  margin-bottom: .375rem;
  background-color: #ffffff;
  z-index: 10;
  position: sticky;
  top: 0;
}
.action-container{
  height: 2rem;
  padding: .75rem;
  display: flex;
}
:deep(.el-select__wrapper) {
  border: none; /* 取消边框 */
  box-shadow: none; /* 移除阴影 */ 
  color: black; /* 设置字体颜色为黑色 */
}
:deep(.el-select__wrapper.is-hovering:not(.is-focused) ) {
  border: none; /* 取消边框 */
  box-shadow: none; /* 移除阴影 */ 
  color: black; /* 设置字体颜色为黑色 */
}
:deep(.el-select__wrapper.is-hovering ) {
  border: none; /* 取消边框 */
  box-shadow: none; /* 移除阴影 */ 
  color: black; /* 设置字体颜色为黑色 */
}
:deep(.el-select__wrapper.is-focused) {
  border: none; /* 取消边框 */
  box-shadow: none; /* 移除阴影 */
  color: black; /* 设置字体颜色为黑色 */
}
.setting {
  margin-left: auto;
  display: flex;
  flex-direction: row;
}
.chat-header .avatar img {
  width: 40px;
  height: 40px;
  border-radius: 50%;
}
.content {
  max-width: 100%;
  padding: 20px;
  justify-content: center;
  display: flex;
}
.chat-content {
  min-width: 180px;
  width: 720px;
  display: flex;
  flex-direction: column;
  position: relative;
}
.message-item {
  display: flex;
  flex-direction: column;
}
.message-item .avatar {
  margin-right: 10px;
  display: flex;
  align-items: center;
}
.message-item .avatar img {
  width: 40px;
  height: 40px;
  border-radius: 50%;
}
.markdown-body {
  box-sizing: border-box;
  min-width: 200px;
  max-width: 980px;
  margin: 0 auto;
  padding: 45px;
}
@media (max-width: 767px) {
  .markdown-body {
    padding: 15px;
  }
}
.chat-footer {
  width: 100%;
  padding-top: 0;
  background-color: #fff;
  align-items: center;
  display: flex;
  flex-direction: column;
  z-index: 10;
  position: sticky;
  bottom: 0;
}
.input-container {
  min-width: 180px;
  width: 720px;
  padding: 0.75rem;
  background-color: #ffffff;
}
.input-container-inner {
  display: flex;
  flex-direction: row;
  align-items: center;
  position: relative;
}
.input-field-container {
  flex: 1;
  margin-left: 2.5rem;
  margin-right: 2.5rem;
}
.file-bubble {
  display: inline-flex;
  align-items: center;
  background-color: #f0f0f0;
  border-radius: 12px;
  padding: 0.25rem 0.5rem;
  margin-bottom: 0.375rem;
  margin-right: 0.375rem;
  font-size: 0.875rem;
}
.file-bubble span {
  margin-right: 0.5rem;
}
.chat-btn-left {
  margin-right: .375rem;
  position: absolute; /* 绝对定位 */
  left: 0; /* 靠左边对齐 */
  bottom: 0;

}
.chat-btn-right {
  margin-left: .375rem;
  position: absolute; /* 绝对定位 */
  right: 0; /* 靠右边对齐 */
  bottom: 0;
}
/* 输入框 */
:deep(.el-textarea__inner) {
  font-size: 1rem;
  background-color: #F7F7F7;
  border: none; /* 移除外边框 */
  box-shadow: none; /* 移除阴影 */
  outline: none; /* 移除输入框聚焦时的默认外边框 */
  padding: .5rem .75rem;
  color: black;
}
:deep(.el-textarea__inner:hover) {
  font-size: 1rem;
  background-color: #F7F7F7;
  border: none; /* 移除外边框 */
  box-shadow: none; /* 移除阴影 */
  outline: none; /* 移除输入框聚焦时的默认外边框 */
  padding: .5rem .75rem;
}
:deep(.el-textarea__inner:focus) {
  font-size: 1rem;
  background-color: #F7F7F7;
  border: none; /* 移除外边框 */
  box-shadow: none; /* 移除阴影 */
  outline: none; /* 移除输入框聚焦时的默认外边框 */
  padding: .5rem .75rem;
}
.text-prompt {
  text-align: center;
  font-size: 12px;
  color: #999;
  margin-top: 0.375rem;
  margin-bottom: 0.375rem;
}
.file-preview {
  width: 50px;
  height: 50px;
  object-fit: cover;
  margin-right: 10px;
}
.file-icon {
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 10px;
  font-size: 24px;
}
/* 为不同类型的文件添加图标 */
.image-icon::before { content: '🖼️'; }
.video-icon::before { content: '🎥'; }
.audio-icon::before { content: '🎵'; }
.pdf-icon::before { content: '📄'; }
.word-icon::before { content: '📝'; }
.excel-icon::before { content: '📊'; }
.file-icon::before { content: '📁'; }
</style>
