# server/server.py

import socket
import threading
import json
import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, DateTime, create_engine
from sqlalchemy.orm import sessionmaker

# Declaración de la base de los modelos
Base = declarative_base()

class GameResult(Base):
    __tablename__ = 'game_results'
    id = Column(Integer, primary_key=True)
    game_name = Column(String(50))
    details = Column(Text)  # Se almacena el JSON de detalles como texto
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

# Crear el motor SQLAlchemy con SQLite (archivo results.db)
engine = create_engine('sqlite:///results.db', echo=True)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

HOST = 'localhost'
PORT = 9999

def manejar_cliente(conn, addr):
    print(f"Conexión establecida desde {addr}")
    session = Session()
    with conn:
        while True:
            data = conn.recv(4096)
            if not data:
                break
            try:
                payload = json.loads(data.decode())
                game_name = payload.get("game_name", "Desconocido")
                # Convertir los detalles a cadena JSON
                details = json.dumps(payload.get("details", {}))
                resultado = GameResult(game_name=game_name, details=details)
                session.add(resultado)
                session.commit()
                print(f"Guardado resultado para el juego: {game_name}")
                conn.sendall(b"Resultado guardado")
            except Exception as e:
                session.rollback()
                error_msg = f"Error al guardar: {e}"
                print(error_msg)
                conn.sendall(error_msg.encode())
    session.close()
    print(f"Conexión cerrada desde {addr}")

def iniciar_servidor():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((HOST, PORT))
    servidor.listen()
    print(f"Servidor escuchando en {HOST}:{PORT}...")
    while True:
        conn, addr = servidor.accept()
        hilo_cliente = threading.Thread(target=manejar_cliente, args=(conn, addr))
        hilo_cliente.start()

if __name__ == "__main__":
    iniciar_servidor()
