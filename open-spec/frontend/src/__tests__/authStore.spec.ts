import { describe, it, expect, beforeEach, vi } from 'vitest';
import { setActivePinia, createPinia } from 'pinia';
import { useAuthStore } from '../stores/useAuthStore';
import axios from 'axios';

describe('Auth Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    vi.restoreAllMocks();
  });

  it('has correct initial state', () => {
    const store = useAuthStore();
    expect(store.user).toBeNull();
    expect(store.accessToken).toBeNull();
    expect(store.isAuthenticated).toBe(false);
  });

  it('login action sets user and token on success', async () => {
    const store = useAuthStore();
    const mockUser = { id: 1, email: 'test@example.com', full_name: 'Test', role: 'passenger' };
    
    vi.spyOn(axios, 'post').mockResolvedValueOnce({
      data: {
        access_token: 'fake-jwt-token',
        user: mockUser,
      },
    });

    const result = await store.login({ email: 'test@example.com', password: 'Password123' });
    
    expect(result.access_token).toBe('fake-jwt-token');
    expect(store.accessToken).toBe('fake-jwt-token');
    expect(store.user).toEqual(mockUser);
    expect(store.isAuthenticated).toBe(true);
  });

  it('logout action clears state', async () => {
    const store = useAuthStore();
    store.accessToken = 'token';
    store.user = { id: 1 };

    vi.spyOn(axios, 'post').mockResolvedValueOnce({});

    await store.logout();

    expect(store.accessToken).toBeNull();
    expect(store.user).toBeNull();
    expect(store.isAuthenticated).toBe(false);
  });

  it('refreshToken rotates the access token', async () => {
    const store = useAuthStore();
    
    vi.spyOn(axios, 'post').mockResolvedValueOnce({
      data: {
        access_token: 'new-rotated-token',
      },
    });

    const token = await store.refreshToken();

    expect(token).toBe('new-rotated-token');
    expect(store.accessToken).toBe('new-rotated-token');
  });

  it('clearAuth resets user and token', () => {
    const store = useAuthStore();
    store.accessToken = 'some-token';
    store.user = { name: 'John' };

    store.clearAuth();

    expect(store.accessToken).toBeNull();
    expect(store.user).toBeNull();
  });
});
