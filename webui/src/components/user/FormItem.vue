<template>
  <div class="auth-form">
    <h2>{{ isLogin ? '登录' : '注册' }}</h2>
    <form @submit.prevent="handleSubmit">
      <div class="form-item">
        <label for="username">用户名</label>
        <input v-model="form.username" type="text" id="username" placeholder="请输入用户名" required />
      </div>
      <div class="form-item">
        <label for="email" v-if="!isLogin">邮箱</label>
        <input
          v-if="!isLogin"
          v-model="form.email"
          type="email"
          id="email"
          placeholder="请输入邮箱"
          required
        />
      </div>
      <div class="form-item">
        <label for="password">密码</label>
        <input v-model="form.password" type="password" id="password" placeholder="请输入密码" required />
      </div>
      <div class="form-item" v-if="!isLogin">
        <label for="confirmPassword">确认密码</label>
        <input
          v-model="form.confirmPassword"
          type="password"
          id="confirmPassword"
          placeholder="请输入确认密码"
          required
        />
      </div>
      <button type="submit">{{ isLogin ? '登录' : '注册' }}</button>
      <div class="toggle-link">
        <span @click="toggleForm">{{ isLogin ? '没有账号？注册' : '已有账号？登录' }}</span>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';

// 用来控制登录和注册的状态
const isLogin = ref(true);

// 表单数据
const form = ref({
  username: '',
  email: '',
  password: '',
  confirmPassword: '',
});

// 切换登录和注册表单
const toggleForm = () => {
  isLogin.value = !isLogin.value;
  // 清空表单
  form.value = { username: '', email: '', password: '', confirmPassword: '' };
};

// 提交表单的方法
const handleSubmit = () => {
  if (!isLogin.value && form.value.password !== form.value.confirmPassword) {
    alert('密码和确认密码不一致');
    return;
  }
  // 提交登录或注册逻辑
  alert(isLogin.value ? '登录成功' : '注册成功');
};
</script>

<style scoped>
.auth-form {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
}

.form-item {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
}

input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button {
  width: 100%;
  padding: 10px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #45a049;
}

.toggle-link {
  text-align: center;
  margin-top: 15px;
}

.toggle-link span {
  color: #007bff;
  cursor: pointer;
}
</style>
