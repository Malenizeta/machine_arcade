# games/caballo_tour.py

class CaballoTour:
    def __init__(self, tamaño=8):
        self.tamaño = tamaño
        self.tablero = [[-1 for _ in range(tamaño)] for _ in range(tamaño)]
        self.movimientos = [(2, 1), (1, 2), (-1, 2), (-2, 1),
                            (-2, -1), (-1, -2), (1, -2), (2, -1)]

    def es_valido(self, x, y):
        return 0 <= x < self.tamaño and 0 <= y < self.tamaño and self.tablero[x][y] == -1

    def resolver(self, x, y, mov_count=0):
        self.tablero[x][y] = mov_count
        if mov_count == self.tamaño * self.tamaño - 1:
            return True
        for dx, dy in self.movimientos:
            nx, ny = x + dx, y + dy
            if self.es_valido(nx, ny):
                if self.resolver(nx, ny, mov_count + 1):
                    return True
        self.tablero[x][y] = -1
        return False

    def get_tour(self, inicio=(0, 0)):
        if self.resolver(inicio[0], inicio[1]):
            return self.tablero
        return None

    def estado_a_json(self):
        import json
        return json.dumps(self.tablero)
