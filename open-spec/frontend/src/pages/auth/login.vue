<template>
  <div class="auth-container">
    <div class="auth-layout">
      <div class="auth-image">
        <img src="https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?q=80&w=800&auto=format&fit=crop" alt="Viaje desde Loja" />
        <div class="auth-image-overlay">
          <h3>Comienza tu aventura</h3>
          <p>Conecta con los mejores destinos desde Loja</p>
        </div>
      </div>
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
    validation.error.issues.forEach((err: any) => {
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
  max-width: 900px;
}

.auth-image {
  display: none;
  position: relative;
  width: 50%;
}

@media (min-width: 768px) {
  .auth-image {
    display: block;
  }
}

.auth-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.auth-image-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 2rem;
  background: linear-gradient(to top, rgba(0, 0, 0, 0.8), transparent);
  color: white;
}

.auth-image-overlay h3 {
  margin: 0 0 0.5rem 0;
  font-size: 1.5rem;
}

.auth-image-overlay p {
  margin: 0;
  color: #e2e8f0;
}

.auth-card {
  padding: 3rem;
  width: 100%;
}

@media (min-width: 768px) {
  .auth-card {
    width: 50%;
  }
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
.auth-actions {
  display: flex;
  justify-content: flex-end;
}
.forgot-link {
  font-size: 0.8125rem;
  color: #0ea5e9;
  text-decoration: none;
  font-weight: 500;
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
