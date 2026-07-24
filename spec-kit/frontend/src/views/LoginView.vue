<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/authStore'

const email = ref('')
const password = ref('')
const error = ref('')
const store = useAuthStore()
const router = useRouter()

async function handleLogin() {
  error.value = ''
  try {
    await store.login(email.value, password.value)
    router.push('/dashboard')
  } catch (err: any) {
    error.value = store.error || 'Invalid credentials'
  }
}
</script>

<template>
  <div class="auth-container">
    <div class="auth-card">
      <h2>Welcome Back</h2>
      <p class="subtitle">Transport Tickets Cooperative Portal</p>
      
      <form @submit.prevent="handleLogin" class="auth-form">
        <div class="form-group">
          <label for="email">Email Address</label>
          <input 
            type="email" 
            id="email" 
            v-model="email" 
            required 
            placeholder="you@cooperative.com"
          />
        </div>
        
        <div class="form-group">
          <label for="password">Password</label>
          <input 
            type="password" 
            id="password" 
            v-model="password" 
            required 
            placeholder="••••••••"
          />
        </div>

        <p v-if="error" class="error-msg">{{ error }}</p>

        <button type="submit" :disabled="store.loading" class="btn-primary">
          {{ store.loading ? 'Signing in...' : 'Sign In' }}
        </button>
      </form>
      
      <div class="auth-links">
        <p class="auth-link-text">
          Don't have an account? <router-link to="/register">Register here</router-link>
        </p>
        <p class="auth-link-text">
          Forgot password? <router-link to="/recovery-request">Recover it</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.auth-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
  font-family: 'Outfit', 'Inter', sans-serif;
}

.auth-card {
  background: rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  padding: 40px;
  width: 100%;
  max-width: 420px;
  box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
}

h2 {
  color: #ffffff;
  margin-bottom: 8px;
  font-size: 28px;
  font-weight: 600;
  text-align: center;
}

.subtitle {
  color: #a0aec0;
  text-align: center;
  margin-bottom: 32px;
  font-size: 14px;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

label {
  color: #cbd5e0;
  font-size: 14px;
  font-weight: 500;
}

input {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  padding: 12px 16px;
  color: #ffffff;
  font-size: 16px;
  transition: all 0.3s ease;
}

input:focus {
  outline: none;
  border-color: #63b3ed;
  box-shadow: 0 0 0 3px rgba(99, 179, 237, 0.2);
}

.btn-primary {
  background: linear-gradient(135deg, #3182ce 0%, #319795 100%);
  color: white;
  border: none;
  border-radius: 8px;
  padding: 14px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s, opacity 0.2s;
  margin-top: 10px;
}

.btn-primary:hover {
  transform: translateY(-2px);
  opacity: 0.95;
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.error-msg {
  color: #feb2b2;
  font-size: 14px;
  text-align: center;
}

.auth-links {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-top: 24px;
}

.auth-link-text {
  color: #a0aec0;
  text-align: center;
  font-size: 14px;
  margin: 0;
}

.auth-link-text a {
  color: #63b3ed;
  text-decoration: none;
  font-weight: 500;
}

.auth-link-text a:hover {
  text-decoration: underline;
}
</style>
