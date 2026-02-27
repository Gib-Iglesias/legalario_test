"""
Script de prueba para el endpoint POST /transactions/create
Ejecutar después de iniciar el servidor
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_create_transaction():
    """Prueba básica de creación de transacción"""
    print("🧪 Test 1: Crear transacción nueva")

    payload = {
        "user_id": "user123",
        "monto": 100.50,
        "tipo": "deposito"
    }

    response = requests.post(
        f"{BASE_URL}/transactions/create",
        json=payload,
        headers={"X-Idempotency-Key": "test-key-001"}
    )

    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_idempotency():
    """Prueba de idempotencia"""
    print("🧪 Test 2: Verificar idempotencia (misma clave)")

    payload = {
        "user_id": "user456",
        "monto": 250.00,
        "tipo": "retiro"
    }

    # Primera llamada
    response1 = requests.post(
        f"{BASE_URL}/transactions/create",
        json=payload,
        headers={"X-Idempotency-Key": "test-key-002"}
    )

    # Segunda llamada con la misma clave
    response2 = requests.post(
        f"{BASE_URL}/transactions/create",
        json=payload,
        headers={"X-Idempotency-Key": "test-key-002"}
    )

    print(f"Primera llamada - ID: {response1.json()['id']}")
    print(f"Segunda llamada - ID: {response2.json()['id']}")
    print(f"¿Son iguales? {response1.json()['id'] == response2.json()['id']}")
    print()

def test_different_transaction_types():
    """Prueba diferentes tipos de transacciones"""
    print("🧪 Test 3: Diferentes tipos de transacciones")

    tipos = ["deposito", "retiro", "transferencia"]

    for i, tipo in enumerate(tipos):
        payload = {
            "user_id": f"user{i}",
            "monto": 100.0 * (i + 1),
            "tipo": tipo
        }

        response = requests.post(
            f"{BASE_URL}/transactions/create",
            json=payload,
            headers={"X-Idempotency-Key": f"test-key-{tipo}-{i}"}
        )

        print(f"✓ {tipo}: {response.status_code} - ID: {response.json()['id']}")
    print()

if __name__ == "__main__":
    print("=" * 50)
    print("PRUEBAS DEL ENDPOINT /transactions/create")
    print("=" * 50)
    print()

    try:
        # Verificar que el servidor esté corriendo
        health = requests.get(f"{BASE_URL}/health")
        print(f"✓ Servidor activo: {health.json()}")
        print()

        test_create_transaction()
        test_idempotency()
        test_different_transaction_types()

        print("=" * 50)
        print("✅ Todas las pruebas completadas")
        print("=" * 50)

    except requests.exceptions.ConnectionError:
        print("❌ Error: No se puede conectar al servidor")
        print("Asegúrate de que el servidor esté corriendo en http://localhost:8000")
