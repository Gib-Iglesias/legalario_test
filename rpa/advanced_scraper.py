"""
RPA Avanzado - Scraper con múltiples opciones
"""
import argparse
from wikipedia_scraper import WikipediaScraper
from playwright.sync_api import sync_playwright
import requests


class AdvancedScraper(WikipediaScraper):
    """
    Versión avanzada del scraper con más funcionalidades
    """
    
    def scrape_full_content(self, url: str, headless: bool = True) -> dict:
        """
        Extrae todo el contenido principal de la página
        """
        print(f"🤖 Scraping completo de: {url}")
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=headless)
            page = browser.new_page()
            
            try:
                page.goto(url, wait_until="domcontentloaded")
                page.wait_for_selector(".mw-parser-output", timeout=10000)
                
                # Extraer todo el contenido
                content = page.evaluate("""
                    () => {
                        const content = document.querySelector('.mw-content-container');
                        if (!content) return null;
                        
                        // Extraer todos los párrafos
                        const paragraphs = Array.from(content.querySelectorAll('p'))
                            .map(p => p.innerText.trim())
                            .filter(text => text.length > 50);
                        
                        return {
                            title: document.title,
                            paragraphs: paragraphs,
                            full_text: paragraphs.join('\\n\\n')
                        };
                    }
                """)
                
                return content
                
            finally:
                browser.close()
    
    def scrape_multiple_pages(self, urls: list, headless: bool = True) -> list:
        """
        Scrapea múltiples páginas y genera resúmenes
        """
        results = []
        
        for i, url in enumerate(urls, 1):
            print(f"\n📄 Procesando {i}/{len(urls)}: {url}")
            
            try:
                result = self.run(url, headless)
                results.append(result)
                print("✓ Completado")
            except Exception as e:
                print(f"✗ Error: {e}")
                results.append({"url": url, "error": str(e)})
        
        return results
    
    def search_and_scrape(self, search_term: str, headless: bool = True) -> dict:
        """
        Busca en Wikipedia y scrapea el primer resultado
        """
        print(f"🔍 Buscando: {search_term}")
        
        # Construir URL de búsqueda
        search_url = f"https://en.wikipedia.org/wiki/{search_term.replace(' ', '_')}"
        
        return self.run(search_url, headless)


def main():
    parser = argparse.ArgumentParser(
        description="RPA Avanzado - Wikipedia Scraper + AI Summarizer"
    )
    
    parser.add_argument(
        "url",
        nargs="?",
        default="https://en.wikipedia.org/wiki/Avengers:_Endgame",
        help="URL de Wikipedia a scrapear"
    )
    
    parser.add_argument(
        "--show",
        action="store_true",
        help="Mostrar el navegador (no headless)"
    )
    
    parser.add_argument(
        "--full",
        action="store_true",
        help="Extraer todo el contenido (no solo el primer párrafo)"
    )
    
    parser.add_argument(
        "--search",
        type=str,
        help="Buscar un término en Wikipedia"
    )
    
    parser.add_argument(
        "--multiple",
        nargs="+",
        help="Scrapear múltiples URLs"
    )
    
    args = parser.parse_args()
    
    scraper = AdvancedScraper()
    headless = not args.show
    
    try:
        if args.search:
            # Modo búsqueda
            result = scraper.search_and_scrape(args.search, headless)
            print(f"\n✨ Resumen: {result['summary']['summary']}")
            
        elif args.multiple:
            # Modo múltiple
            results = scraper.scrape_multiple_pages(args.multiple, headless)
            print(f"\n✅ Procesadas {len(results)} páginas")
            
        elif args.full:
            # Modo completo
            content = scraper.scrape_full_content(args.url, headless)
            print(f"\n📝 Extraídos {len(content['paragraphs'])} párrafos")
            
            # Resumir el contenido completo
            summary = scraper.send_to_summarizer(content['full_text'][:5000])
            print(f"\n✨ Resumen: {summary['summary']}")
            
        else:
            # Modo normal
            result = scraper.run(args.url, headless)
            print(f"\n✨ Resumen: {result['summary']['summary']}")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
