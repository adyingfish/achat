<script setup lang="ts">
import SignInComponent from '@/components/SignIn.vue'
import FooterComponent from '@/components/Footer.vue'
</script>

<template>
  <div class="signin-container">
    <div class="signin-main">
      <SignInComponent/>
    </div>
    <div class="signin-footer">
      <FooterComponent/>
    </div>
  </div>

</template>

<style scoped>
.signin-container {
  box-sizing: border-box;
  align-items: stretch;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
.signin-main {
  display: flex;
  flex-direction: column;
  flex-grow: 1;
  flex-shrink: 0;
  justify-content: safe center;
  align-items: safe center;
}
.signin-footer {
  padding: 32px 18px 20px;
  justify-content: center;
  display: flex
}
</style>
