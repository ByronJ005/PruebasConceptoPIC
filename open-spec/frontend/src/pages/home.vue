<template>
  <div class="home-container">
    <div class="home-card">
      <div class="profile-header">
        <div class="avatar">{{ user?.full_name?.charAt(0).toUpperCase() || 'U' }}</div>
        <h2>Bienvenido, {{ user?.full_name || 'Usuario' }}</h2>
        <p class="role-tag">Rol: {{ user?.role }}</p>
      </div>

      <div class="profile-details">
        <p class="email-info"><strong>Correo:</strong> {{ user?.email }}</p>
      </div>
      
      <div class="actions">
        <button @click="showLogoutModal = true" class="btn-danger">Cerrar Sesión</button>
      </div>
    </div>

    <!-- Modal de confirmación de logout -->
    <div v-if="showLogoutModal" class="modal-overlay" @click.self="showLogoutModal = false">
      <div class="modal-card">
        <h3>¿Cerrar Sesión?</h3>
        <p>¿Estás seguro que deseas cerrar sesión?</p>
        <div class="modal-actions">
          <button @click="showLogoutModal = false" class="btn-secondary">Cancelar</button>
          <button @click="handleLogout" class="btn-danger">Sí, salir</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useAuth } from '../composables/useAuth';
import { useRouter } from 'vue-router';

const { user, logoutUser } = useAuth();
const router = useRouter();
const showLogoutModal = ref(false);

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
  min-height: 100vh;
  padding: 1rem;
  font-family: 'Inter', sans-serif;
  background-color: #f3f4f6;
}
.home-card {
  background: white;
  padding: 3rem 2.5rem;
  border-radius: 16px;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 420px;
  text-align: center;
}

.profile-header {
  margin-bottom: 2rem;
}

.avatar {
  width: 80px;
  height: 80px;
  background: #e0f2fe;
  color: #0284c7;
  font-size: 2.5rem;
  font-weight: bold;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 50%;
  margin: 0 auto 1rem;
}

h2 {
  margin: 0 0 0.5rem 0;
  color: #0f172a;
  font-size: 1.5rem;
}

.role-tag {
  display: inline-block;
  background: #fef08a; /* Yellow from Loja palette */
  color: #854d0e;
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.8125rem;
  font-weight: 600;
  margin: 0;
}

.profile-details {
  background: #f8fafc;
  padding: 1.5rem;
  border-radius: 8px;
  margin-bottom: 2rem;
  text-align: left;
}

.email-info {
  color: #475569;
  font-size: 0.95rem;
  margin: 0;
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
  transition: all 0.2s;
  width: 100%;
}
.btn-danger:hover {
  background: #dc2626;
  transform: translateY(-1px);
}

.btn-secondary {
  background: #f1f5f9;
  color: #334155;
  padding: 0.75rem 1.5rem;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  width: 100%;
}

.btn-secondary:hover {
  background: #e2e8f0;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  backdrop-filter: blur(4px);
}

.modal-card {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
  width: 90%;
  max-width: 400px;
  text-align: center;
  animation: modal-in 0.3s ease-out;
}

.modal-card h3 {
  margin: 0 0 1rem 0;
  color: #0f172a;
  font-size: 1.25rem;
}

.modal-card p {
  color: #475569;
  margin-bottom: 2rem;
}

.modal-actions {
  display: flex;
  gap: 1rem;
}

@keyframes modal-in {
  from {
    opacity: 0;
    transform: translateY(1rem) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}
</style>
