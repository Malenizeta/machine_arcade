from games.torres_hanoi import TorresHanoi
from ia_client import solicitar_sugerencia

def solve_hanoi(n_discos):
    try:
        n_discos = int(n_discos)
        game = TorresHanoi(n_discos)
        moves = game.get_solucion()
        result_str = "\n".join(moves)
        return result_str
    except Exception as e:
        return f"Error: {e}"

def suggestion_hanoi(n_discos):
    try:
        n_discos = int(n_discos)
        game = TorresHanoi(n_discos)
        state = game.estado_a_json()
        suggestion = solicitar_sugerencia("TorresHanoi", state)
        return suggestion
    except Exception as e:
        return f"Error: {e}"


