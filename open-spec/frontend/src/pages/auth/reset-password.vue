<template>
  <div class="auth-container">
    <div class="auth-layout">
      <div class="auth-card">
        <div class="auth-header">
          <span class="icon">🔐</span>
          <h2>Nueva Contraseña</h2>
          <p class="subtitle">Establece tu nueva contraseña</p>
        </div>

        <form @submit.prevent="handleResetPassword" class="auth-form">
        <div class="form-group">
          <label for="password">Contraseña Nueva</label>
          <input 
            type="password" 
            id="password" 
            v-model="password" 
            placeholder="••••••••" 
            :class="{ 'has-error': errors.password }"
          />
          <span v-if="errors.password" class="error-text">{{ errors.password }}</span>
        </div>

        <div class="form-group">
          <label for="confirmPassword">Confirmar Contraseña</label>
          <input 
            type="password" 
            id="confirmPassword" 
            v-model="confirmPassword" 
            placeholder="••••••••" 
            :class="{ 'has-error': errors.confirmPassword }"
          />
          <span v-if="errors.confirmPassword" class="error-text">{{ errors.confirmPassword }}</span>
        </div>

        <div v-if="successMessage" class="alert success-alert">{{ successMessage }}</div>
        <div v-if="errorMessage" class="alert error-alert">{{ errorMessage }}</div>

          <button type="submit" :disabled="isLoading || !token" class="btn-primary">
            <span v-if="isLoading">Actualizando...</span>
            <span v-else>Actualizar Contraseña</span>
          </button>
        </form>

        <p class="auth-footer">
          <router-link to="/login">Volver al inicio de sesión</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { z } from 'zod';
import axios from 'axios';

const password = ref('');
const confirmPassword = ref('');
const token = ref('');
const isLoading = ref(false);
const successMessage = ref('');
const errorMessage = ref('');
const errors = ref<{ password?: string; confirmPassword?: string }>({});

const route = useRoute();
const router = useRouter();

const apiBase = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';

onMounted(() => {
  const queryToken = route.query.token;
  if (queryToken && typeof queryToken === 'string') {
    token.value = queryToken;
  } else {
    errorMessage.value = 'Enlace inválido o token no proporcionado.';
  }
});

const passwordSchema = z.object({
  password: z.string()
    .min(8, 'Debe tener al menos 8 caracteres')
    .regex(/[A-Z]/, 'Debe contener al menos una letra mayúscula')
    .regex(/[a-z]/, 'Debe contener al menos una letra minúscula')
    .regex(/\d/, 'Debe contener al menos un número'),
  confirmPassword: z.string(),
}).refine((data) => data.password === data.confirmPassword, {
  message: 'Las contraseñas no coinciden',
  path: ['confirmPassword'],
});

const handleResetPassword = async () => {
  errors.value = {};
  errorMessage.value = '';
  successMessage.value = '';

  const validation = passwordSchema.safeParse({
    password: password.value,
    confirmPassword: confirmPassword.value,
  });

  if (!validation.success) {
    validation.error.issues.forEach((err: any) => {
      const field = err.path[0] as string;
      if (field === 'password') errors.value.password = err.message;
      if (field === 'confirmPassword') errors.value.confirmPassword = err.message;
    });
    return;
  }

  isLoading.value = true;
  try {
    await axios.post(`${apiBase}/auth/reset-password`, {
      token: token.value,
      new_password: password.value,
    });
    successMessage.value = 'Tu contraseña ha sido restablecida. Redirigiendo al inicio de sesión...';
    setTimeout(() => {
      router.push('/login');
    }, 3000);
  } catch (err: any) {
    if (err.response?.status === 400) {
      errorMessage.value = 'El enlace de recuperación es inválido o ha expirado.';
    } else {
      errorMessage.value = 'Ocurrió un error al restablecer tu contraseña. Inténtalo más tarde.';
    }
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
  min-height: 100vh;
  padding: 1rem;
  font-family: 'Inter', sans-serif;
  background-color: #f3f4f6;
}

.auth-layout {
  display: flex;
  background: white;
  border-radius: 16px;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  width: 100%;
  max-width: 480px;
}

.auth-card {
  padding: 3rem;
  width: 100%;
}

.auth-header {
  text-align: center;
  margin-bottom: 2rem;
}

.auth-header .icon {
  font-size: 3rem;
  display: block;
  margin-bottom: 1rem;
}

h2 {
  margin: 0 0 0.5rem 0;
  color: #1a1a1a;
  font-size: 1.75rem;
}
.subtitle {
  color: #666;
  font-size: 0.95rem;
  line-height: 1.5;
  margin: 0;
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
  border-color: #0ea5e9;
  box-shadow: 0 0 0 3px rgba(14, 165, 233, 0.2);
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
  background: #0ea5e9;
  color: white;
  padding: 0.875rem;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}
.btn-primary:hover {
  background: #0284c7;
  transform: translateY(-1px);
}
.btn-primary:disabled {
  background: #7dd3fc;
  cursor: not-allowed;
  transform: none;
}
.auth-footer {
  text-align: center;
  font-size: 0.875rem;
  color: #666;
  margin-top: 1.5rem;
}
.auth-footer a {
  color: #0ea5e9;
  text-decoration: none;
  font-weight: 600;
}
.auth-footer a:hover {
  text-decoration: underline;
}
</style>
