import base64
import requests
import json

from pydantic import BaseModel, Field
from typing import Dict, Any

# Define a classe de entrada para o pipeline
class Input(BaseModel):
    text: str = Field(..., description="O texto a ser gerado como áudio.")

# --- ALTERAÇÃO CRUCIAL ---
# A função handler deve ser parte de uma classe chamada Pipeline.
class Pipeline:
    def handler(self, input: Input, context: Dict[str, Any]) -> Dict[str, Any]:
     # URL do novo serviço API do Bark
     bark_url = "http://bark:5000/generate"

        payload = {"text": input.text}

        try:
            response = requests.post(
                bark_url,
                json=payload,
                timeout=120
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            return {"error": f"Erro ao comunicar com o servidor do Bark: {e}"}

        # O retorno agora é o arquivo WAV diretamente, não o JSON.
        audio_data = response.content
        audio_base64 = base64.b64encode(audio_data).decode('utf-8')

        return {
         "text": input.text,
         "type": "audio",
         "mime_type": "audio/wav",
         "data": audio_base64
        }
        