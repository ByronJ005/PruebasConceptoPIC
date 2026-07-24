import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import RegisterView from '../views/RegisterView.vue'
import { useAuthStore } from '../stores/authStore'
import * as authApi from '../services/authApi'

// Mock the API calls
vi.mock('../services/authApi', () => ({
  registerApi: vi.fn(),
}))

describe('RegisterView.vue', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
  })

  it('renders registration form fields', () => {
    const wrapper = mount(RegisterView)
    expect(wrapper.find('input[type="email"]').exists()).toBe(true)
    expect(wrapper.find('input[type="password"]').exists()).toBe(true)
    expect(wrapper.find('button[type="submit"]').exists()).toBe(true)
  })

  it('shows error if password does not meet criteria', async () => {
    const wrapper = mount(RegisterView)
    const emailInput = wrapper.find('input[type="email"]')
    const passwordInput = wrapper.find('input[type="password"]')
    
    await emailInput.setValue('test@example.com')
    await passwordInput.setValue('123') // Too short
    await wrapper.find('form').trigger('submit.prevent')
    
    expect(wrapper.text()).toContain('Password must be at least 8 characters long')
  })

  it('calls registerApi on valid form submission', async () => {
    const wrapper = mount(RegisterView)
    const emailInput = wrapper.find('input[type="email"]')
    const passwordInput = wrapper.find('input[type="password"]')
    
    await emailInput.setValue('valid@example.com')
    await passwordInput.setValue('SecurePassword123!')
    
    // Setup mock resolution
    vi.mocked(authApi.registerApi).mockResolvedValueOnce({ id: '123', email: 'valid@example.com', is_active: true })
    
    await wrapper.find('form').trigger('submit.prevent')
    
    expect(authApi.registerApi).toHaveBeenCalledWith('valid@example.com', 'SecurePassword123!')
  })
})
