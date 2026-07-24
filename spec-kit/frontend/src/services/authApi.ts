import api from './api'

export async function registerApi(email: string, password: string) {
  const response = await api.post('/api/auth/register', { email, password })
  return response.data
}

export async function loginApi(email: string, password: string) {
  const response = await api.post('/api/auth/login', { email, password })
  return response.data
}

export async function logoutApi() {
  const response = await api.post('/api/auth/logout')
  return response.data
}

export async function passwordRecoveryApi(email: string) {
  const response = await api.post('/api/auth/password-recovery', { email })
  return response.data
}

export async function passwordResetApi(token: string, new_password: string) {
  const response = await api.post('/api/auth/password-reset', { token, new_password })
  return response.data
}
