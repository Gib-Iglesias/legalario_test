from fastapi import WebSocket
from typing import List, Dict
import json
import asyncio

class ConnectionManager:
    """Gestor de conexiones WebSocket para notificaciones en tiempo real"""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.user_connections: Dict[str, List[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, user_id: str = None):
        """Acepta una nueva conexión WebSocket"""
        await websocket.accept()
        self.active_connections.append(websocket)
        
        if user_id:
            if user_id not in self.user_connections:
                self.user_connections[user_id] = []
            self.user_connections[user_id].append(websocket)
    
    def disconnect(self, websocket: WebSocket, user_id: str = None):
        """Remueve una conexión WebSocket"""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        
        if user_id and user_id in self.user_connections:
            if websocket in self.user_connections[user_id]:
                self.user_connections[user_id].remove(websocket)
            if not self.user_connections[user_id]:
                del self.user_connections[user_id]
    
    async def send_personal_message(self, message: dict, websocket: WebSocket):
        """Envía un mensaje a una conexión específica"""
        try:
            await websocket.send_json(message)
        except Exception as e:
            print(f"Error enviando mensaje personal: {e}")
    
    async def broadcast(self, message: dict):
        """Envía un mensaje a todas las conexiones activas"""
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                print(f"Error en broadcast: {e}")
                disconnected.append(connection)
        
        # Limpiar conexiones muertas
        for conn in disconnected:
            self.disconnect(conn)
    
    async def broadcast_to_user(self, user_id: str, message: dict):
        """Envía un mensaje a todas las conexiones de un usuario específico"""
        if user_id in self.user_connections:
            disconnected = []
            for connection in self.user_connections[user_id]:
                try:
                    await connection.send_json(message)
                except Exception as e:
                    print(f"Error enviando a usuario {user_id}: {e}")
                    disconnected.append(connection)
            
            # Limpiar conexiones muertas
            for conn in disconnected:
                self.disconnect(conn, user_id)
    
    async def notify_transaction_change(self, transaction_data: dict):
        """Notifica cambios en una transacción a todos los clientes"""
        message = {
            "type": "transaction_update",
            "data": transaction_data,
            "timestamp": transaction_data.get("updated_at") or transaction_data.get("created_at")
        }
        await self.broadcast(message)
    
    async def notify_transaction_to_user(self, user_id: str, transaction_data: dict):
        """Notifica cambios en una transacción a un usuario específico"""
        message = {
            "type": "transaction_update",
            "data": transaction_data,
            "timestamp": transaction_data.get("updated_at") or transaction_data.get("created_at")
        }
        await self.broadcast_to_user(user_id, message)

# Instancia global del gestor de conexiones
manager = ConnectionManager()
