import { computed } from 'vue';
import { useAuthStore } from '../stores/useAuthStore';

export function useAuth() {
  const authStore = useAuthStore();

  const user = computed(() => authStore.user);
  const accessToken = computed(() => authStore.accessToken);
  const isAuthenticated = computed(() => authStore.isAuthenticated);

  async function loginUser(credentials: any) {
    return await authStore.login(credentials);
  }

  async function logoutUser() {
    return await authStore.logout();
  }

  async function registerUser(data: any) {
    return await authStore.register(data);
  }

  return {
    user,
    accessToken,
    isAuthenticated,
    loginUser,
    logoutUser,
    registerUser,
  };
}
