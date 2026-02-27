"""
Script de prueba para el WebSocket /transactions/stream
Ejecutar después de iniciar el servidor
"""
import asyncio
import websockets
import json
import requests
from datetime import datetime

BASE_URL = "http://localhost:8000"
WS_URL = "ws://localhost:8000/transactions/stream"

async def listen_to_stream(user_id: str = None):
    """Escucha el stream de transacciones"""
    url = WS_URL
    if user_id:
        url = f"{WS_URL}?user_id={user_id}"
    
    print(f"🔌 Conectando a WebSocket: {url}")
    
    try:
        async with websockets.connect(url) as websocket:
            print("✓ Conectado al WebSocket")
            print("📡 Esperando notificaciones...\n")
            
            # Escuchar mensajes
            async for message in websocket:
                data = json.loads(message)
                
                if data["type"] == "connection_established":
                    print(f"✓ {data['message']}")
                    if data.get("user_id"):
                        print(f"  Filtrando por usuario: {data['user_id']}")
                    print()
                
                elif data["type"] == "transaction_update":
                    tx = data["data"]
                    timestamp = data.get("timestamp", "")
                    
                    print("=" * 60)
                    print(f"🔔 NOTIFICACIÓN DE TRANSACCIÓN")
                    print(f"   Timestamp: {timestamp}")
                    print(f"   ID: {tx['id']}")
                    print(f"   Usuario: {tx['user_id']}")
                    print(f"   Monto: ${tx['monto']}")
                    print(f"   Tipo: {tx['tipo']}")
                    print(f"   Estado: {tx['estado']}")
                    print("=" * 60)
                    print()
                
                elif data["type"] == "pong":
                    print(f"🏓 Pong recibido")
    
    except websockets.exceptions.ConnectionClosed:
        print("\n❌ Conexión cerrada")
    except Exception as e:
        print(f"\n❌ Error: {e}")

async def test_websocket_with_transactions():
    """Prueba el WebSocket creando transacciones"""
    print("=" * 60)
    print("PRUEBA DE WEBSOCKET CON TRANSACCIONES")
    print("=" * 60)
    print()
    
    # Crear tarea para escuchar el WebSocket
    listener_task = asyncio.create_task(listen_to_stream())
    
    # Esperar un poco para que se establezca la conexión
    await asyncio.sleep(2)
    
    print("\n📝 Creando transacciones de prueba...\n")
    
    # Crear 3 transacciones
    for i in range(3):
        print(f"Creando transacción {i+1}...")
        
        response = requests.post(
            f"{BASE_URL}/transactions/create",
            json={
                "user_id": f"ws_test_user_{i}",
                "monto": 100.0 * (i + 1),
                "tipo": "deposito"
            }
        )
        
        if response.status_code == 201:
            tx = response.json()
            print(f"✓ Transacción {tx['id']} creada")
            
            # Encolar para procesamiento
            requests.post(
                f"{BASE_URL}/transactions/async-process",
                json={"transaction_id": tx["id"]}
            )
            print(f"✓ Transacción {tx['id']} encolada para procesamiento")
        
        await asyncio.sleep(1)
    
    print("\n⏳ Esperando notificaciones (15 segundos)...\n")
    
    # Esperar para recibir notificaciones
    await asyncio.sleep(15)
    
    # Cancelar el listener
    listener_task.cancel()
    try:
        await listener_task
    except asyncio.CancelledError:
        pass

async def test_simple_connection():
    """Prueba simple de conexión al WebSocket"""
    print("=" * 60)
    print("PRUEBA SIMPLE DE CONEXIÓN WEBSOCKET")
    print("=" * 60)
    print()
    
    try:
        async with websockets.connect(WS_URL) as websocket:
            print("✓ Conectado exitosamente")
            
            # Esperar mensaje de bienvenida
            message = await websocket.recv()
            data = json.loads(message)
            print(f"✓ Mensaje recibido: {data}")
            
            # Enviar ping
            print("\n🏓 Enviando ping...")
            await websocket.send("ping")
            
            # Esperar pong
            message = await websocket.recv()
            data = json.loads(message)
            print(f"✓ Respuesta: {data}")
            
            print("\n✅ Prueba de conexión exitosa")
    
    except Exception as e:
        print(f"❌ Error: {e}")

async def main():
    """Función principal"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 15 + "PRUEBAS DE WEBSOCKET" + " " * 23 + "║")
    print("╚" + "=" * 58 + "╝")
    print()
    
    try:
        # Verificar que el servidor esté corriendo
        health = requests.get(f"{BASE_URL}/health")
        print(f"✓ Servidor activo: {health.json()}")
        print()
        
        # Menú de opciones
        print("Selecciona una prueba:")
        print("1. Prueba simple de conexión")
        print("2. Prueba con creación de transacciones")
        print("3. Solo escuchar el stream (mantener abierto)")
        print()
        
        choice = input("Opción (1-3): ").strip()
        print()
        
        if choice == "1":
            await test_simple_connection()
        elif choice == "2":
            await test_websocket_with_transactions()
        elif choice == "3":
            print("Presiona Ctrl+C para detener\n")
            await listen_to_stream()
        else:
            print("Opción inválida")
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se puede conectar al servidor")
        print("Asegúrate de que el servidor esté corriendo en http://localhost:8000")
    except KeyboardInterrupt:
        print("\n\n👋 Prueba interrumpida por el usuario")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Adiós!")
