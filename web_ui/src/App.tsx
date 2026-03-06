import { useState, useEffect } from 'react'
import { UserSetup } from './components/UserSetup'
import { Dashboard } from './components/Dashboard'

const STORAGE_KEY = 'tg_user_id'

export default function App() {
  const [userId, setUserId] = useState<number | null>(() => {
    const stored = localStorage.getItem(STORAGE_KEY)
    return stored ? parseInt(stored) : null
  })

  useEffect(() => {
    if (userId !== null) {
      localStorage.setItem(STORAGE_KEY, String(userId))
    } else {
      localStorage.removeItem(STORAGE_KEY)
    }
  }, [userId])

  if (userId === null) {
    return <UserSetup onSetup={setUserId} />
  }

  return <Dashboard userId={userId} onLogout={() => setUserId(null)} />
}
