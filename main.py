# main.py

import gradio as gr
import threading
from games.n_reinas import NReinas
from games.caballo_tour import CaballoTour
from games.torres_hanoi import TorresHanoi
from ia_client import solicitar_sugerencia, consultar_chatbot

# Funciones para cada juego:

def solve_n_reinas(n):
    try:
        game = NReinas(int(n))
        solution = game.get_solucion()
        result_str = "\n".join(" ".join(str(cell) for cell in row) for row in solution)
        return result_str
    except Exception as e:
        return f"Error: {e}"

def ia_suggestion_n_reinas(n):
    try:
        game = NReinas(int(n))
        state = game.estado_a_json()
        suggestion = solicitar_sugerencia("NReinas", state)
        return suggestion
    except Exception as e:
        return f"Error: {e}"

def solve_caballo(tamaño):
    try:
        game = CaballoTour(int(tamaño))
        tour = game.get_tour((0, 0))
        result_str = "\n".join(" ".join(str(cell) for cell in row) for row in tour)
        return result_str
    except Exception as e:
        return f"Error: {e}"

def ia_suggestion_caballo(tamaño):
    try:
        game = CaballoTour(int(tamaño))
        state = game.estado_a_json()
        suggestion = solicitar_sugerencia("CaballoTour", state)
        return suggestion
    except Exception as e:
        return f"Error: {e}"

def solve_hanoi(n_discos):
    try:
        game = TorresHanoi(int(n_discos))
        moves = game.get_solucion()
        result_str = "\n".join(moves)
        return result_str
    except Exception as e:
        return f"Error: {e}"

def ia_suggestion_hanoi(n_discos):
    try:
        game = TorresHanoi(int(n_discos))
        state = game.estado_a_json()
        suggestion = solicitar_sugerencia("TorresHanoi", state)
        return suggestion
    except Exception as e:
        return f"Error: {e}"

def chatbot_response(question):
    try:
        response = consultar_chatbot(question)
        return response
    except Exception as e:
        return f"Error: {e}"

# Construcción de la interfaz de Gradio:
def build_interface():
    with gr.Blocks() as demo:
        gr.Markdown("# Máquina Arcade Distribuida con IA")
        
        with gr.Tab("N Reinas"):
            n_input = gr.Number(label="Número de reinas", value=8, precision=0)
            solve_btn = gr.Button("Resolver N Reinas")
            result_n = gr.Textbox(label="Solución", lines=10)
            ia_btn_n = gr.Button("Ayuda IA")
            ia_result_n = gr.Textbox(label="Sugerencia IA", lines=5)
            solve_btn.click(solve_n_reinas, inputs=n_input, outputs=result_n)
            ia_btn_n.click(ia_suggestion_n_reinas, inputs=n_input, outputs=ia_result_n)
            
        with gr.Tab("Recorrido del Caballo"):
            size_input = gr.Number(label="Tamaño del tablero", value=8, precision=0)
            solve_btn_c = gr.Button("Resolver Recorrido del Caballo")
            result_c = gr.Textbox(label="Recorrido", lines=10)
            ia_btn_c = gr.Button("Ayuda IA")
            ia_result_c = gr.Textbox(label="Sugerencia IA", lines=5)
            solve_btn_c.click(solve_caballo, inputs=size_input, outputs=result_c)
            ia_btn_c.click(ia_suggestion_caballo, inputs=size_input, outputs=ia_result_c)
            
        with gr.Tab("Torres de Hanói"):
            disks_input = gr.Number(label="Número de discos", value=3, precision=0)
            solve_btn_h = gr.Button("Resolver Torres de Hanói")
            result_h = gr.Textbox(label="Movimientos", lines=10)
            ia_btn_h = gr.Button("Ayuda IA")
            ia_result_h = gr.Textbox(label="Sugerencia IA", lines=5)
            solve_btn_h.click(solve_hanoi, inputs=disks_input, outputs=result_h)
            ia_btn_h.click(ia_suggestion_hanoi, inputs=disks_input, outputs=ia_result_h)
            
        with gr.Tab("Chatbot"):
            chatbot_input = gr.Textbox(label="Pregunta sobre fórmulas o estrategias", lines=2)
            chatbot_btn = gr.Button("Consultar Chatbot")
            chatbot_output = gr.Textbox(label="Respuesta del Chatbot", lines=5)
            chatbot_btn.click(chatbot_response, inputs=chatbot_input, outputs=chatbot_output)
            
    return demo

if __name__ == "__main__":
    # (Opcional) Iniciar el servidor en un hilo separado si se desea trabajar en local
    # from server.server import iniciar_servidor
    # import threading
    # threading.Thread(target=iniciar_servidor, daemon=True).start()
    
    demo = build_interface()
    demo.launch()
