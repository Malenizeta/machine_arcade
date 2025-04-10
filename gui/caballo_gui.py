from games.caballo_tour import CaballoTour
from ia_client import solicitar_sugerencia

def solve_caballo(tamaño):
    try:
        tamaño = int(tamaño)
        game = CaballoTour(tamaño)
        tour = game.get_tour((0, 0))
        if tour is None:
            return "No se encontró solución."
        result_str = "\n".join(" ".join(str(cell) for cell in row) for row in tour)
        return result_str
    except Exception as e:
        return f"Error: {e}"

def suggestion_caballo(tamaño):
    try:
        tamaño = int(tamaño)
        game = CaballoTour(tamaño)
        state = game.estado_a_json()
        suggestion = solicitar_sugerencia("CaballoTour", state)
        return suggestion
    except Exception as e:
        return f"Error: {e}"



