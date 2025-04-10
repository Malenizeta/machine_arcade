# gui/n_reinas_gui.py

from games.n_reinas import NReinas
from ia_client import solicitar_sugerencia

def solve_n_reinas(n):
    try:
        n = int(n)
        game = NReinas(n)
        solution = game.get_solucion()
        result_str = "\n".join(" ".join(str(cell) for cell in row) for row in solution)
        return result_str
    except Exception as e:
        return f"Error: {e}"

def suggestion_n_reinas(n):
    try:
        n = int(n)
        game = NReinas(n)
        state = game.estado_a_json()
        suggestion = solicitar_sugerencia("NReinas", state)
        return suggestion
    except Exception as e:
        return f"Error: {e}"

