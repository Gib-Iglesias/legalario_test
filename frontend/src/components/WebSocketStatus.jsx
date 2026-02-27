import './WebSocketStatus.css'

function WebSocketStatus({ isConnected }) {
  return (
    <div className={`ws-status ${isConnected ? 'connected' : 'disconnected'}`}>
      <span className="ws-indicator"></span>
      <span className="ws-text">
        {isConnected ? 'Conectado' : 'Desconectado'}
      </span>
    </div>
  )
}

export default WebSocketStatus
