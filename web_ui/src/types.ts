export interface User {
  id: number
  username: string
  tg_user_id: number
  first_name: string | null
  last_name: string | null
  registered_at: string
}

export interface Regimen {
  id: number
  reception_time: string // "HH:MM:SS" — already in user's local timezone
  supplement: string
  is_active: boolean
}

export interface Manager {
  id: number
  name: string
  start_date: string   // ISO datetime
  finish_date: string  // ISO datetime
  timezone: string     // "МСК" | "+1" | "+2" ... "-1"
  is_active: boolean
  regimens: Regimen[]
  user: User
}

// Timezone is offset from MSK (UTC+3).
// Keys map to UTC offset labels shown in UI.
export const TIMEZONES: Record<string, string> = {
  '-1': 'UTC+2 (МСК−1)',
  'МСК': 'UTC+3 (МСК)',
  '+1': 'UTC+4 (МСК+1, Самара)',
  '+2': 'UTC+5 (МСК+2, Екатеринбург)',
  '+3': 'UTC+6 (МСК+3, Омск)',
  '+4': 'UTC+7 (МСК+4, Красноярск)',
  '+5': 'UTC+8 (МСК+5, Иркутск)',
  '+6': 'UTC+9 (МСК+6, Якутск)',
  '+7': 'UTC+10 (МСК+7, Владивосток)',
  '+8': 'UTC+11 (МСК+8)',
  '+9': 'UTC+12 (МСК+9)',
}

export interface CreateManagerPayload {
  user_tg_id: number
  manager: {
    name: string
    start_date: string
    finish_date: string
    timezone: string
    is_active: boolean
  }
  regimen: {
    reception_time: string
    supplement: string
    is_active: boolean
  }
}

export interface UpdateManagerPayload {
  name: string
  start_date: string
  finish_date: string
  timezone: string
  is_active: boolean
}

export interface AddRegimenPayload {
  manager_id: number
  reception_time: string
  supplement: string
  is_active: boolean
}

export interface UpdateRegimenPayload {
  reception_time?: string
  supplement?: string
  is_active?: boolean
}
