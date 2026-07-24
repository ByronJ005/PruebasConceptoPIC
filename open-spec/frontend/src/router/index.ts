import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/useAuthStore'

const Home = () => import('../pages/home.vue')
const Login = () => import('../pages/auth/login.vue')
const Register = () => import('../pages/auth/register.vue')
const ForgotPassword = () => import('../pages/auth/forgot-password.vue')
const ResetPassword = () => import('../pages/auth/reset-password.vue')

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home,
      meta: { requiresAuth: true }
    },
    {
      path: '/login',
      name: 'login',
      component: Login,
      meta: { guestOnly: true }
    },
    {
      path: '/register',
      name: 'register',
      component: Register,
      meta: { guestOnly: true }
    },
    {
      path: '/forgot-password',
      name: 'forgot-password',
      component: ForgotPassword,
      meta: { guestOnly: true }
    },
    {
      path: '/reset-password',
      name: 'reset-password',
      component: ResetPassword,
      meta: { guestOnly: true }
    }
  ],
})

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    try {
      await authStore.refreshToken()
      next()
    } catch {
      next({ name: 'login' })
    }
  } else if (to.meta.guestOnly && authStore.isAuthenticated) {
    next({ name: 'home' })
  } else {
    next()
  }
})

export default router
