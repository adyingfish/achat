<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'

import { useChatStore } from '@/store/chatStore'
const chatStore = useChatStore()

const textarea = ref<HTMLTextAreaElement | null>(null);

function adjustHeight() {
  if (textarea.value) {
    // 重置高度以确保 scrollHeight 计算准确
    textarea.value.style.height = 'auto';
    // 设置 textarea 高度为内容的 scrollHeight
    textarea.value.style.height = textarea.value.scrollHeight + 'px';
  }
}
// 初始化时也执行一次调整，确保初始显示正确
onMounted(() => {
  nextTick(() => {
    adjustHeight();
  });
});

// 发送消息请求后端接口
// async function sendMessage() {
//   try {
//     const response = await fetch('http://127.0.0.1:8000/api/v1/chat/chat', {
//       method: 'POST',
//       headers: {
//         'Content-Type': 'application/json'
//       },
//       body: JSON.stringify({ message: userInput.value })
//     });
//     if (!response.ok) {
//       throw new Error(`网络错误: ${response.statusText}`);
//     }
//     const data = await response.json();
//     console.log("后端返回的响应:", data.response);
//     // 清空输入框
//     userInput.value = '';
//     // 调整输入框高度
//     adjustHeight();
//     // 根据需要更新界面，例如显示回答内容等
//   } catch (error) {
//     console.error("请求失败:", error);
//   }
// }
</script>

<template>
  <div class="max-w-[800px] mx-auto" id="chat-footer">
    <div class=" bg-base-200 rounded-3xl p-[10px]">
      <div id="files-upload"></div>
      <div class="flex flex-col justify-start content-start">
        <div class="w-full min-h-12 max-h-96 overflow-y-auto">
          <textarea 
            class="w-full border-none shadow-none outline-none resize-none" 
            placeholder="询问任何问题"
            ref="textarea"
            v-model="chatStore.user_message"
            @input="adjustHeight"
          >
          </textarea>
        </div>
        <div class="flex">
          <div class="flex justify-start w-full">
            <button class="btn rounded-3xl btn-disabled">
              <svg class="w-5 h-5 fill-base-content" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg"><path d="M480 64C214.848 64 0 278.848 0 544S214.848 1024 480 1024 960 809.152 960 544 745.152 64 480 64zM893.696 512l-126.784 0c-5.504-138.56-45.952-260.992-107.136-342.72C790.144 231.936 881.984 360.64 893.696 512zM702.4 512 512 512 512 132.736C614.848 160.128 694.336 317.312 702.4 512zM448 132.736 448 512 257.6 512C265.664 317.312 345.152 160.128 448 132.736zM300.288 169.28C239.04 251.008 198.656 373.44 193.152 512L66.304 512C78.016 360.64 169.856 231.936 300.288 169.28zM66.304 576l126.784 0c5.504 138.56 45.952 260.992 107.136 342.72C169.856 856.064 78.016 727.36 66.304 576zM257.6 576 448 576l0 379.264C345.152 927.872 265.664 770.688 257.6 576zM512 955.264 512 576l190.4 0C694.336 770.688 614.848 927.872 512 955.264zM659.712 918.72c61.248-81.728 101.632-204.16 107.136-342.72l126.784 0C881.984 727.36 790.144 856.064 659.712 918.72z"></path></svg>
              网络搜索
            </button>
          </div>
          <div class="flex justify-end w-full">
            <button @click="chatStore.sendMessage" class="btn btn-circle bg-base-content">
              <svg class="w-6 h-6 fill-base-100 stroke-base-100 stroke-10" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024">
                <path d="M572.235 205.282v600.365a30.118 30.118 0 1 1-60.235 0V205.282L292.382 438.633a28.913 28.913 0 0 1-42.646 0 33.43 33.43 0 0 1 0-45.236l271.058-288.045a28.913 28.913 0 0 1 42.647 0L834.5 393.397a33.43 33.43 0 0 1 0 45.176 28.913 28.913 0 0 1-42.647 0l-219.618-233.23z"></path></svg>
            </button>
          </div>
        </div>
        
      </div>
    </div>
    
<!-- 
    <div class="input-container">
      <div class="input-container-inner">
        <div class="chat-btn-left">
          <el-button :icon="UploadFilled" @click="onSearchClick" circle />
        </div>
        <div class="input-field-container">
          <div class="uploaded-files">

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

    <div class="input-container">
      <div class="input-container-inner">
        <div class="chat-btn-left">
          <el-button :icon="UploadFilled" @click="onSearchClick" circle />
        </div>
        <div class="input-field-container">
          <div class="uploaded-files">
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
     -->
    <div class="text-center p-2 flex items-center justify-center whitespace-nowrap">
      <span class="text-sm">内容由AI生成，请仔细甄别 | Developed by adyingfish |&nbsp;</span>
      <svg class="w-5 h-5 fill-base-content" aria-label="GitHub logo" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12,2A10,10 0 0,0 2,12C2,16.42 4.87,20.17 8.84,21.5C9.34,21.58 9.5,21.27 9.5,21C9.5,20.77 9.5,20.14 9.5,19.31C6.73,19.91 6.14,17.97 6.14,17.97C5.68,16.81 5.03,16.5 5.03,16.5C4.12,15.88 5.1,15.9 5.1,15.9C6.1,15.97 6.63,16.93 6.63,16.93C7.5,18.45 8.97,18 9.54,17.76C9.63,17.11 9.89,16.67 10.17,16.42C7.95,16.17 5.62,15.31 5.62,11.5C5.62,10.39 6,9.5 6.65,8.79C6.55,8.54 6.2,7.5 6.75,6.15C6.75,6.15 7.59,5.88 9.5,7.17C10.29,6.95 11.15,6.84 12,6.84C12.85,6.84 13.71,6.95 14.5,7.17C16.41,5.88 17.25,6.15 17.25,6.15C17.8,7.5 17.45,8.54 17.35,8.79C18,9.5 18.38,10.39 18.38,11.5C18.38,15.32 16.04,16.16 13.81,16.41C14.17,16.72 14.5,17.33 14.5,18.26C14.5,19.6 14.5,20.68 14.5,21C14.5,21.27 14.66,21.59 15.17,21.5C19.14,20.16 22,16.42 22,12A10,10 0 0,0 12,2Z"></path></svg>
      <a class="text-sm" href="https://github.com/adyingfish/achat" target="_blank">&nbsp;github.com/adyingfish/achat</a>
    </div>
  </div>
</template>

<style lang="css">
.btn-disabled svg {
  fill: #ccc;
}
</style>