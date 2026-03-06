import { useState, type FormEvent } from 'react'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { api, toApiTime, formatTime } from '../api'
import { type Regimen } from '../types'
import { Modal } from './Modal'

interface AddProps {
  mode: 'add'
  managerId: number
  onClose: () => void
}

interface EditProps {
  mode: 'edit'
  regimen: Regimen
  onClose: () => void
}

type Props = AddProps | EditProps

export function RegimenModal(props: Props) {
  const isEdit = props.mode === 'edit'
  const regimen = isEdit ? props.regimen : null

  const [time, setTime] = useState(regimen ? formatTime(regimen.reception_time) : '')
  const [supplement, setSupplement] = useState(regimen?.supplement ?? '')
  const [isActive, setIsActive] = useState(regimen?.is_active ?? true)
  const [error, setError] = useState('')

  const qc = useQueryClient()

  const addMutation = useMutation({
    mutationFn: api.addRegimen,
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['managers'] })
      props.onClose()
    },
    onError: (e: Error) => setError(e.message),
  })

  const updateMutation = useMutation({
    mutationFn: ({ id, data }: { id: number; data: Parameters<typeof api.updateRegimen>[1] }) =>
      api.updateRegimen(id, data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['managers'] })
      props.onClose()
    },
    onError: (e: Error) => setError(e.message),
  })

  const isPending = addMutation.isPending || updateMutation.isPending

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault()
    setError('')

    if (!time || !supplement) {
      setError('Заполните все поля')
      return
    }

    if (isEdit && regimen) {
      updateMutation.mutate({
        id: regimen.id,
        data: {
          reception_time: toApiTime(time),
          supplement,
          is_active: isActive,
        },
      })
    } else {
      const managerId = (props as AddProps).managerId
      addMutation.mutate({
        manager_id: managerId,
        reception_time: toApiTime(time),
        supplement,
        is_active: isActive,
      })
    }
  }

  return (
    <Modal title={isEdit ? 'Редактировать напоминание' : 'Новое напоминание'} onClose={props.onClose}>
      <form onSubmit={handleSubmit}>
        <div className="modal-body">
          <div className="form-row">
            <div className="form-group">
              <label>Время приёма</label>
              <input
                type="time"
                value={time}
                onChange={(e) => setTime(e.target.value)}
                required
              />
            </div>
            <div className="form-group">
              <label>Описание</label>
              <input
                type="text"
                placeholder="💊 После еды"
                value={supplement}
                onChange={(e) => setSupplement(e.target.value)}
                required
              />
            </div>
          </div>

          <div className="checkbox-row">
            <input
              type="checkbox"
              id="regimen-active"
              checked={isActive}
              onChange={(e) => setIsActive(e.target.checked)}
            />
            <label htmlFor="regimen-active" style={{ color: 'var(--text)', fontWeight: 400 }}>
              Напоминание активно
            </label>
          </div>

          {error && <p className="error-text">{error}</p>}
        </div>

        <div className="modal-footer">
          <button type="button" className="btn btn-ghost" onClick={props.onClose}>
            Отмена
          </button>
          <button type="submit" className="btn btn-primary" disabled={isPending}>
            {isPending ? 'Сохранение...' : isEdit ? 'Сохранить' : 'Добавить'}
          </button>
        </div>
      </form>
    </Modal>
  )
}
