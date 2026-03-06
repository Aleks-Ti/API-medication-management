import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { api } from '../api'
import { type Manager } from '../types'
import { ManagerCard } from './ManagerCard'
import { ManagerModal } from './ManagerModal'

interface Props {
  userId: number
  onLogout: () => void
}

export function Dashboard({ userId, onLogout }: Props) {
  const [showCreate, setShowCreate] = useState(false)
  const [filter, setFilter] = useState<'all' | 'active' | 'inactive'>('all')

  const { data: managers = [], isLoading, isError, error } = useQuery<Manager[]>({
    queryKey: ['managers', userId],
    queryFn: () => api.getManagers(userId),
  })

  const filtered = managers.filter((m) => {
    if (filter === 'active') return m.is_active
    if (filter === 'inactive') return !m.is_active
    return true
  })

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <div className="header-brand">
          <span className="brand-icon">💊</span>
          <span className="brand-name">Medication Reminders</span>
        </div>
        <div className="header-right">
          <span className="user-id">ID: {userId}</span>
          <button className="btn btn-ghost btn-sm" onClick={onLogout}>
            Сменить
          </button>
        </div>
      </header>

      <main className="dashboard-main">
        <div className="toolbar">
          <div className="filter-tabs">
            {(['all', 'active', 'inactive'] as const).map((f) => (
              <button
                key={f}
                className={`filter-tab ${filter === f ? 'filter-tab-active' : ''}`}
                onClick={() => setFilter(f)}
              >
                {f === 'all' ? 'Все' : f === 'active' ? 'Активные' : 'Завершённые'}
              </button>
            ))}
          </div>
          <button className="btn btn-primary" onClick={() => setShowCreate(true)}>
            + Новый курс
          </button>
        </div>

        {isLoading && <p className="state-text">Загрузка...</p>}

        {isError && (
          <p className="state-text error-text">
            {(error as Error).message}
          </p>
        )}

        {!isLoading && !isError && filtered.length === 0 && (
          <div className="empty-state">
            <p>Нет курсов</p>
            <button className="btn btn-primary" onClick={() => setShowCreate(true)}>
              Добавить первый
            </button>
          </div>
        )}

        <div className="manager-list">
          {filtered.map((m) => (
            <ManagerCard key={m.id} manager={m} />
          ))}
        </div>
      </main>

      {showCreate && (
        <ManagerModal mode="create" userId={userId} onClose={() => setShowCreate(false)} />
      )}
    </div>
  )
}
