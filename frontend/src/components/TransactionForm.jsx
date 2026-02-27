import { useState } from 'react'
import './TransactionForm.css'

function TransactionForm({ onTransactionCreated }) {
  const [formData, setFormData] = useState({
    user_id: '',
    monto: '',
    tipo: 'deposito'
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)

    try {
      const response = await fetch('http://localhost:8000/transactions/create', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_id: formData.user_id,
          monto: parseFloat(formData.monto),
          tipo: formData.tipo
        })
      })

      if (!response.ok) {
        throw new Error('Error al crear la transacción')
      }

      const data = await response.json()
      onTransactionCreated(data)
      
      // Limpiar formulario
      setFormData({
        user_id: '',
        monto: '',
        tipo: 'deposito'
      })
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
  }

  return (
    <div className="card transaction-form">
      <h2>📝 Nueva Transacción</h2>
      
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="user_id">Usuario ID</label>
          <input
            type="text"
            id="user_id"
            name="user_id"
            value={formData.user_id}
            onChange={handleChange}
            placeholder="user123"
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="monto">Monto</label>
          <input
            type="number"
            id="monto"
            name="monto"
            value={formData.monto}
            onChange={handleChange}
            placeholder="100.00"
            step="0.01"
            min="0.01"
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="tipo">Tipo</label>
          <select
            id="tipo"
            name="tipo"
            value={formData.tipo}
            onChange={handleChange}
            required
          >
            <option value="deposito">Depósito</option>
            <option value="retiro">Retiro</option>
            <option value="transferencia">Transferencia</option>
          </select>
        </div>

        {error && (
          <div className="error-message">
            ❌ {error}
          </div>
        )}

        <button 
          type="submit" 
          className="btn-primary"
          disabled={loading}
        >
          {loading ? 'Creando...' : 'Crear Transacción'}
        </button>
      </form>
    </div>
  )
}

export default TransactionForm
