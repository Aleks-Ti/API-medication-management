import { useState, type FormEvent } from 'react'

interface Props {
  onSetup: (id: number) => void
}

export function UserSetup({ onSetup }: Props) {
  const [input, setInput] = useState('')
  const [error, setError] = useState('')

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault()
    const id = parseInt(input.trim())
    if (!id || id <= 0) {
      setError('Введите корректный Telegram User ID')
      return
    }
    onSetup(id)
  }

  return (
    <div className="setup-wrap">
      <div className="setup-card">
        <div className="setup-icon">💊</div>
        <h1>Medication Reminders</h1>
        <p>
          Введите ваш Telegram User ID, чтобы просмотреть и управлять расписанием
          приёма препаратов.
        </p>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <input
              type="number"
              placeholder="Telegram User ID"
              value={input}
              onChange={(e) => { setInput(e.target.value); setError('') }}
              autoFocus
            />
            {error && <span className="error-text">{error}</span>}
          </div>
          <button type="submit" className="btn btn-primary">
            Продолжить →
          </button>
        </form>
        <p className="section-hint" style={{ marginTop: 16 }}>
          ID можно узнать через бота @userinfobot в Telegram
        </p>
      </div>
    </div>
  )
}
