<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/authStore'

const store = useAuthStore()
const router = useRouter()

async function handleLogout() {
  await store.logout()
  router.push('/login')
}
</script>

<template>
  <div class="dashboard-container">
    <div class="dashboard-card">
      <div class="header">
        <h1>Cooperative Ticket Booking</h1>
        <button @click="handleLogout" class="btn-logout">Logout</button>
      </div>

      <div class="profile-section">
        <p class="welcome">Welcome, <span class="user-email">{{ store.user?.email }}</span>!</p>
        <p class="status-badge">Authenticated via JWT</p>
      </div>

      <div class="content-grid">
        <div class="info-card">
          <h3>Your Bookings</h3>
          <p class="no-bookings">No active ticket bookings found.</p>
          <button class="btn-action">Book New Ticket</button>
        </div>

        <div class="info-card">
          <h3>Available Cooperatives</h3>
          <ul class="cooperative-list">
            <li>Loja Internacional</li>
            <li>Trans Esmeraldas</li>
            <li>Cooperativa Loja</li>
            <li>Flota Imbabura</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.dashboard-container {
  padding: 40px 20px;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  min-height: 80vh;
  font-family: 'Outfit', 'Inter', sans-serif;
}

.dashboard-card {
  background: rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  padding: 32px;
  width: 100%;
  max-width: 800px;
  box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  padding-bottom: 20px;
  margin-bottom: 24px;
}

h1 {
  color: #ffffff;
  font-size: 24px;
  font-weight: 600;
  margin: 0;
}

.btn-logout {
  background: transparent;
  color: #fc8181;
  border: 1px solid #fc8181;
  border-radius: 6px;
  padding: 8px 16px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-logout:hover {
  background: #fc8181;
  color: white;
}

.profile-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 8px;
  padding: 16px 24px;
  margin-bottom: 32px;
}

.welcome {
  color: #cbd5e0;
  font-size: 16px;
  margin: 0;
}

.user-email {
  color: #63b3ed;
  font-weight: 600;
}

.status-badge {
  background: rgba(72, 187, 120, 0.2);
  color: #48bb78;
  padding: 4px 12px;
  border-radius: 9999px;
  font-size: 12px;
  font-weight: 600;
  margin: 0;
}

.content-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

.info-card {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  padding: 24px;
}

.info-card h3 {
  color: #ffffff;
  margin-top: 0;
  margin-bottom: 16px;
  font-size: 18px;
  font-weight: 500;
}

.no-bookings {
  color: #a0aec0;
  font-size: 14px;
  margin-bottom: 20px;
}

.btn-action {
  background: linear-gradient(135deg, #3182ce 0%, #319795 100%);
  color: white;
  border: none;
  border-radius: 6px;
  padding: 10px 20px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s;
  width: 100%;
}

.btn-action:hover {
  transform: translateY(-1px);
}

.cooperative-list {
  color: #cbd5e0;
  padding-left: 20px;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.cooperative-list li {
  font-size: 14px;
}

@media (max-width: 600px) {
  .content-grid {
    grid-template-columns: 1fr;
  }
}
</style>
