<template>
  <div class="sign-in-wrapper">
    <div class="sign-in-icon">
      <img src="@/assets/mohamlab.png" alt="logo" style="height: 44px;">
    </div>
    <div class="sign-in-tabs">
      <div><span>登录</span></div>
    </div>
    <div class="sign-in-tips">
      <span>支持淼翰账号MHID登录</span>
    </div>
    <div class="form-item">
      <div class="form-item-content">
        <div class="input-box" :class="{ 'input-error': errors.user_id }">
          <!-- 前置图标 -->
          <svg class="w-4 h-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024"><path fill="currentColor" d="M512 512a192 192 0 1 0 0-384 192 192 0 0 0 0 384m0 64a256 256 0 1 1 0-512 256 256 0 0 1 0 512m320 320v-96a96 96 0 0 0-96-96H288a96 96 0 0 0-96 96v96a32 32 0 1 1-64 0v-96a160 160 0 0 1 160-160h448a160 160 0 0 1 160 160v96a32 32 0 1 1-64 0"></path></svg>
          <input
            type="text"
            placeholder="请输入账号"
            autocomplete="off"
            v-model="form.user_id"
            @input="clearError('user_id')"
            @blur="clearError('user_id')"
            class="w-full outline-none caret-[#0A59F7]"
          />
        </div>
      </div>
      <div class="form-item-feedback">
        <span class="error-text" style="color:red;">{{ errors.user_id }}</span>
      </div>
    </div>
    <div class="form-item">
      <div class="form-item-content">
        <div class="input-box" :class="{ 'input-error': errors.password }">
          <svg class="w-4 h-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024"><path fill="currentColor" d="M448 456.064V96a32 32 0 0 1 32-32.064L672 64a32 32 0 0 1 0 64H512v128h160a32 32 0 0 1 0 64H512v128a256 256 0 1 1-64 8.064M512 896a192 192 0 1 0 0-384 192 192 0 0 0 0 384"></path></svg>
          <input
            type="password"
            placeholder="请输入密码"
            autocomplete="off"
            v-model="form.password"
            @input="clearError('password')"
            @blur="clearError('password')"
            class="w-full outline-none caret-[#0A59F7]"
          />
        </div>
      </div>
      <div class="form-item-feedback">
        <span class="error-text" style="color:red;">{{ errors.password }}</span>
      </div>
    </div>
    <div class="form-item">
    </div>
    <div role="button">
      <button class="signin-button" @click="handleSignIn">登录</button>
    </div>
    <div class="sign-in-footer">
      <div role="button">
        <button class="footer-button" style="color:gray;" disabled>忘记密码</button>
      </div>
      <div role="button">
        <button class="footer-button sign-btn" @click="goToSignUp">立即注册</button>
      </div>
    </div>
    <div class="divider">

    </div>
    <div class="other">
    </div>
    
  </div>
</template>

<script setup>
import { ref } from 'vue'
import 'boxicons'
import { useRouter } from 'vue-router';
import axios from 'axios';
const router = useRouter();

// 当输入框获取焦点时，清除该项的错误提示
const clearError = (field) => {
  errors.value[field] = ''
}

function goToSignUp() {
  router.push('/sign_up');
}

// 用来控制登录和注册的状态
const isLogin = ref(true);

// 表单数据
const form = ref({
  user_id: '',
  password: ''
});

// 错误信息对象，每个字段对应一个错误提示
const errors = ref({
  user_id: '',
  password: ''
})

const valSignInForm = () => {
  let valid = true
  // 清空之前的错误
  errors.value = { user_id: '', password: '' }

  const newmhid = form.value.user_id.trim()
  const minidLen = 5
  const maxidLen = 18

  if (!newmhid) {
    errors.value.user_id = '请输入账号'
    valid = false
  } else if (newmhid.length < minidLen || newmhid.length > maxidLen) {
    errors.value.user_id = `账号长度在 ${minidLen} 到 ${maxidLen} 个字符之间`
    valid = false
  } else if (!/^[a-z]/.test(newmhid)) {
    errors.value.user_id = '账号以小写字母开头'
    valid = false
  } else if (!/^[a-z0-9]+$/.test(newmhid)) {
    errors.value.user_id = '账号只包含小写字母和数字'
    valid = false
  }

  // 密码校验
  const minpwLen = 6
  const maxpwLen = 18
  if (!form.value.password) {
    errors.value.password = '请输入密码'
    valid = false
  } else if (form.value.password.length < minpwLen || form.value.password.length > maxpwLen) {
    errors.value.password = `密码长度在 ${minpwLen} 到 ${maxpwLen} 个字符之间`
    valid = false
  } else if (!/^[a-zA-Z0-9]+$/.test(form.value.password)) {
    errors.value.password = '密码只可能包含大小写字母和数字'
    valid = false
  }

  return valid
}

// 提交表单
const handleSignIn = async () => {
  // 先进行前端表单验证
  if (!valSignInForm()) return

  // 构造要发送的数据
  const data = {
    user_id: form.value.user_id,
    password: form.value.password
  }

  try {
    // 发送 POST 请求到后端接口
    const response = await axios.post(
      'http://localhost:8000/api/v1/user/signin',
      data, 
      {
        headers: { 'Content-Type': 'application/json' },
        withCredentials: true  // 关键：允许携带 Cookie（Session 认证）
    })
    alert(response.data.message)
    if (response.data.status === "True") {
      // 如果登录成功，可以调用获取用户信息接口确认 Session 状态，也可以直接跳转
      const userResponse = await axios.get('http://localhost:8000/api/v1/user/me', {
        withCredentials: true  // 确保 Cookie 被携带
      })
      console.log(data.user_id)
      localStorage.setItem('authed_user_id', data.user_id)
      console.log(localStorage.getItem('authed_user_id'))
      router.push('/')
    }
  } catch (error) {
    alert('请求失败：' + (error.response?.data?.message || error.message))
  }
}
</script>

<style scoped>
.sign-in-wrapper {
  width:300px;
  padding-top: 48px;
}
.sign-in-icon {
  justify-content: center;
  align-items: center;
  margin: auto auto 24px;
  line-height: 0;
  display: flex;
}
.sign-in-tabs {
  font-weight: 600;
  color: rgb(#BBB);
  justify-content: center;
  margin: 0 auto 20px;
  display: flex;
}
.sign-in-tips {
  text-align: left;
  font-size: 13px;
  line-height: 23px;
  color: rgb(#BBB);
  margin-bottom: 4px;
}
.signup-form {
  display: grid;
  grid-template-rows: repeat(7, 1fr);
}
.form-item-feedback {
  box-sizing: border-box;
  min-height: 21px;
  transition: color 0.2s cubic-bezier(.4,0,.2,1);
  padding: 2px 0;
  font-size: 12px;
  line-height: 17px;
}
.sign-in-footer {
  justify-content: space-between;
  margin-top: 12px;
  display: flex;
}

.input-icon {
  margin-right: 8px;
  width: 18px;
  height: 18px;
}
.input-box {
  width: 100%;
  height: 42px;
  padding-left: 10px;
  padding-right: 10px;
  border-radius: 10px;
  display: flex;
  justify-content: center;
  align-items: center;
  box-shadow: inset 0 0 0 1px rgb(229, 229, 229, 1);
}
.input-box.input-error {
  box-shadow: inset 0 0 0 2px rgb(255, 0, 0);
}
.input-box:focus-within {
  box-shadow: inset 0 0 0 2px rgb(10, 89, 247);
}

/* 错误提示文本，显示为红色 */
.error-message {
  color: red;
  font-size: 12px;
}
/* 登录按钮 */
.signin-button {
  width: 100%;
  padding: 10px;
  background-color: rgba(77,107,254,1);
  border-radius: 10px;
  border: none;
  color: white;
  cursor: pointer;
}
.footer-button {
  border: none;
  color: rgba(77,107,254,1);
}
/* 超链接 */
a {
  text-decoration: none;
  color: #0a59f7cc;
}
a:hover,
a:focus {
  color: #0a59f7ff;
}

</style>
