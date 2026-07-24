import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/authStore'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import RecoveryRequestView from '../views/RecoveryRequestView.vue'
import PasswordResetView from '../views/PasswordResetView.vue'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: LoginView,
      meta: { guestOnly: true }
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView,
      meta: { guestOnly: true }
    },
    {
      path: '/recovery-request',
      name: 'recovery-request',
      component: RecoveryRequestView,
      meta: { guestOnly: true }
    },
    {
      path: '/password-reset',
      name: 'password-reset',
      component: PasswordResetView,
      meta: { guestOnly: true }
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: HomeView,
      meta: { requiresAuth: true }
    },
    {
      path: '/',
      redirect: '/dashboard'
    }
  ],
})

// Navigation Guard
router.beforeEach((to, from, next) => {
  const store = useAuthStore()
  store.initializeAuth()

  if (to.meta.requiresAuth && !store.isAuthenticated) {
    next('/login')
  } else if (to.meta.guestOnly && store.isAuthenticated) {
    next('/dashboard')
  } else {
    next()
  }
})

export default router
