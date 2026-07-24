<template>
  <div class="auth-container">
    <div class="auth-layout">
      <div class="auth-image">
        <img src="https://images.unsplash.com/photo-1590523277543-a94d2e4eb00b?q=80&w=800&auto=format&fit=crop" alt="Destinos desde Loja" />
        <div class="auth-image-overlay">
          <h3>Únete a nosotros</h3>
          <p>La forma más fácil de viajar desde Loja</p>
        </div>
      </div>
      <div class="auth-card">
        <h2>Registrarse</h2>
        <p class="subtitle">Crear una cuenta nueva</p>

        <form @submit.prevent="handleRegister" class="auth-form">
        <div class="form-group">
          <label for="fullName">Nombre Completo</label>
          <input 
            type="text" 
            id="fullName" 
            v-model="fullName" 
            placeholder="Juan Pérez" 
            :class="{ 'has-error': errors.fullName }"
          />
          <span v-if="errors.fullName" class="error-text">{{ errors.fullName }}</span>
        </div>

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

        <div v-if="errorMessage" class="alert error-alert">{{ errorMessage }}</div>
        <div v-if="successMessage" class="alert success-alert">{{ successMessage }}</div>

          <button type="submit" :disabled="isLoading" class="btn-primary">
            <span v-if="isLoading">Cargando...</span>
            <span v-else>Registrarse</span>
          </button>
        </form>

        <p class="auth-footer">
          ¿Ya tienes una cuenta? <router-link to="/login">Inicia sesión</router-link>
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

const fullName = ref('');
const email = ref('');
const password = ref('');
const isLoading = ref(false);
const errorMessage = ref('');
const successMessage = ref('');
const errors = ref<{ fullName?: string; email?: string; password?: string }>({});

const router = useRouter();
const { registerUser } = useAuth();

const registerSchema = z.object({
  fullName: z.string().min(1, 'El nombre es obligatorio'),
  email: z.string().email('Formato de correo inválido'),
  password: z.string()
    .min(8, 'Debe tener al menos 8 caracteres')
    .regex(/[A-Z]/, 'Debe contener al menos una letra mayúscula')
    .regex(/[a-z]/, 'Debe contener al menos una letra minúscula')
    .regex(/\d/, 'Debe contener al menos un número'),
});

const handleRegister = async () => {
  errors.value = {};
  errorMessage.value = '';
  successMessage.value = '';

  const validation = registerSchema.safeParse({
    fullName: fullName.value,
    email: email.value,
    password: password.value,
  });

  if (!validation.success) {
    validation.error.issues.forEach((err: any) => {
      const field = err.path[0] as string;
      if (field === 'fullName') errors.value.fullName = err.message;
      if (field === 'email') errors.value.email = err.message;
      if (field === 'password') errors.value.password = err.message;
    });
    return;
  }

  isLoading.value = true;
  try {
    await registerUser({
      full_name: fullName.value,
      email: email.value,
      password: password.value,
    });
    successMessage.value = 'Registro exitoso. Redirigiendo al login...';
    setTimeout(() => {
      router.push('/login');
    }, 2000);
  } catch (error: any) {
    if (error.response?.status === 409) {
      errorMessage.value = 'El correo ya está registrado.';
    } else {
      errorMessage.value = 'Error al registrar usuario. Inténtalo más tarde.';
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
