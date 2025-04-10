# ia_client.py

import requests
import json
import threading

API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
API_KEY = "TU_API_KEY_AQUI"  # Reemplaza con tu API key
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def solicitar_sugerencia(juego, estado_json):
    payload = {
        "juego": juego,
        "estado": json.loads(estado_json)
    }
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    return response.text

def consultar_chatbot(pregunta):
    payload = {"pregunta": pregunta}
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    return response.text

class IAHelperThread(threading.Thread):
    """
    Esta clase ejecuta la solicitud a la API en un hilo para evitar bloquear la interfaz.
    El parámetro callback es una función que recibe el resultado cuando esté disponible.
    """
    def __init__(self, juego, estado_json, callback):
        super().__init__()
        self.juego = juego
        self.estado_json = estado_json
        self.callback = callback

    def run(self):
        try:
            resultado = solicitar_sugerencia(self.juego, self.estado_json)
            self.callback(resultado)
        except Exception as e:
            self.callback(f"Error al conectar con la IA: {e}")
