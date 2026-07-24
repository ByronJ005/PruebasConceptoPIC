<script setup lang="ts">
import { onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from './stores/authStore'

const router = useRouter()
const store = useAuthStore()

function handleGlobalLogout() {
  store.clearAuth()
  router.push('/login')
}

onMounted(() => {
  window.addEventListener('auth-logout', handleGlobalLogout)
})

onUnmounted(() => {
  window.removeEventListener('auth-logout', handleGlobalLogout)
})
</script>

<template>
  <div class="app-layout">
    <router-view />
  </div>
</template>

<style>
/* Global background styles to match premium dark/glassmorphic look */
body {
  margin: 0;
  padding: 0;
  background: radial-gradient(circle at top right, #1a202c 0%, #0d1117 100%);
  min-height: 100vh;
  color: #f7fafc;
}

.app-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
</style>
