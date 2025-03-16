import { createRouter, createWebHistory } from 'vue-router'

import ChatView from '@/views/chat/ChatView.vue'
import ConvChatView from '@/views/chat/ConvChatView.vue'
import TestView from '@/views/test/TestView.vue'
import SignIn from '@/pages/user/SignInPage.vue'
import SignUp from '@/pages/user/SignUpPage.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'chat',
      meta: { isAuth: true },
      component: ChatView,
      children: [
        {
          path: '/chat/:chat_id', // 动态路由，匹配不同的聊天记录
          name: 'conv_chat', // 聊天记录页面
          component: ConvChatView,
        }
      ]
    },
    {
      path: '/sign_in',
      name: 'signin',
      component: SignIn,
    },
    {
      path: '/sign_up',
      name: 'signup',
      component: SignUp,
    },
    {
      path: '/test',
      name: 'test',
      component: TestView,
    },
  ]
})

function isAuth() {
  // 这里可以根据实际情况判断，比如检查 authed_user_id 是否存在
  return !!localStorage.getItem('authed_user_id')
}

router.beforeEach((to, from, next) => {
  // to 参数代表当前导航去往的路由对象，from 参数代表当前导航离开的路由对象，next用于确定路由是否继续或重定向到其他页面。 如果目标路由需要验证，并且用户未登录，则跳转到登录页
  if (to.meta.isAuth && !isAuth()) {
    next('/sign_in')
  } else {
    next()
  }
})

export default router
