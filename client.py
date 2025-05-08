import socket
import json
import threading

SERVER_HOST = 'localhost'
SERVER_PORT = 9999

def enviar_resultado(game_name, details):
    def enviar():
        try:
            with socket.create_connection((SERVER_HOST, SERVER_PORT)) as sock:
                payload = {
                    "game_name": game_name,
                    "details": details
                }
                sock.sendall(json.dumps(payload).encode())
                respuesta = sock.recv(1024)
                print("Servidor:", respuesta.decode())
        except Exception as e:
            print("Error al enviar al servidor:", e)

    threading.Thread(target=enviar).start()
