"""
Script de prueba para el endpoint POST /assistant/summarize
Ejecutar después de iniciar el servidor
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_summarize_short_text():
    """Prueba con un texto corto"""
    print("🧪 Test 1: Resumir texto corto")
    
    text = """
    Python es un lenguaje de programación de alto nivel, interpretado y de propósito general.
    Fue creado por Guido van Rossum y lanzado por primera vez en 1991.
    Python enfatiza la legibilidad del código y permite a los programadores expresar conceptos
    en menos líneas de código que en lenguajes como C++ o Java.
    """
    
    response = requests.post(
        f"{BASE_URL}/assistant/summarize",
        json={"text": text}
    )
    
    print(f"Status: {response.status_code}")
    if response.ok:
        data = response.json()
        print(f"\n📝 Texto original ({len(text)} caracteres):")
        print(text.strip())
        print(f"\n✨ Resumen generado:")
        print(data['summary'])
        print(f"\n📊 Metadata:")
        print(f"  - Modelo: {data['model_used']}")
        print(f"  - Tokens: {data['tokens_used']}")
        print(f"  - ID: {data['id']}")
    else:
        print(f"Error: {response.text}")
    print()

def test_summarize_long_text():
    """Prueba con un texto largo"""
    print("🧪 Test 2: Resumir texto largo")
    
    text = """
    La inteligencia artificial (IA) es la simulación de procesos de inteligencia humana por parte de máquinas,
    especialmente sistemas informáticos. Estos procesos incluyen el aprendizaje (la adquisición de información
    y reglas para usar la información), el razonamiento (usar reglas para llegar a conclusiones aproximadas o
    definitivas) y la autocorrección.
    
    Las aplicaciones particulares de la IA incluyen sistemas expertos, reconocimiento de voz y visión artificial.
    La IA se puede categorizar como débil o fuerte. La IA débil, también conocida como IA estrecha, es un sistema
    de IA diseñado y entrenado para una tarea particular. Los asistentes personales virtuales, como el Asistente
    de Google de Apple, son una forma de IA débil.
    
    La IA fuerte, también conocida como inteligencia artificial general, es un sistema de IA con capacidades
    cognitivas humanas generalizadas. Cuando se presenta con una tarea desconocida, un sistema de IA fuerte
    puede encontrar una solución sin intervención humana.
    
    El aprendizaje automático es un método de análisis de datos que automatiza la construcción de modelos
    analíticos. Es una rama de la inteligencia artificial basada en la idea de que los sistemas pueden aprender
    de datos, identificar patrones y tomar decisiones con mínima intervención humana.
    """
    
    response = requests.post(
        f"{BASE_URL}/assistant/summarize",
        json={"text": text}
    )
    
    print(f"Status: {response.status_code}")
    if response.ok:
        data = response.json()
        print(f"\n📝 Texto original ({len(text)} caracteres):")
        print(text.strip()[:200] + "...")
        print(f"\n✨ Resumen generado:")
        print(data['summary'])
        print(f"\n📊 Metadata:")
        print(f"  - Modelo: {data['model_used']}")
        print(f"  - Tokens: {data['tokens_used']}")
        print(f"  - ID: {data['id']}")
    else:
        print(f"Error: {response.text}")
    print()

def test_list_summaries():
    """Prueba listar resúmenes"""
    print("🧪 Test 3: Listar resúmenes")
    
    response = requests.get(f"{BASE_URL}/assistant/summaries?limit=5")
    
    print(f"Status: {response.status_code}")
    if response.ok:
        summaries = response.json()
        print(f"\n📋 Total de resúmenes: {len(summaries)}")
        
        for i, summary in enumerate(summaries, 1):
            print(f"\n{i}. Resumen #{summary['id']}")
            print(f"   Estado: {summary['status']}")
            print(f"   Modelo: {summary['model_used']}")
            print(f"   Tokens: {summary['tokens_used']}")
            print(f"   Creado: {summary['created_at']}")
    else:
        print(f"Error: {response.text}")
    print()

def test_get_stats():
    """Prueba obtener estadísticas"""
    print("🧪 Test 4: Estadísticas del asistente")
    
    response = requests.get(f"{BASE_URL}/assistant/stats")
    
    print(f"Status: {response.status_code}")
    if response.ok:
        stats = response.json()
        print(f"\n📊 Estadísticas:")
        print(f"  - Total de peticiones: {stats['total_requests']}")
        print(f"  - Por estado: {stats['by_status']}")
        print(f"  - Total de tokens: {stats['total_tokens_used']}")
    else:
        print(f"Error: {response.text}")
    print()

def test_wikipedia_example():
    """Prueba con un texto de ejemplo de Wikipedia"""
    print("🧪 Test 5: Texto de Wikipedia")
    
    text = """
    FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.7+
    based on standard Python type hints. The key features are: Fast: Very high performance, on par
    with NodeJS and Go (thanks to Starlette and Pydantic). One of the fastest Python frameworks available.
    Fast to code: Increase the speed to develop features by about 200% to 300%. Fewer bugs: Reduce about
    40% of human (developer) induced errors. Intuitive: Great editor support. Completion everywhere.
    Less time debugging. Easy: Designed to be easy to use and learn. Less time reading docs. Short:
    Minimize code duplication. Multiple features from each parameter declaration. Fewer bugs. Robust:
    Get production-ready code. With automatic interactive documentation. Standards-based: Based on
    (and fully compatible with) the open standards for APIs: OpenAPI and JSON Schema.
    """
    
    response = requests.post(
        f"{BASE_URL}/assistant/summarize",
        json={"text": text}
    )
    
    print(f"Status: {response.status_code}")
    if response.ok:
        data = response.json()
        print(f"\n📝 Texto sobre FastAPI")
        print(f"\n✨ Resumen:")
        print(data['summary'])
        print(f"\n📊 Tokens usados: {data['tokens_used']}")
    else:
        print(f"Error: {response.text}")
    print()

if __name__ == "__main__":
    print("=" * 70)
    print("PRUEBAS DEL ENDPOINT /assistant/summarize")
    print("=" * 70)
    print()
    
    try:
        # Verificar que el servidor esté corriendo
        health = requests.get(f"{BASE_URL}/health")
        print(f"✓ Servidor activo: {health.json()}")
        print()
        
        # Ejecutar pruebas
        test_summarize_short_text()
        test_summarize_long_text()
        test_wikipedia_example()
        test_list_summaries()
        test_get_stats()
        
        print("=" * 70)
        print("✅ Todas las pruebas completadas")
        print("=" * 70)
        print()
        print("💡 Nota:")
        print("   - Si no tienes API key de OpenAI, el sistema usa un mock")
        print("   - Para usar OpenAI real, configura OPENAI_API_KEY en .env")
        print("   - El mock genera resúmenes básicos para desarrollo")
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se puede conectar al servidor")
        print("Asegúrate de que el servidor esté corriendo en http://localhost:8000")
