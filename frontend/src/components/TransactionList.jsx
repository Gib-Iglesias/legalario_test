import './TransactionList.css'

function TransactionList({ transactions, loading, onProcess, onRefresh }) {
  const getStatusEmoji = (estado) => {
    switch (estado) {
      case 'procesado': return '✅'
      case 'fallido': return '❌'
      case 'pendiente': return '⏳'
      default: return '📄'
    }
  }

  const getStatusClass = (estado) => {
    switch (estado) {
      case 'procesado': return 'status-success'
      case 'fallido': return 'status-error'
      case 'pendiente': return 'status-pending'
      default: return ''
    }
  }

  const getTipoEmoji = (tipo) => {
    switch (tipo) {
      case 'deposito': return '💵'
      case 'retiro': return '💸'
      case 'transferencia': return '🔄'
      default: return '💰'
    }
  }

  if (loading) {
    return (
      <div className="card">
        <h2>📋 Transacciones</h2>
        <div className="loading">Cargando transacciones...</div>
      </div>
    )
  }

  return (
    <div className="card transaction-list">
      <div className="list-header">
        <h2>📋 Transacciones ({transactions.length})</h2>
        <button onClick={onRefresh} className="btn-refresh">
          🔄 Actualizar
        </button>
      </div>

      {transactions.length === 0 ? (
        <div className="empty-state">
          <p>No hay transacciones aún</p>
          <p className="empty-hint">Crea una nueva transacción para comenzar</p>
        </div>
      ) : (
        <div className="transactions">
          {transactions.map((tx) => (
            <div key={tx.id} className="transaction-item">
              <div className="transaction-header">
                <div className="transaction-id">
                  {getTipoEmoji(tx.tipo)} #{tx.id}
                </div>
                <div className={`transaction-status ${getStatusClass(tx.estado)}`}>
                  {getStatusEmoji(tx.estado)} {tx.estado}
                </div>
              </div>

              <div className="transaction-body">
                <div className="transaction-info">
                  <span className="label">Usuario:</span>
                  <span className="value">{tx.user_id}</span>
                </div>
                <div className="transaction-info">
                  <span className="label">Monto:</span>
                  <span className="value">${tx.monto.toFixed(2)}</span>
                </div>
                <div className="transaction-info">
                  <span className="label">Tipo:</span>
                  <span className="value">{tx.tipo}</span>
                </div>
                <div className="transaction-info">
                  <span className="label">Creada:</span>
                  <span className="value">
                    {new Date(tx.created_at).toLocaleString('es-ES')}
                  </span>
                </div>
              </div>

              {tx.estado === 'pendiente' && (
                <div className="transaction-actions">
                  <button
                    onClick={() => onProcess(tx.id)}
                    className="btn-process"
                  >
                    ⚡ Procesar
                  </button>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default TransactionList
