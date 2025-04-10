# main.py

import threading
import tkinter as tk
from gui.menu import MenuGUI

def iniciar_servidor_local():
    from server.server import iniciar_servidor
    hilo_servidor = threading.Thread(target=iniciar_servidor, daemon=True)
    hilo_servidor.start()

def main():
    # Iniciar el servidor localmente
    iniciar_servidor_local()

    # Crear y mostrar la GUI principal
    root = tk.Tk()
    root.title("Máquina Arcade Distribuida con IA")
    app = MenuGUI(master=root)
    app.mainloop()

if __name__ == "__main__":
    main()
