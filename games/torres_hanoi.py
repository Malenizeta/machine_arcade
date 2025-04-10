# games/torres_hanoi.py

class TorresHanoi:
    def __init__(self, n_discos):
        self.n_discos = n_discos
        self.origen = list(range(n_discos, 0, -1))
        self.auxiliar = []
        self.destino = []
        self.movimientos = []

    def mover_disco(self, origen, destino):
        disco = origen.pop()
        destino.append(disco)
        self.movimientos.append(f"Mover disco {disco}")

    def resolver(self, n, origen, destino, auxiliar):
        if n == 1:
            self.mover_disco(origen, destino)
        else:
            self.resolver(n - 1, origen, auxiliar, destino)
            self.mover_disco(origen, destino)
            self.resolver(n - 1, auxiliar, destino, origen)

    def get_solucion(self):
        self.movimientos = []
        self.resolver(self.n_discos, self.origen.copy(), self.destino, self.auxiliar.copy())
        return self.movimientos

    def estado_a_json(self):
        import json
        estado = {
            "origen": self.origen,
            "destino": self.destino,
            "auxiliar": self.auxiliar,
            "movimientos": self.movimientos
        }
        return json.dumps(estado)

