const BASE_URL = 'http://localhost:8000'

interface RequestOptions extends RequestInit {
  json?: any
}

async function request(path: string, options: RequestOptions = {}) {
  const url = `${BASE_URL}${path}`
  
  // Set headers
  const headers = new Headers(options.headers || {})
  if (!headers.has('Content-Type') && options.json) {
    headers.set('Content-Type', 'application/json')
  }
  
  // Attach access token
  const token = localStorage.getItem('access_token')
  if (token && !headers.has('Authorization')) {
    headers.set('Authorization', `Bearer ${token}`)
  }

  const fetchOptions: RequestInit = {
    ...options,
    headers,
    credentials: 'include', // Needed to send cookies
  }

  if (options.json) {
    fetchOptions.body = JSON.stringify(options.json)
  }

  const response = await fetch(url, fetchOptions)

  if (response.status === 401) {
    // Session expired
    localStorage.removeItem('access_token')
    localStorage.removeItem('user')
    if (typeof window !== 'undefined') {
      window.dispatchEvent(new Event('auth-logout'))
    }
    throw new Error('Unauthorized')
  }

  if (!response.ok) {
    let errorDetail = 'An error occurred'
    try {
      const errorJson = await response.json()
      errorDetail = errorJson.detail || errorDetail
    } catch {
      // ignore
    }
    throw { response: { data: { detail: errorDetail } } }
  }

  return {
    data: await response.json()
  }
}

const api = {
  get: (path: string, options?: RequestOptions) => request(path, { ...options, method: 'GET' }),
  post: (path: string, body?: any, options?: RequestOptions) => request(path, { ...options, method: 'POST', json: body }),
  put: (path: string, body?: any, options?: RequestOptions) => request(path, { ...options, method: 'PUT', json: body }),
  delete: (path: string, options?: RequestOptions) => request(path, { ...options, method: 'DELETE' }),
}

export default api
