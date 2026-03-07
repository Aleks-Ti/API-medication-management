interface TelegramWebAppUser {
  id: number
  first_name: string
  last_name?: string
  username?: string
  language_code?: string
}

interface TelegramWebApp {
  ready(): void
  expand(): void
  close(): void
  initDataUnsafe: {
    user?: TelegramWebAppUser
    query_id?: string
    auth_date?: number
    hash?: string
  }
  colorScheme: 'light' | 'dark'
  themeParams: Record<string, string>
  isExpanded: boolean
  viewportHeight: number
  viewportStableHeight: number
}

interface Window {
  Telegram?: {
    WebApp: TelegramWebApp
  }
}
