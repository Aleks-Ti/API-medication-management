import { useState, type FormEvent } from 'react'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { api, toApiTime, toApiDatetime, toDateInput } from '../api'
import { TIMEZONES, type Manager } from '../types'
import { Modal } from './Modal'

interface CreateProps {
  mode: 'create'
  userId: number
  onClose: () => void
}

interface EditProps {
  mode: 'edit'
  manager: Manager
  onClose: () => void
}

type Props = CreateProps | EditProps

export function ManagerModal(props: Props) {
  const isEdit = props.mode === 'edit'
  const manager = isEdit ? props.manager : null

  const [name, setName] = useState(manager?.name ?? '')
  const [startDate, setStartDate] = useState(manager ? toDateInput(manager.start_date) : '')
  const [finishDate, setFinishDate] = useState(manager ? toDateInput(manager.finish_date) : '')
  const [timezone, setTimezone] = useState(manager?.timezone ?? 'МСК')
  const [isActive, setIsActive] = useState(manager?.is_active ?? true)
  // Only for create mode — first regimen
  const [time, setTime] = useState('')
  const [supplement, setSupplement] = useState('')
  const [error, setError] = useState('')

  const qc = useQueryClient()

  const createMutation = useMutation({
    mutationFn: api.createManager,
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['managers'] })
      props.onClose()
    },
    onError: (e: Error) => setError(e.message),
  })

  const updateMutation = useMutation({
    mutationFn: ({ id, data }: { id: number; data: Parameters<typeof api.updateManager>[1] }) =>
      api.updateManager(id, data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['managers'] })
      props.onClose()
    },
    onError: (e: Error) => setError(e.message),
  })

  const isPending = createMutation.isPending || updateMutation.isPending

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault()
    setError('')

    if (!name || !startDate || !finishDate) {
      setError('Заполните все обязательные поля')
      return
    }

    if (isEdit && manager) {
      updateMutation.mutate({
        id: manager.id,
        data: {
          name,
          start_date: toApiDatetime(startDate),
          finish_date: toApiDatetime(finishDate),
          timezone,
          is_active: isActive,
        },
      })
    } else {
      if (!time || !supplement) {
        setError('Укажите время и описание первого напоминания')
        return
      }
      const userId = (props as CreateProps).userId
      createMutation.mutate({
        user_tg_id: userId,
        manager: {
          name,
          start_date: toApiDatetime(startDate),
          finish_date: toApiDatetime(finishDate),
          timezone,
          is_active: isActive,
        },
        regimen: {
          reception_time: toApiTime(time),
          supplement,
          is_active: true,
        },
      })
    }
  }

  return (
    <Modal title={isEdit ? 'Редактировать курс' : 'Новый курс'} onClose={props.onClose}>
      <form onSubmit={handleSubmit}>
        <div className="modal-body">
          <div className="form-group">
            <label>Название препарата / курса</label>
            <input
              type="text"
              placeholder="Vitamin D, Магний, Омега-3..."
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
            />
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Дата начала</label>
              <input
                type="date"
                value={startDate}
                onChange={(e) => setStartDate(e.target.value)}
                required
              />
            </div>
            <div className="form-group">
              <label>Дата окончания</label>
              <input
                type="date"
                value={finishDate}
                onChange={(e) => setFinishDate(e.target.value)}
                required
              />
            </div>
          </div>

          <div className="form-group">
            <label>Часовой пояс</label>
            <select value={timezone} onChange={(e) => setTimezone(e.target.value)}>
              {Object.entries(TIMEZONES).map(([val, label]) => (
                <option key={val} value={val}>{label}</option>
              ))}
            </select>
          </div>

          <div className="checkbox-row">
            <input
              type="checkbox"
              id="is-active"
              checked={isActive}
              onChange={(e) => setIsActive(e.target.checked)}
            />
            <label htmlFor="is-active" style={{ color: 'var(--text)', fontWeight: 400 }}>
              Курс активен
            </label>
          </div>

          {!isEdit && (
            <>
              <hr className="card-divider" />
              <p style={{ fontSize: 13, color: 'var(--text-muted)' }}>Первое напоминание</p>
              <div className="form-row">
                <div className="form-group">
                  <label>Время приёма</label>
                  <input
                    type="time"
                    value={time}
                    onChange={(e) => setTime(e.target.value)}
                  />
                </div>
                <div className="form-group">
                  <label>Описание</label>
                  <input
                    type="text"
                    placeholder="💊 После еды"
                    value={supplement}
                    onChange={(e) => setSupplement(e.target.value)}
                  />
                </div>
              </div>
            </>
          )}

          {error && <p className="error-text">{error}</p>}
        </div>

        <div className="modal-footer">
          <button type="button" className="btn btn-ghost" onClick={props.onClose}>
            Отмена
          </button>
          <button type="submit" className="btn btn-primary" disabled={isPending}>
            {isPending ? 'Сохранение...' : isEdit ? 'Сохранить' : 'Создать'}
          </button>
        </div>
      </form>
    </Modal>
  )
}
