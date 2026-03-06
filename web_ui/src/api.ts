import type {
  Manager,
  User,
  CreateManagerPayload,
  UpdateManagerPayload,
  AddRegimenPayload,
  UpdateRegimenPayload,
  Regimen,
} from './types'

async function request<T>(url: string, options?: RequestInit): Promise<T> {
  const res = await fetch('/api' + url, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  })
  if (!res.ok) {
    const text = await res.text()
    throw new Error(text || `HTTP ${res.status}`)
  }
  return res.json()
}

export const api = {
  getOrCreateUser: (tg_user_id: number): Promise<User> =>
    request('/user', {
      method: 'POST',
      body: JSON.stringify({
        username: String(tg_user_id),
        tg_user_id,
        first_name: null,
        last_name: null,
      }),
    }),

  getManagers: (user_tg_id: number): Promise<Manager[]> =>
    request(`/drug-regimen/manager?user_tg_id=${user_tg_id}`),

  createManager: (data: CreateManagerPayload): Promise<Manager> =>
    request('/drug-regimen/manager/complex', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  // Sends all fields to avoid partial-update bug (backend uses model_dump() not exclude_none)
  updateManager: (id: number, data: UpdateManagerPayload): Promise<Manager> =>
    request(`/drug-regimen/manager/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    }),

  deleteManager: (id: number): Promise<{ message: string }> =>
    request(`/drug-regimen/manager/${id}`, { method: 'DELETE' }),

  addRegimen: (data: AddRegimenPayload): Promise<{ message: string }> =>
    request('/drug-regimen/regimen/complex', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  updateRegimen: (id: number, data: UpdateRegimenPayload): Promise<Regimen> =>
    request(`/drug-regimen/regimen/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    }),

  deleteRegimen: (id: number): Promise<{ message: string }> =>
    request(`/drug-regimen/regimen/${id}`, { method: 'DELETE' }),
}

// Helpers for date/time formatting
export function formatDate(iso: string): string {
  return new Date(iso).toLocaleDateString('ru-RU', {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
  })
}

export function formatTime(t: string): string {
  return t.slice(0, 5) // "HH:MM:SS" → "HH:MM"
}

// "HH:MM" → "HH:MM:00" for API
export function toApiTime(t: string): string {
  return t.length === 5 ? t + ':00' : t
}

// "2024-01-15T00:00:00" → "2024-01-15" for date input
export function toDateInput(iso: string): string {
  return iso.slice(0, 10)
}

// "2024-01-15" → "2024-01-15T00:00:00" for API
export function toApiDatetime(d: string): string {
  return d + 'T00:00:00'
}
