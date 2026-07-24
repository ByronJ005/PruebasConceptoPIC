<template>
  <div class="auth-container">
    <div class="auth-card">
      <h2>Recuperar Contraseña</h2>
      <p class="subtitle">Ingresa tu correo para recibir un enlace de recuperación</p>
      
      <form @submit.prevent="handleForgotPassword" class="auth-form">
        <div class="form-group">
          <label for="email">Correo Electrónico</label>
          <input 
            type="email" 
            id="email" 
            v-model="email" 
            placeholder="ejemplo@correo.com" 
            :class="{ 'has-error': error }"
          />
          <span v-if="error" class="error-text">{{ error }}</span>
        </div>

        <div v-if="successMessage" class="alert success-alert">{{ successMessage }}</div>
        <div v-if="errorMessage" class="alert error-alert">{{ errorMessage }}</div>

        <button type="submit" :disabled="isLoading" class="btn-primary">
          <span v-if="isLoading">Enviando...</span>
          <span v-else>Enviar Enlace</span>
        </button>
      </form>

      <p class="auth-footer">
        <router-link to="/login">Volver al inicio de sesión</router-link>
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { z } from 'zod';
import axios from 'axios';

const email = ref('');
const isLoading = ref(false);
const successMessage = ref('');
const errorMessage = ref('');
const error = ref('');

const emailSchema = z.string().email('Formato de correo inválido');
const apiBase = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';

const handleForgotPassword = async () => {
  error.value = '';
  successMessage.value = '';
  errorMessage.value = '';

  const validation = emailSchema.safeParse(email.value);
  if (!validation.success) {
    error.value = validation.error.errors[0].message;
    return;
  }

  isLoading.value = true;
  try {
    await axios.post(`${apiBase}/auth/forgot-password`, { email: email.value });
    successMessage.value = 'Si el correo está registrado, recibirás un enlace para restablecer tu contraseña.';
    email.value = '';
  } catch (err) {
    errorMessage.value = 'Ocurrió un error al procesar tu solicitud. Inténtalo más tarde.';
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
.auth-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
  font-family: 'Inter', sans-serif;
}
.auth-card {
  background: white;
  padding: 2.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  width: 100%;
  max-width: 420px;
}
h2 {
  margin: 0 0 0.25rem 0;
  color: #1a1a1a;
  text-align: center;
  font-size: 1.75rem;
}
.subtitle {
  color: #666;
  text-align: center;
  margin-bottom: 2rem;
  font-size: 0.9rem;
}
.auth-form {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}
.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.375rem;
}
label {
  font-size: 0.875rem;
  font-weight: 500;
  color: #4a4a4a;
}
input {
  padding: 0.75rem;
  border: 1px solid #dcdcdc;
  border-radius: 6px;
  font-size: 1rem;
  transition: border-color 0.2s;
}
input:focus {
  outline: none;
  border-color: #3b82f6;
}
input.has-error {
  border-color: #ef4444;
}
.error-text {
  color: #ef4444;
  font-size: 0.75rem;
}
.alert {
  padding: 0.75rem;
  border-radius: 6px;
  font-size: 0.875rem;
}
.error-alert {
  background: #fef2f2;
  color: #b91c1c;
  border: 1px solid #fca5a5;
}
.success-alert {
  background: #f0fdf4;
  color: #15803d;
  border: 1px solid #86efac;
}
.btn-primary {
  background: #3b82f6;
  color: white;
  padding: 0.875rem;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}
.btn-primary:hover {
  background: #2563eb;
}
.btn-primary:disabled {
  background: #93c5fd;
  cursor: not-allowed;
}
.auth-footer {
  text-align: center;
  font-size: 0.875rem;
  color: #666;
  margin-top: 1.5rem;
}
.auth-footer a {
  color: #3b82f6;
  text-decoration: none;
  font-weight: 500;
}
.auth-footer a:hover {
  text-decoration: underline;
}
</style>
