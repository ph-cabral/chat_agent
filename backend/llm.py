import httpx
import os
import json

class LLMClient:
    def __init__(self):
        self.base_url = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        # self.model = "llama3.1:8b"
        self.model = "llama3.2:3b"  # ← Modelo más pequeño
    
    def generate_answer(self, question: str, context: str) -> str:
        prompt = f"""Eres un asistente de RRHH. Responde la pregunta basándote SOLO en el contexto proporcionado.
Si la información no está en el contexto, di que no tienes esa información.

Contexto:
{context}

Pregunta: {question}

Respuesta:"""
        
        try:
            response = httpx.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=60.0
            )
            
            if response.status_code != 200:
                return f"Error: Ollama respondió con código {response.status_code}"
            
            data = response.json()
            
            # Verificar que 'response' exista en la respuesta
            if 'response' not in data:
                return f"Error: Respuesta inesperada de Ollama. Data: {json.dumps(data)}"
            
            return data['response']
            
        except httpx.ConnectError:
            return "Error: No se puede conectar con Ollama. ¿Está corriendo?"
        except httpx.TimeoutException:
            return "Error: Timeout esperando respuesta de Ollama (puede ser que el modelo esté descargándose)"
        except Exception as e:
            return f"Error al generar respuesta: {str(e)}"
    
    def is_healthy(self) -> bool:
        try:
            response = httpx.get(f"{self.base_url}/api/tags", timeout=5.0)
            return response.status_code == 200
        except:
            return False