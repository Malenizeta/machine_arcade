# gui/menu.py

import tkinter as tk
from gui.n_reinas_gui import NReinasGUI
from gui.caballo_gui import CaballoGUI
from gui.torres_hanoi_gui import TorresHanoiGUI

class MenuGUI(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_menu()

    def create_menu(self):
        self.label = tk.Label(self, text="Bienvenido a la Máquina Arcade Distribuida con IA")
        self.label.pack(pady=10)
        
        self.btn_n_reinas = tk.Button(self, text="Juego: N Reinas", command=self.abrir_n_reinas)
        self.btn_n_reinas.pack(pady=5)
        
        self.btn_caballo = tk.Button(self, text="Juego: Recorrido del Caballo", command=self.abrir_caballo)
        self.btn_caballo.pack(pady=5)
        
        self.btn_hanoi = tk.Button(self, text="Juego: Torres de Hanói", command=self.abrir_hanoi)
        self.btn_hanoi.pack(pady=5)
        
        self.btn_salir = tk.Button(self, text="Salir", command=self.master.quit)
        self.btn_salir.pack(pady=10)

    def abrir_n_reinas(self):
        ventana = tk.Toplevel(self.master)
        ventana.title("Juego N Reinas")
        app = NReinasGUI(master=ventana)
        app.mainloop()

    def abrir_caballo(self):
        ventana = tk.Toplevel(self.master)
        ventana.title("Recorrido del Caballo")
        app = CaballoGUI(master=ventana)
        app.mainloop()

    def abrir_hanoi(self):
        ventana = tk.Toplevel(self.master)
        ventana.title("Torres de Hanói")
        app = TorresHanoiGUI(master=ventana)
        app.mainloop()
