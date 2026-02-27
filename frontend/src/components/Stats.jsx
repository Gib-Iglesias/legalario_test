import { useState, useEffect } from 'react'
import './Stats.css'

function Stats() {
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchStats()
    const interval = setInterval(fetchStats, 5000) // Actualizar cada 5 segundos
    return () => clearInterval(interval)
  }, [])

  const fetchStats = async () => {
    try {
      const response = await fetch('http://localhost:8000/transactions/stats')
      const data = await response.json()
      setStats(data)
    } catch (error) {
      console.error('Error fetching stats:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="card stats">
        <h3>📊 Estadísticas</h3>
        <div className="loading-stats">Cargando...</div>
      </div>
    )
  }

  if (!stats) return null

  return (
    <div className="card stats">
      <h3>📊 Estadísticas</h3>
      
      <div className="stat-item">
        <span className="stat-label">Total Transacciones</span>
        <span className="stat-value">{stats.total}</span>
      </div>

      <div className="stat-section">
        <h4>Por Estado</h4>
        <div className="stat-item">
          <span className="stat-label">⏳ Pendientes</span>
          <span className="stat-value">{stats.by_status?.pendiente || 0}</span>
        </div>
        <div className="stat-item">
          <span className="stat-label">✅ Procesadas</span>
          <span className="stat-value">{stats.by_status?.procesado || 0}</span>
        </div>
        <div className="stat-item">
          <span className="stat-label">❌ Fallidas</span>
          <span className="stat-value">{stats.by_status?.fallido || 0}</span>
        </div>
      </div>

      <div className="stat-section">
        <h4>Por Tipo</h4>
        <div className="stat-item">
          <span className="stat-label">💵 Depósitos</span>
          <span className="stat-value">{stats.by_type?.deposito || 0}</span>
        </div>
        <div className="stat-item">
          <span className="stat-label">💸 Retiros</span>
          <span className="stat-value">{stats.by_type?.retiro || 0}</span>
        </div>
        <div className="stat-item">
          <span className="stat-label">🔄 Transferencias</span>
          <span className="stat-value">{stats.by_type?.transferencia || 0}</span>
        </div>
      </div>

      <div className="stat-item highlight">
        <span className="stat-label">🔌 Conexiones Activas</span>
        <span className="stat-value">{stats.active_websocket_connections}</span>
      </div>
    </div>
  )
}

export default Stats
