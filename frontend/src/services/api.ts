import type { Maintenance, Payment, Property, User } from '../types'

const baseUrl = import.meta.env.VITE_API_URL ?? '/api'
const accessKey = 'nyumbani.access'
const refreshKey = 'nyumbani.refresh'

export const auth = {
  get token() { return localStorage.getItem(accessKey) },
  save(access: string, refresh: string) { localStorage.setItem(accessKey, access); localStorage.setItem(refreshKey, refresh) },
  clear() { localStorage.removeItem(accessKey); localStorage.removeItem(refreshKey) },
}

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const headers = new Headers(options.headers)
  headers.set('Content-Type', 'application/json')
  if (auth.token) headers.set('Authorization', `Bearer ${auth.token}`)
  const response = await fetch(`${baseUrl}${path}`, { ...options, headers })
  if (!response.ok) throw new Error((await response.json().catch(() => ({}))).detail ?? 'Something went wrong.')
  return response.status === 204 ? (undefined as T) : response.json()
}

export const api = {
  properties: () => request<Property[]>('/properties/'),
  payments: () => request<Payment[]>('/payments/history/'),
  maintenance: () => request<Maintenance[]>('/users/maintenance/'),
  me: () => request<User>('/users/me/'),
  async login(username: string, password: string) {
    const tokens = await request<{ access: string; refresh: string }>('/token/', { method: 'POST', body: JSON.stringify({ username, password }) })
    auth.save(tokens.access, tokens.refresh)
    return this.me()
  },
  register: (data: Record<string, string>) => request<User>('/users/register/', { method: 'POST', body: JSON.stringify(data) }),
}
