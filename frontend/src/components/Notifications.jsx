import './Notifications.css'

function Notifications({ notifications }) {
  if (notifications.length === 0) return null

  const getNotificationClass = (type) => {
    switch (type) {
      case 'procesado': return 'notification-success'
      case 'fallido': return 'notification-error'
      case 'created': return 'notification-info'
      case 'processing': return 'notification-warning'
      default: return 'notification-info'
    }
  }

  const getNotificationEmoji = (type) => {
    switch (type) {
      case 'procesado': return '✅'
      case 'fallido': return '❌'
      case 'created': return '📝'
      case 'processing': return '⚡'
      default: return '🔔'
    }
  }

  return (
    <div className="notifications-container">
      {notifications.map((notification) => (
        <div
          key={notification.id}
          className={`notification ${getNotificationClass(notification.type)}`}
        >
          <span className="notification-emoji">
            {getNotificationEmoji(notification.type)}
          </span>
          <span className="notification-message">
            {notification.message}
          </span>
        </div>
      ))}
    </div>
  )
}

export default Notifications
