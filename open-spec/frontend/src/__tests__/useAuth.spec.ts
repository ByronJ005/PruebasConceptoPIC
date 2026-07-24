import { describe, it, expect, beforeEach, vi } from 'vitest';
import { setActivePinia, createPinia } from 'pinia';
import { useAuth } from '../composables/useAuth';
import { useAuthStore } from '../stores/useAuthStore';

describe('useAuth Composable', () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  it('provides reactive access to store state', () => {
    const store = useAuthStore();
    const { user, accessToken, isAuthenticated } = useAuth();

    expect(user.value).toBeNull();
    expect(accessToken.value).toBeNull();
    expect(isAuthenticated.value).toBe(false);

    store.accessToken = 'some-token';
    store.user = { id: 1 };

    expect(user.value).toEqual({ id: 1 });
    expect(accessToken.value).toBe('some-token');
    expect(isAuthenticated.value).toBe(true);
  });

  it('calls correct store methods for actions', async () => {
    const store = useAuthStore();
    const { loginUser, logoutUser, registerUser } = useAuth();

    const loginSpy = vi.spyOn(store, 'login').mockResolvedValueOnce({} as any);
    const logoutSpy = vi.spyOn(store, 'logout').mockResolvedValueOnce();
    const registerSpy = vi.spyOn(store, 'register').mockResolvedValueOnce({} as any);

    await loginUser({ email: 'test@example.com', password: 'password' });
    expect(loginSpy).toHaveBeenCalledWith({ email: 'test@example.com', password: 'password' });

    await logoutUser();
    expect(logoutSpy).toHaveBeenCalled();

    await registerUser({ email: 'test@example.com', password: 'password', full_name: 'Name' });
    expect(registerSpy).toHaveBeenCalledWith({ email: 'test@example.com', password: 'password', full_name: 'Name' });
  });
});
