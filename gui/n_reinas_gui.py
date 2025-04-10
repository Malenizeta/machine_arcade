# gui/n_reinas_gui.py

import tkinter as tk
from tkinter import messagebox
from games.n_reinas import NReinas
from ia_client import IAHelperThread

class NReinasGUI(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.n_reinas = None
        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self, text="Ingrese el número de reinas:")
        self.label.pack(pady=5)

        self.entry = tk.Entry(self)
        self.entry.pack(pady=5)

        self.btn_iniciar = tk.Button(self, text="Iniciar Juego", command=self.iniciar_juego)
        self.btn_iniciar.pack(pady=5)

        self.btn_ayuda = tk.Button(self, text="Ayuda IA", command=self.ayuda_ia)
        self.btn_ayuda.pack(pady=5)

        self.txt_resultado = tk.Text(self, height=10, width=50)
        self.txt_resultado.pack(pady=5)

    def iniciar_juego(self):
        try:
            n = int(self.entry.get())
            self.n_reinas = NReinas(n)
            solucion = self.n_reinas.get_solucion()
            self.txt_resultado.delete("1.0", tk.END)
            self.txt_resultado.insert(tk.END, f"Solución encontrada:\n{solucion}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al iniciar el juego: {e}")

    def ayuda_ia(self):
        if self.n_reinas is None:
            messagebox.showinfo("Información", "Inicie el juego primero.")
            return
        estado_json = self.n_reinas.estado_a_json()

        def callback(resultado):
            self.txt_resultado.insert(tk.END, f"\nSugerencia IA: {resultado}")

        hilo = IAHelperThread("NReinas", estado_json, callback)
        hilo.start()
