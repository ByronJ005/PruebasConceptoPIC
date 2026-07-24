import { describe, it, expect, beforeEach, vi } from 'vitest';
import { mount } from '@vue/test-utils';
import LoginPage from '../pages/auth/login.vue';
import { createPinia, setActivePinia } from 'pinia';
import router from '../router';
import * as authComposable from '../composables/useAuth';

describe('LoginPage Component', () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    vi.restoreAllMocks();
  });

  it('renders correctly with initial elements', () => {
    const wrapper = mount(LoginPage, {
      global: {
        plugins: [router],
      },
    });

    expect(wrapper.find('h2').text()).toBe('Iniciar Sesión');
    expect(wrapper.find('input[type="email"]').exists()).toBe(true);
    expect(wrapper.find('input[type="password"]').exists()).toBe(true);
    expect(wrapper.find('button[type="submit"]').text()).toBe('Ingresar');
  });

  it('shows error messages if form fields are empty or invalid', async () => {
    const wrapper = mount(LoginPage, {
      global: {
        plugins: [router],
      },
    });

    await wrapper.find('form').trigger('submit.prevent');

    expect(wrapper.text()).toContain('Formato de correo inválido');
    expect(wrapper.text()).toContain('La contraseña debe tener al menos 8 caracteres');
  });

  it('calls loginUser and redirects on success', async () => {
    const mockLoginUser = vi.fn<any>().mockResolvedValueOnce({});
    vi.spyOn(authComposable, 'useAuth').mockReturnValue({
      user: {} as any,
      accessToken: {} as any,
      isAuthenticated: {} as any,
      loginUser: mockLoginUser as any,
      logoutUser: vi.fn<any>() as any,
      registerUser: vi.fn<any>() as any,
    });

    const pushSpy = vi.spyOn(router, 'push');

    const wrapper = mount(LoginPage, {
      global: {
        plugins: [router],
      },
    });

    await wrapper.find('input[type="email"]').setValue('correct@example.com');
    await wrapper.find('input[type="password"]').setValue('Password123');
    await wrapper.find('form').trigger('submit.prevent');

    expect(mockLoginUser).toHaveBeenCalledWith({
      email: 'correct@example.com',
      password: 'Password123',
    });
    expect(pushSpy).toHaveBeenCalledWith('/');
  });

  it('shows api credentials error on 401', async () => {
    const mockLoginUser = vi.fn<any>().mockRejectedValueOnce({
      response: { status: 401 }
    });
    vi.spyOn(authComposable, 'useAuth').mockReturnValue({
      user: {} as any,
      accessToken: {} as any,
      isAuthenticated: {} as any,
      loginUser: mockLoginUser as any,
      logoutUser: vi.fn<any>() as any,
      registerUser: vi.fn<any>() as any,
    });

    const wrapper = mount(LoginPage, {
      global: {
        plugins: [router],
      },
    });

    await wrapper.find('input[type="email"]').setValue('wrong@example.com');
    await wrapper.find('input[type="password"]').setValue('Password123');
    await wrapper.find('form').trigger('submit.prevent');

    expect(wrapper.find('.error-alert').text()).toBe('Credenciales incorrectas.');
  });
});
