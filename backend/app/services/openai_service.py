import os
from typing import Dict, Optional


class OpenAIService:
    """
    Servicio para interactuar con la API de OpenAI.
    Si no hay API key, usa un mock para desarrollo.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.use_mock = not api_key or api_key == "mock"
        
        if not self.use_mock:
            try:
                from openai import AsyncOpenAI
                self.client = AsyncOpenAI(api_key=api_key)
            except ImportError:
                print("⚠️  OpenAI library not installed. Using mock mode.")
                self.use_mock = True
    
    async def summarize(self, text: str) -> Dict:
        """
        Genera un resumen del texto proporcionado.
        
        Args:
            text: Texto a resumir
            
        Returns:
            Dict con: summary, model, tokens_used
        """
        if self.use_mock:
            return self._mock_summarize(text)
        
        try:
            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "Eres un asistente que genera resúmenes concisos y claros. Resume el texto en 2-3 oraciones capturando los puntos principales."
                    },
                    {
                        "role": "user",
                        "content": f"Resume el siguiente texto:\n\n{text}"
                    }
                ],
                max_tokens=150,
                temperature=0.7
            )
            
            summary = response.choices[0].message.content.strip()
            
            return {
                "summary": summary,
                "model": response.model,
                "tokens_used": response.usage.total_tokens
            }
            
        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            # Fallback a mock si falla la API
            return self._mock_summarize(text)
    
    def _mock_summarize(self, text: str) -> Dict:
        """
        Genera un resumen mock para desarrollo/testing.
        """
        words = text.split()
        word_count = len(words)
        
        # Tomar las primeras 30 palabras o menos
        summary_words = words[:min(30, word_count)]
        summary = " ".join(summary_words)
        
        if word_count > 30:
            summary += "..."
        
        # Agregar estadísticas básicas
        summary = f"[MOCK] Resumen del texto ({word_count} palabras): {summary}"
        
        return {
            "summary": summary,
            "model": "mock-gpt-3.5-turbo",
            "tokens_used": word_count + 50  # Simulado
        }
