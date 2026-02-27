import os
import sys
import requests
from playwright.sync_api import sync_playwright
from datetime import datetime
import json


class WikipediaScraper:
    def __init__(self, api_url: str = "http://localhost:8000"):
        self.api_url = api_url
        self.screenshots_dir = "screenshots"

        if not os.path.exists(self.screenshots_dir):
            os.makedirs(self.screenshots_dir)

    def scrape_wikipedia(self, url: str, headless: bool = True) -> dict:
        print(f"🤖 Iniciando RPA para: {url}")
        print(f"   Modo: {'Headless' if headless else 'Con interfaz'}")
        print()
        with sync_playwright() as p:
            # Lanzamos navegador
            browser = p.chromium.launch(headless=headless)
            page = browser.new_page()

            try:
                # Navegamos a la página
                print(f"📡 Navegando a {url}...")
                page.goto(url, wait_until="domcontentloaded")

                # Esperamos a que cargue el contenido
                page.wait_for_selector(".mw-parser-output", timeout=100000)
                print("✓ Página cargada")

                # Tomar screenshot
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                screenshot_path = f"{self.screenshots_dir}/wikipedia_{timestamp}.png"
                page.screenshot(path=screenshot_path)
                print(f"✓ Screenshot guardado: {screenshot_path}")

                # Extraer título
                title = page.title()
                print(f"✓ Título: {title}")

                first_paragraph = page.evaluate("""
                    () => {
                        const content = document.querySelector('.mw-content-container');
                        if (!content) return null;

                        const paragraphs = content.querySelectorAll('p');

                        for (let p of paragraphs) {
                            const text = p.innerText.trim();
                            if (text.length > 50 && !text.startsWith('Coordinates:')) {
                                return text;
                            }
                        }
                        return null;
                    }
                """)

                if not first_paragraph:
                    raise Exception("No se pudo extraer el primer párrafo")

                print(f"✓ Primer párrafo extraído ({len(first_paragraph)} caracteres)")
                print()

                result = {
                    "url": url,
                    "title": title,
                    "first_paragraph": first_paragraph,
                    "timestamp": timestamp,
                    "screenshot": screenshot_path
                }
                
                return result
                
            except Exception as e:
                print(f"❌ Error durante el scraping: {e}")
                raise
            
            finally:
                browser.close()
    
    def send_to_summarizer(self, text: str) -> dict:
        print("📤 Enviando texto al asistente de IA...")
        
        try:
            response = requests.post(
                f"{self.api_url}/assistant/summarize",
                json={"text": text},
                timeout=30
            )
            
            response.raise_for_status()
            data = response.json()
            
            print("✓ Resumen generado exitosamente")
            print()
            
            return data
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error al comunicarse con el API: {e}")
            raise
    
    def run(self, url: str, headless: bool = True) -> dict:
        print("=" * 70)
        print("🤖 RPA - WIKIPEDIA SCRAPER + AI SUMMARIZER")
        print("=" * 70)
        print()
        
        # Paso 1: Scrapear Wikipedia
        scrape_result = self.scrape_wikipedia(url, headless)
        
        # Paso 2: Enviar al asistente
        summary_result = self.send_to_summarizer(scrape_result["first_paragraph"])
        
        # Combinar resultados
        final_result = {
            **scrape_result,
            "summary": summary_result
        }
        
        # Guardar resultado en JSON
        output_file = f"{self.screenshots_dir}/result_{scrape_result['timestamp']}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(final_result, f, indent=2, ensure_ascii=False)
        
        print("=" * 70)
        print("✅ PROCESO COMPLETADO")
        print("=" * 70)
        print()
        print(f"📄 Título: {scrape_result['title']}")
        print(f"📝 Texto original: {len(scrape_result['first_paragraph'])} caracteres")
        print(f"✨ Resumen: {len(summary_result['summary'])} caracteres")
        print(f"🤖 Modelo: {summary_result['model_used']}")
        print(f"🎯 Tokens: {summary_result['tokens_used']}")
        print(f"📸 Screenshot: {scrape_result['screenshot']}")
        print(f"💾 Resultado: {output_file}")
        print()
        
        return final_result


def main():
    """Función principal"""
    # URL por defecto
    default_url = "https://en.wikipedia.org/wiki/Avengers:_Endgame"
    
    # Obtener URL de argumentos o usar default
    url = sys.argv[1] if len(sys.argv) > 1 else default_url
    
    # Modo headless (puede cambiarse a False para ver el navegador)
    headless = True
    if len(sys.argv) > 2 and sys.argv[2] == "--show":
        headless = False
    
    # Crear scraper
    scraper = WikipediaScraper()
    
    try:
        # Ejecutar RPA
        result = scraper.run(url, headless)
        
        # Mostrar resumen
        print("📋 RESUMEN GENERADO:")
        print("-" * 70)
        print(result["summary"]["summary"])
        print("-" * 70)
        print()
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Error fatal: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
