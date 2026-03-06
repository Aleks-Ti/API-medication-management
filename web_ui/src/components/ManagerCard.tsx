import { useState } from 'react'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { api, formatDate, formatTime } from '../api'
import { type Manager, type Regimen } from '../types'
import { ManagerModal } from './ManagerModal'
import { RegimenModal } from './RegimenModal'

interface Props {
  manager: Manager
}

export function ManagerCard({ manager }: Props) {
  const [showEdit, setShowEdit] = useState(false)
  const [showAddRegimen, setShowAddRegimen] = useState(false)
  const [editingRegimen, setEditingRegimen] = useState<Regimen | null>(null)
  const [expanded, setExpanded] = useState(true)

  const qc = useQueryClient()

  const deleteManagerMutation = useMutation({
    mutationFn: api.deleteManager,
    onSuccess: () => qc.invalidateQueries({ queryKey: ['managers'] }),
  })

  const deleteRegimenMutation = useMutation({
    mutationFn: api.deleteRegimen,
    onSuccess: () => qc.invalidateQueries({ queryKey: ['managers'] }),
  })

  const handleDeleteManager = () => {
    if (confirm(`Удалить курс "${manager.name}"?`)) {
      deleteManagerMutation.mutate(manager.id)
    }
  }

  const handleDeleteRegimen = (regimen: Regimen) => {
    if (confirm(`Удалить напоминание "${regimen.supplement}"?`)) {
      deleteRegimenMutation.mutate(regimen.id)
    }
  }

  return (
    <>
      <div className="card">
        <div className="card-header">
          <div className="card-title-row">
            <button
              className="btn-icon expand-btn"
              onClick={() => setExpanded((v) => !v)}
              aria-label={expanded ? 'Свернуть' : 'Развернуть'}
            >
              {expanded ? '▾' : '▸'}
            </button>
            <h3 className="card-title">{manager.name}</h3>
            <span className={`badge ${manager.is_active ? 'badge-active' : 'badge-inactive'}`}>
              {manager.is_active ? 'Активен' : 'Неактивен'}
            </span>
          </div>
          <div className="card-actions">
            <button className="btn btn-ghost btn-sm" onClick={() => setShowEdit(true)}>
              Изменить
            </button>
            <button
              className="btn btn-danger btn-sm"
              onClick={handleDeleteManager}
              disabled={deleteManagerMutation.isPending}
            >
              Удалить
            </button>
          </div>
        </div>

        {expanded && (
          <>
            <div className="card-meta">
              <span>{formatDate(manager.start_date)} — {formatDate(manager.finish_date)}</span>
              <span className="meta-sep">·</span>
              <span>{manager.timezone}</span>
            </div>

            <div className="regimens-section">
              <div className="regimens-header">
                <span className="section-label">Напоминания</span>
                <button className="btn btn-ghost btn-sm" onClick={() => setShowAddRegimen(true)}>
                  + Добавить
                </button>
              </div>

              {manager.regimens.length === 0 ? (
                <p className="section-hint">Нет напоминаний</p>
              ) : (
                <div className="regimen-list">
                  {manager.regimens.map((r) => (
                    <div key={r.id} className="regimen-row">
                      <span className={`chip ${r.is_active ? 'chip-active' : 'chip-inactive'}`}>
                        {formatTime(r.reception_time)}
                      </span>
                      <span className="regimen-supplement">{r.supplement}</span>
                      <div className="regimen-actions">
                        <button
                          className="btn-icon"
                          onClick={() => setEditingRegimen(r)}
                          aria-label="Редактировать"
                        >
                          ✎
                        </button>
                        <button
                          className="btn-icon btn-icon-danger"
                          onClick={() => handleDeleteRegimen(r)}
                          disabled={deleteRegimenMutation.isPending}
                          aria-label="Удалить"
                        >
                          ✕
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </>
        )}
      </div>

      {showEdit && (
        <ManagerModal mode="edit" manager={manager} onClose={() => setShowEdit(false)} />
      )}
      {showAddRegimen && (
        <RegimenModal mode="add" managerId={manager.id} onClose={() => setShowAddRegimen(false)} />
      )}
      {editingRegimen && (
        <RegimenModal mode="edit" regimen={editingRegimen} onClose={() => setEditingRegimen(null)} />
      )}
    </>
  )
}
