# gui/caballo_gui.py

import tkinter as tk
from tkinter import messagebox
from games.caballo_tour import CaballoTour
from ia_client import IAHelperThread

class CaballoGUI(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.caballo = None
        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self, text="Tablero de Ajedrez (Recorrido del Caballo)")
        self.label.pack(pady=5)

        self.btn_iniciar = tk.Button(self, text="Iniciar Recorrido", command=self.iniciar_juego)
        self.btn_iniciar.pack(pady=5)

        self.btn_ayuda = tk.Button(self, text="Ayuda IA", command=self.ayuda_ia)
        self.btn_ayuda.pack(pady=5)

        self.txt_resultado = tk.Text(self, height=10, width=50)
        self.txt_resultado.pack(pady=5)

    def iniciar_juego(self):
        self.caballo = CaballoTour(tamaño=8)
        tour = self.caballo.get_tour((0, 0))
        self.txt_resultado.delete("1.0", tk.END)
        if tour:
            self.txt_resultado.insert(tk.END, f"Recorrido completado:\n{tour}")
        else:
            self.txt_resultado.insert(tk.END, "No se encontró recorrido")

    def ayuda_ia(self):
        if self.caballo is None:
            tk.messagebox.showinfo("Información", "Inicie el juego primero.")
            return
        estado_json = self.caballo.estado_a_json()

        def callback(resultado):
            self.txt_resultado.insert(tk.END, f"\nSugerencia IA: {resultado}")

        hilo = IAHelperThread("CaballoTour", estado_json, callback)
        hilo.start()
