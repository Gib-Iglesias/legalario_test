import { useState, useEffect } from 'react'
import TransactionForm from './components/TransactionForm'
import TransactionList from './components/TransactionList'
import WebSocketStatus from './components/WebSocketStatus'
import Notifications from './components/Notifications'
import Stats from './components/Stats'
import SummaryTool from './components/SummaryTool'
import { useWebSocket } from './hooks/useWebSocket'
import './App.css'

function App() {
  const [transactions, setTransactions] = useState([])
  const [loading, setLoading] = useState(true)
  const [notifications, setNotifications] = useState([])
  const { isConnected, lastMessage } = useWebSocket('ws://localhost:8000/transactions/stream')

  // Cargar transacciones iniciales
  useEffect(() => {
    fetchTransactions()
  }, [])

  // Escuchar mensajes del WebSocket
  useEffect(() => {
    if (lastMessage) {
      handleWebSocketMessage(lastMessage)
    }
  }, [lastMessage])

  const fetchTransactions = async () => {
    try {
      const response = await fetch('http://localhost:8000/transactions/list?limit=50')
      const data = await response.json()
      setTransactions(data)
    } catch (error) {
      console.error('Error fetching transactions:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleWebSocketMessage = (message) => {
    if (message.type === 'transaction_update') {
      const updatedTx = message.data
      
      // Actualizar la lista de transacciones
      setTransactions(prev => {
        const index = prev.findIndex(tx => tx.id === updatedTx.id)
        if (index >= 0) {
          // Actualizar transacción existente
          const newTransactions = [...prev]
          newTransactions[index] = updatedTx
          return newTransactions
        } else {
          // Agregar nueva transacción
          return [updatedTx, ...prev]
        }
      })

      // Agregar notificación
      addNotification({
        id: Date.now(),
        type: updatedTx.estado,
        message: `Transacción #${updatedTx.id} - ${updatedTx.estado}`,
        transaction: updatedTx
      })
    }
  }

  const addNotification = (notification) => {
    setNotifications(prev => [notification, ...prev].slice(0, 5))
    
    // Auto-remover después de 5 segundos
    setTimeout(() => {
      setNotifications(prev => prev.filter(n => n.id !== notification.id))
    }, 5000)
  }

  const handleTransactionCreated = (newTransaction) => {
    setTransactions(prev => [newTransaction, ...prev])
    addNotification({
      id: Date.now(),
      type: 'created',
      message: `Transacción #${newTransaction.id} creada`,
      transaction: newTransaction
    })
  }

  const handleProcessTransaction = async (transactionId) => {
    try {
      const response = await fetch('http://localhost:8000/transactions/async-process', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ transaction_id: transactionId })
      })
      
      if (response.ok) {
        addNotification({
          id: Date.now(),
          type: 'processing',
          message: `Transacción #${transactionId} encolada para procesamiento`
        })
      }
    } catch (error) {
      console.error('Error processing transaction:', error)
    }
  }

  return (
    <div className="app">
      <header className="app-header">
        <div className="container">
          <h1>💰 Transactions App</h1>
          <WebSocketStatus isConnected={isConnected} />
        </div>
      </header>

      <main className="container">
        <Notifications notifications={notifications} />
        
        <div className="grid">
          <div className="col-left">
            <TransactionForm onTransactionCreated={handleTransactionCreated} />
            <Stats />
          </div>
          
          <div className="col-right">
            <TransactionList 
              transactions={transactions}
              loading={loading}
              onProcess={handleProcessTransaction}
              onRefresh={fetchTransactions}
            />
          </div>
        </div>

        <div className="full-width-section">
          <SummaryTool />
        </div>
      </main>
    </div>
  )
}

export default App
