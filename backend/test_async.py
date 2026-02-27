"""
Script de prueba para el endpoint POST /transactions/async-process
Ejecutar después de iniciar el servidor y el worker de Celery
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000"

def create_transaction(user_id: str, monto: float, tipo: str):
    """Crea una transacción y retorna su ID"""
    payload = {
        "user_id": user_id,
        "monto": monto,
        "tipo": tipo
    }
    
    response = requests.post(
        f"{BASE_URL}/transactions/create",
        json=payload
    )
    
    return response.json()

def process_async(transaction_id: int):
    """Encola una transacción para procesamiento asíncrono"""
    payload = {
        "transaction_id": transaction_id
    }
    
    response = requests.post(
        f"{BASE_URL}/transactions/async-process",
        json=payload
    )
    
    return response.json()

def get_transaction(transaction_id: int):
    """Obtiene el estado actual de una transacción"""
    response = requests.get(f"{BASE_URL}/transactions/{transaction_id}")
    return response.json()

def test_async_processing():
    """Prueba completa del procesamiento asíncrono"""
    print("=" * 60)
    print("PRUEBA DE PROCESAMIENTO ASÍNCRONO")
    print("=" * 60)
    print()
    
    # Paso 1: Crear transacción
    print("📝 Paso 1: Creando transacción...")
    transaction = create_transaction("user_async_001", 500.00, "deposito")
    transaction_id = transaction["id"]
    print(f"✓ Transacción creada - ID: {transaction_id}")
    print(f"  Estado inicial: {transaction['estado']}")
    print()
    
    # Paso 2: Encolar para procesamiento
    print("📤 Paso 2: Encolando para procesamiento asíncrono...")
    async_response = process_async(transaction_id)
    print(f"✓ Transacción encolada")
    print(f"  Task ID: {async_response['task_id']}")
    print(f"  Status: {async_response['status']}")
    print()
    
    # Paso 3: Monitorear el estado
    print("⏳ Paso 3: Monitoreando el procesamiento...")
    max_attempts = 15
    attempt = 0
    
    while attempt < max_attempts:
        time.sleep(1)
        attempt += 1
        
        current_state = get_transaction(transaction_id)
        estado = current_state['estado']
        
        print(f"  [{attempt}] Estado: {estado}")
        
        if estado in ["procesado", "fallido"]:
            print()
            if estado == "procesado":
                print("✅ Transacción procesada exitosamente!")
            else:
                print("❌ Transacción falló durante el procesamiento")
            break
    else:
        print()
        print("⚠️  Timeout: La transacción sigue en procesamiento")
    
    print()
    print(f"Estado final: {json.dumps(current_state, indent=2)}")
    print()

def test_multiple_async():
    """Prueba procesamiento de múltiples transacciones"""
    print("=" * 60)
    print("PRUEBA DE MÚLTIPLES TRANSACCIONES ASÍNCRONAS")
    print("=" * 60)
    print()
    
    transactions = []
    
    # Crear y encolar 5 transacciones
    print("📝 Creando y encolando 5 transacciones...")
    for i in range(5):
        tx = create_transaction(f"user_{i}", 100.0 * (i + 1), "deposito")
        process_async(tx["id"])
        transactions.append(tx["id"])
        print(f"  ✓ Transacción {tx['id']} encolada")
    
    print()
    print("⏳ Esperando procesamiento (10 segundos)...")
    time.sleep(10)
    print()
    
    # Verificar estados
    print("📊 Estados finales:")
    for tx_id in transactions:
        state = get_transaction(tx_id)
        print(f"  ID {tx_id}: {state['estado']}")
    
    print()

def test_list_transactions():
    """Prueba el endpoint de listado"""
    print("=" * 60)
    print("PRUEBA DE LISTADO DE TRANSACCIONES")
    print("=" * 60)
    print()
    
    response = requests.get(f"{BASE_URL}/transactions/list?limit=10")
    transactions = response.json()
    
    print(f"Total de transacciones: {len(transactions)}")
    print()
    
    if transactions:
        print("Últimas transacciones:")
        for tx in transactions[:5]:
            print(f"  ID {tx['id']}: {tx['user_id']} - ${tx['monto']} - {tx['estado']}")
    
    print()

if __name__ == "__main__":
    try:
        # Verificar que el servidor esté corriendo
        health = requests.get(f"{BASE_URL}/health")
        print(f"✓ Servidor activo: {health.json()}")
        print()
        
        # Ejecutar pruebas
        test_async_processing()
        test_multiple_async()
        test_list_transactions()
        
        print("=" * 60)
        print("✅ Todas las pruebas completadas")
        print("=" * 60)
        print()
        print("💡 Nota: Asegúrate de que Redis y el worker de Celery estén corriendo:")
        print("   Terminal 1: docker-compose up redis")
        print("   Terminal 2: ./start_worker.sh")
        print("   Terminal 3: uvicorn app.main:app --reload")
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se puede conectar al servidor")
        print("Asegúrate de que el servidor esté corriendo en http://localhost:8000")
