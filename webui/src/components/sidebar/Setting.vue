<template>
    <div class="dropdown dropdown-top border-none shadow-none w-full rounded-xl p-2">
      <div tabindex="0" role="button" class="btn border-none shadow-none w-full h-14 rounded-xl justify-start">
        <div class="w-[32px] h-[32px]">
          <img class="w-[32px] h-[32px] rounded-full" src="@/assets/aipic.png" alt="设置">
        </div>
        设置
      </div>
      <div tabindex="0" class="dropdown-content w-3/4">
        <button class="btn btn-block flex border-none justify-start">
          &nbsp &nbsp &nbsp &nbsp User ID
        </button>
        <button class="btn btn-block flex border-none justify-start">
          <svg class="w-5 h-5 ml-2 fill-base-content" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024"><path fill="currentColor" d="M764.416 254.72a351.68 351.68 0 0 1 86.336 149.184H960v192.064H850.752a351.68 351.68 0 0 1-86.336 149.312l54.72 94.72-166.272 96-54.592-94.72a352.64 352.64 0 0 1-172.48 0L371.136 936l-166.272-96 54.72-94.72a351.68 351.68 0 0 1-86.336-149.312H64v-192h109.248a351.68 351.68 0 0 1 86.336-149.312L204.8 160l166.208-96h.192l54.656 94.592a352.64 352.64 0 0 1 172.48 0L652.8 64h.128L819.2 160l-54.72 94.72zM704 499.968a192 192 0 1 0-384 0 192 192 0 0 0 384 0"></path></svg>
          &nbsp 暂未开放
        </button>
        <button class="btn btn-block flex border-none justify-start">
          <svg class="w-5 h-5 ml-2 fill-base-content" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024"><path fill="currentColor" d="M764.416 254.72a351.68 351.68 0 0 1 86.336 149.184H960v192.064H850.752a351.68 351.68 0 0 1-86.336 149.312l54.72 94.72-166.272 96-54.592-94.72a352.64 352.64 0 0 1-172.48 0L371.136 936l-166.272-96 54.72-94.72a351.68 351.68 0 0 1-86.336-149.312H64v-192h109.248a351.68 351.68 0 0 1 86.336-149.312L204.8 160l166.208-96h.192l54.656 94.592a352.64 352.64 0 0 1 172.48 0L652.8 64h.128L819.2 160l-54.72 94.72zM704 499.968a192 192 0 1 0-384 0 192 192 0 0 0 384 0"></path></svg>
          &nbsp 暂未开放
        </button>
        <button class="btn btn-block flex border-none justify-start">
          <svg class="w-5 h-5 ml-2 fill-base-content" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024"><path fill="currentColor" d="M764.416 254.72a351.68 351.68 0 0 1 86.336 149.184H960v192.064H850.752a351.68 351.68 0 0 1-86.336 149.312l54.72 94.72-166.272 96-54.592-94.72a352.64 352.64 0 0 1-172.48 0L371.136 936l-166.272-96 54.72-94.72a351.68 351.68 0 0 1-86.336-149.312H64v-192h109.248a351.68 351.68 0 0 1 86.336-149.312L204.8 160l166.208-96h.192l54.656 94.592a352.64 352.64 0 0 1 172.48 0L652.8 64h.128L819.2 160l-54.72 94.72zM704 499.968a192 192 0 1 0-384 0 192 192 0 0 0 384 0"></path></svg>
          &nbsp 暂未开放
        </button>
        <button  @click="handleSignOut"  class="btn btn-block flex border-none justify-start">
          <svg class="w-5 h-5 ml-2 fill-base-content" t="1740728564703" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="1498"><path d="M192 192h512v-64H128v768h576v-64H192z" p-id="1499"></path><path d="M738 265l-49.3 49.2L850.5 476H320v72h530.5L688.7 709.8 738 759l247-247z" p-id="1500"></path></svg>
          &nbsp 退出登录
        </button>
      </div>
    </div>
</template>

<script setup>
import { useRouter } from 'vue-router';
const router = useRouter();
const handleSignOut = async () => {
  try {
    // 使用 Fetch API 发送请求
    const response = await fetch('http://localhost:8000/api/v1/user/signout', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',    // 明确指定内容类型
      },
    });

    // 检查 HTTP 状态码
    if (!response.ok) {
      throw new Error(`退出登录失败: HTTP ${response.status}`);
    }
    // 清除本地存储
    // localStorage.removeItem('token');
    // localStorage.removeItem('userInfo');
    // 跳转登录页
    router.push('/sign_in');
  } catch (error) {
    console.error('退出登录异常:', error);
    // 强制清除所有认证信息
    localStorage.clear();
    // 跳转登录页
    router.push('/sign_in');
  }
};

</script>

<style scoped>
</style>
