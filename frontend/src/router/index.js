import { createRouter, createWebHistory } from 'vue-router'
import GameLobby from '@/components/GameLobby.vue'
import AuthCallback from '@/components/AuthCallback.vue'
import DebugPage from '@/components/DebugPage.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: GameLobby
  },
  {
    path: '/auth/google',
    name: 'google-auth',
    component: AuthCallback
  },
  {
    path: '/debug',
    name: 'debug',
    component: DebugPage
  },
  {
    path: '/auth/callback/:provider',
    name: 'auth-callback',
    component: AuthCallback
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router