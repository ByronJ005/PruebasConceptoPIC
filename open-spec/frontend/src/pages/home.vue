<template>
  <div class="home-container">
    <div class="home-card">
      <h2>Bienvenido, {{ user?.full_name || 'Usuario' }}</h2>
      <p class="role-tag">Rol: {{ user?.role }}</p>
      <p class="email-info">Correo: {{ user?.email }}</p>
      
      <div class="actions">
        <button @click="handleLogout" class="btn-danger">Cerrar Sesión</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useAuth } from '../composables/useAuth';
import { useRouter } from 'vue-router';

const { user, logoutUser } = useAuth();
const router = useRouter();

const handleLogout = async () => {
  await logoutUser();
  router.push('/login');
};
</script>

<style scoped>
.home-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
  font-family: 'Inter', sans-serif;
}
.home-card {
  background: white;
  padding: 2.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  width: 100%;
  max-width: 420px;
  text-align: center;
}
h2 {
  margin-bottom: 0.5rem;
  color: #1a1a1a;
}
.role-tag {
  display: inline-block;
  background: #e0f2fe;
  color: #0369a1;
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.8125rem;
  font-weight: 600;
  margin-bottom: 1rem;
}
.email-info {
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 2rem;
}
.btn-danger {
  background: #ef4444;
  color: white;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}
.btn-danger:hover {
  background: #dc2626;
}
</style>
