import { useState, useEffect } from 'react'
import { UserSetup } from './components/UserSetup'
import { Dashboard } from './components/Dashboard'

const STORAGE_KEY = 'tg_user_id'

function getTelegramUserId(): number | null {
  const tgId = window.Telegram?.WebApp?.initDataUnsafe?.user?.id
  return tgId ?? null
}

export default function App() {
  const [userId, setUserId] = useState<number | null>(() => {
    // Приоритет: Telegram WebApp > localStorage
    const tgId = getTelegramUserId()
    if (tgId) return tgId
    const stored = localStorage.getItem(STORAGE_KEY)
    return stored ? parseInt(stored) : null
  })

  useEffect(() => {
    const tg = window.Telegram?.WebApp
    if (tg) {
      tg.ready()
      tg.expand()
    }
  }, [])

  useEffect(() => {
    if (userId !== null) {
      localStorage.setItem(STORAGE_KEY, String(userId))
    } else {
      localStorage.removeItem(STORAGE_KEY)
    }
  }, [userId])

  // Если открыто в TG — скрываем кнопку "Сменить" (id зафиксирован из WebApp)
  const isTelegram = Boolean(window.Telegram?.WebApp?.initDataUnsafe?.user)

  if (userId === null) {
    return <UserSetup onSetup={setUserId} />
  }

  return (
    <Dashboard
      userId={userId}
      onLogout={isTelegram ? undefined : () => setUserId(null)}
    />
  )
}
