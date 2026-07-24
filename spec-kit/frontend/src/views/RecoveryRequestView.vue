<script setup lang="ts">
import { ref } from 'vue'
import { useAuthStore } from '../stores/authStore'

const email = ref('')
const error = ref('')
const success = ref('')
const store = useAuthStore()

async function handleRecovery() {
  error.value = ''
  success.value = ''
  try {
    await store.requestPasswordRecovery(email.value)
    success.value = 'If the email is registered, a password recovery link has been sent!'
  } catch (err: any) {
    error.value = store.error || 'Failed to request password recovery.'
  }
}
</script>

<template>
  <div class="auth-container">
    <div class="auth-card">
      <h2>Reset Password</h2>
      <p class="subtitle">Enter your email and we will send you a reset link</p>
      
      <form @submit.prevent="handleRecovery" class="auth-form">
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

        <p v-if="error" class="error-msg">{{ error }}</p>
        <p v-if="success" class="success-msg">{{ success }}</p>

        <button type="submit" :disabled="store.loading" class="btn-primary">
          {{ store.loading ? 'Sending link...' : 'Send Reset Link' }}
        </button>
      </form>
      
      <p class="auth-link-text">
        Back to <router-link to="/login">Login</router-link>
      </p>
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

.success-msg {
  color: #9ae6b4;
  font-size: 14px;
  text-align: center;
}

.auth-link-text {
  color: #a0aec0;
  text-align: center;
  margin-top: 24px;
  font-size: 14px;
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
