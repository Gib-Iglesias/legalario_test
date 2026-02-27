"""
Script para ejecutar múltiples ejemplos del RPA
"""
from wikipedia_scraper import WikipediaScraper
import time


def run_examples():
    """Ejecuta varios ejemplos de scraping"""
    
    examples = [
        {
            "name": "Avengers: Endgame",
            "url": "https://en.wikipedia.org/wiki/Avengers:_Endgame"
        },
        {
            "name": "Python Programming",
            "url": "https://en.wikipedia.org/wiki/Python_(programming_language)"
        },
        {
            "name": "Artificial Intelligence",
            "url": "https://en.wikipedia.org/wiki/Artificial_intelligence"
        }
    ]
    
    scraper = WikipediaScraper()
    results = []
    
    print("🤖 Ejecutando múltiples ejemplos de RPA")
    print("=" * 70)
    print()
    
    for i, example in enumerate(examples, 1):
        print(f"\n📌 Ejemplo {i}/{len(examples)}: {example['name']}")
        print("-" * 70)
        
        try:
            result = scraper.run(example['url'], headless=True)
            results.append({
                "name": example['name'],
                "success": True,
                "result": result
            })
            
            print(f"✅ Completado: {example['name']}")
            
            # Esperar un poco entre requests
            if i < len(examples):
                print("\n⏳ Esperando 2 segundos...")
                time.sleep(2)
                
        except Exception as e:
            print(f"❌ Error en {example['name']}: {e}")
            results.append({
                "name": example['name'],
                "success": False,
                "error": str(e)
            })
    
    # Resumen final
    print("\n" + "=" * 70)
    print("📊 RESUMEN DE EJECUCIÓN")
    print("=" * 70)
    
    successful = sum(1 for r in results if r['success'])
    failed = len(results) - successful
    
    print(f"\n✅ Exitosos: {successful}/{len(results)}")
    print(f"❌ Fallidos: {failed}/{len(results)}")
    
    if successful > 0:
        print("\n📝 Resúmenes generados:")
        for r in results:
            if r['success']:
                summary = r['result']['summary']['summary']
                print(f"\n• {r['name']}:")
                print(f"  {summary[:100]}...")


if __name__ == "__main__":
    run_examples()
