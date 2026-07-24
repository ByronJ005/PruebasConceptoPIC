import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import axios from 'axios';

const apiBase = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';

export const useAuthStore = defineStore('auth', () => {
  const user = ref<any>(null);
  const accessToken = ref<string | null>(null);

  const isAuthenticated = computed(() => !!accessToken.value);

  function clearAuth() {
    user.value = null;
    accessToken.value = null;
  }

  async function login(credentials: any) {
    const res = await axios.post(`${apiBase}/auth/login`, credentials, {
      withCredentials: true,
    });
    accessToken.value = res.data.access_token;
    user.value = res.data.user;
    return res.data;
  }

  async function register(data: any) {
    const res = await axios.post(`${apiBase}/auth/register`, data);
    return res.data;
  }

  async function logout() {
    try {
      await axios.post(
        `${apiBase}/auth/logout`,
        {},
        {
          headers: accessToken.value ? { Authorization: `Bearer ${accessToken.value}` } : {},
          withCredentials: true,
        }
      );
    } finally {
      clearAuth();
    }
  }

  async function refreshToken(): Promise<string> {
    const res = await axios.post(
      `${apiBase}/auth/refresh`,
      {},
      {
        withCredentials: true,
      }
    );
    accessToken.value = res.data.access_token;
    return res.data.access_token;
  }

  return {
    user,
    accessToken,
    isAuthenticated,
    clearAuth,
    login,
    register,
    logout,
    refreshToken,
  };
});
