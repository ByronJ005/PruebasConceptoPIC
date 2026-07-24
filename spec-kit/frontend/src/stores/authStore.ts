import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import {
  registerApi,
  loginApi,
  logoutApi,
  passwordRecoveryApi,
  passwordResetApi
} from '../services/authApi'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<{ email: string; id: string } | null>(null)
  const accessToken = ref<string | null>(null)
  const loading = ref<boolean>(false)
  const error = ref<string | null>(null)

  const isAuthenticated = computed(() => accessToken.value !== null)

  function setAuth(token: string, email: string) {
    accessToken.value = token
    user.value = { email, id: '' }
    localStorage.setItem('access_token', token)
    localStorage.setItem('user', JSON.stringify({ email }))
  }

  function clearAuth() {
    accessToken.value = null
    user.value = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('user')
  }

  function initializeAuth() {
    const token = localStorage.getItem('access_token')
    const storedUser = localStorage.getItem('user')
    if (token && storedUser) {
      accessToken.value = token
      try {
        user.value = JSON.parse(storedUser)
      } catch {
        clearAuth()
      }
    }
  }

  async function register(email: string, password: string) {
    loading.value = true
    error.value = null
    try {
      const response = await registerApi(email, password)
      loading.value = false
      return response
    } catch (err: any) {
      loading.value = false
      error.value = err.response?.data?.detail || 'An error occurred during registration.'
      throw err
    }
  }

  async function login(email: string, password: string) {
    loading.value = true
    error.value = null
    try {
      const response = await loginApi(email, password)
      setAuth(response.access_token, email)
      loading.value = false
      return response
    } catch (err: any) {
      loading.value = false
      error.value = err.response?.data?.detail || 'Invalid email or password.'
      throw err
    }
  }

  async function logout() {
    loading.value = true
    try {
      await logoutApi()
    } catch (err) {
      // Proceed to clear auth anyway
    } finally {
      clearAuth()
      loading.value = false
    }
  }

  async function requestPasswordRecovery(email: string) {
    loading.value = true
    error.value = null
    try {
      const response = await passwordRecoveryApi(email)
      loading.value = false
      return response
    } catch (err: any) {
      loading.value = false
      error.value = err.response?.data?.detail || 'Failed to request password recovery.'
      throw err
    }
  }

  async function resetPassword(token: string, newPassword: string) {
    loading.value = true
    error.value = null
    try {
      const response = await passwordResetApi(token, newPassword)
      loading.value = false
      return response
    } catch (err: any) {
      loading.value = false
      error.value = err.response?.data?.detail || 'Failed to reset password.'
      throw err
    }
  }

  return {
    user,
    accessToken,
    loading,
    error,
    isAuthenticated,
    setAuth,
    clearAuth,
    initializeAuth,
    register,
    login,
    logout,
    requestPasswordRecovery,
    resetPassword,
  }
})
