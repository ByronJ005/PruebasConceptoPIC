<template>
  <div class="auth-container">
    <div class="auth-card">
      <h2>Iniciar Sesión</h2>
      <p class="subtitle">Terminal Terrestre de Loja</p>
      
      <form @submit.prevent="handleLogin" class="auth-form">
        <div class="form-group">
          <label for="email">Correo Electrónico</label>
          <input 
            type="email" 
            id="email" 
            v-model="email" 
            placeholder="ejemplo@correo.com" 
            :class="{ 'has-error': errors.email }"
          />
          <span v-if="errors.email" class="error-text">{{ errors.email }}</span>
        </div>

        <div class="form-group">
          <label for="password">Contraseña</label>
          <input 
            type="password" 
            id="password" 
            v-model="password" 
            placeholder="••••••••" 
            :class="{ 'has-error': errors.password }"
          />
          <span v-if="errors.password" class="error-text">{{ errors.password }}</span>
        </div>

        <div class="auth-actions">
          <router-link to="/forgot-password" class="forgot-link">¿Olvidaste tu contraseña?</router-link>
        </div>

        <div v-if="errorMessage" class="alert error-alert">{{ errorMessage }}</div>

        <button type="submit" :disabled="isLoading" class="btn-primary">
          <span v-if="isLoading">Cargando...</span>
          <span v-else>Ingresar</span>
        </button>
      </form>

      <p class="auth-footer">
        ¿No tienes cuenta? <router-link to="/register">Regístrate aquí</router-link>
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuth } from '../../composables/useAuth';
import { z } from 'zod';

const email = ref('');
const password = ref('');
const isLoading = ref(false);
const errorMessage = ref('');
const errors = ref<{ email?: string; password?: string }>({});

const router = useRouter();
const { loginUser } = useAuth();

const loginSchema = z.object({
  email: z.string().email('Formato de correo inválido'),
  password: z.string().min(8, 'La contraseña debe tener al menos 8 caracteres'),
});

const handleLogin = async () => {
  errors.value = {};
  errorMessage.value = '';

  const validation = loginSchema.safeParse({
    email: email.value,
    password: password.value,
  });

  if (!validation.success) {
    validation.error.errors.forEach((err) => {
      if (err.path[0] === 'email') errors.value.email = err.message;
      if (err.path[0] === 'password') errors.value.password = err.message;
    });
    return;
  }

  isLoading.value = true;
  try {
    await loginUser({
      email: email.value,
      password: password.value,
    });
    router.push('/');
  } catch (error: any) {
    if (error.response?.status === 401) {
      errorMessage.value = 'Credenciales incorrectas.';
    } else if (error.response?.status === 403) {
      errorMessage.value = 'Esta cuenta está desactivada.';
    } else {
      errorMessage.value = 'Ocurrió un error inesperado. Inténtalo de nuevo.';
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
.auth-actions {
  display: flex;
  justify-content: flex-end;
}
.forgot-link {
  font-size: 0.8125rem;
  color: #3b82f6;
  text-decoration: none;
}
.forgot-link:hover {
  text-decoration: underline;
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
