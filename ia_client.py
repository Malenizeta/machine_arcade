# ia_client.py

import requests
import threading
import json

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
API_KEY = "miapikey"  # Reemplaza esto con tu API key real de Hugging Face

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def solicitar_sugerencia(juego, estado_texto):
    prompt = (
        f"Estoy jugando a '{juego}'.\n"
        f"Este es el estado actual del juego:\n{estado_texto}\n\n"
        "¿Cuál sería una buena recomendación o siguiente movimiento?"
    )

    payload = {
        "inputs": prompt,
        "parameters": {
            "temperature": 0.7,
            "max_new_tokens": 200,
            "do_sample": True,
            "top_p": 0.9
        }
    }

    response = requests.post(API_URL, headers=HEADERS, json=payload)

    if response.status_code == 200:
        result = response.json()
        return result[0]["generated_text"]
    else:
        return f"Error {response.status_code}: {response.text}"
    
def consultar_chatbot(pregunta):
    prompt = (
        f"Soy un estudiante y tengo una duda sobre resolución de problemas con lógica.\n"
        f"Pregunta: {pregunta}\n"
        f"Responde de forma clara y educativa:"
    )

    payload = {
        "inputs": prompt,
        "parameters": {
            "temperature": 0.6,
            "max_new_tokens": 300,
            "do_sample": True,
            "top_p": 0.9
        }
    }

    response = requests.post(API_URL, headers=HEADERS, json=payload)

    if response.status_code == 200:
        result = response.json()
        full_text = result[0]["generated_text"]

        # Elimina todo lo anterior a la última línea del prompt (lo que tú enviaste)
        respuesta_limpia = full_text.split("Responde de forma clara y educativa:")[-1].strip()
        return respuesta_limpia
    else:
        return f"Error {response.status_code}: {response.text}"


class IAHelperThread(threading.Thread):
    """
    Ejecuta una sugerencia de IA en un hilo para no bloquear la interfaz.
    """
    def __init__(self, juego, estado_texto, callback):
        super().__init__()
        self.juego = juego
        self.estado_texto = estado_texto
        self.callback = callback

    def run(self):
        try:
            resultado = solicitar_sugerencia(self.juego, self.estado_texto)
            self.callback(resultado)
        except Exception as e:
            self.callback(f"Error al conectar con la IA: {e}")
