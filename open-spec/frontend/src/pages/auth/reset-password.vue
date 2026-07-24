<template>
  <div class="auth-container">
    <div class="auth-card">
      <h2>Nueva Contraseña</h2>
      <p class="subtitle">Establece tu nueva contraseña</p>
      
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
    validation.error.errors.forEach((err) => {
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
