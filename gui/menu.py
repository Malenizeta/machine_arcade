import gradio as gr
from gui.n_reinas_gui import solve_n_reinas, suggestion_n_reinas
from gui.caballo_gui import solve_caballo, suggestion_caballo
from gui.torres_hanoi_gui import solve_hanoi, suggestion_hanoi
from ia_client import consultar_chatbot

# CSS personalizado para un estilo retro
custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');

body {
    background-color: #000;
    color: #00FF00;
    font-family: 'Press Start 2P', cursive;
}
.gradio-container {
    background: #111;
    border: 2px solid #00FF00;
    border-radius: 8px;
    padding: 20px;
}
h1, h2, h3, .gradio-title, .md {
    color: #00FF00 !important;
}
.gradio-tab label {
    background-color: #222;
    border: 2px solid #00FF00;
    border-radius: 4px;
    padding: 5px 10px;
}
.gradio-button {
    background-color: #00FF00 !important;
    color: #000 !important;
    border: none;
    font-family: 'Press Start 2P', cursive;
    padding: 10px 20px;
    margin: 5px;
}
.gradio-textbox {
    background-color: #000;
    color: #00FF00;
    border: 2px solid #00FF00;
    font-family: 'Press Start 2P', cursive;
}
"""

def chatbot_response(question):
    try:
        response = consultar_chatbot(question)
        return response
    except Exception as e:
        return f"Error: {e}"

def build_interface():
    with gr.Blocks(css=custom_css) as demo:
        gr.Markdown("# Máquina Arcade Distribuida con IA - Retro Edition")
        
        with gr.Tab("N Reinas"):
            n_input = gr.Number(label="Número de reinas", value=8, precision=0)
            solve_btn = gr.Button("Resolver N Reinas")
            result_n = gr.Textbox(label="Solución", lines=10)
            ia_btn_n = gr.Button("Ayuda IA")
            ia_result_n = gr.Textbox(label="Sugerencia IA", lines=5)
            
            solve_btn.click(fn=solve_n_reinas, inputs=n_input, outputs=result_n)
            ia_btn_n.click(fn=suggestion_n_reinas, inputs=n_input, outputs=ia_result_n)
            
        with gr.Tab("Recorrido del Caballo"):
            size_input = gr.Number(label="Tamaño del tablero", value=8, precision=0)
            solve_btn_c = gr.Button("Resolver Recorrido del Caballo")
            result_c = gr.Textbox(label="Recorrido", lines=10)
            ia_btn_c = gr.Button("Ayuda IA")
            ia_result_c = gr.Textbox(label="Sugerencia IA", lines=5)
            
            solve_btn_c.click(fn=solve_caballo, inputs=size_input, outputs=result_c)
            ia_btn_c.click(fn=suggestion_caballo, inputs=size_input, outputs=ia_result_c)
            
        with gr.Tab("Torres de Hanói"):
            disks_input = gr.Number(label="Número de discos", value=3, precision=0)
            solve_btn_h = gr.Button("Resolver Torres de Hanói")
            result_h = gr.Textbox(label="Movimientos", lines=10)
            ia_btn_h = gr.Button("Ayuda IA")
            ia_result_h = gr.Textbox(label="Sugerencia IA", lines=5)
            
            solve_btn_h.click(fn=solve_hanoi, inputs=disks_input, outputs=result_h)
            ia_btn_h.click(fn=suggestion_hanoi, inputs=disks_input, outputs=ia_result_h)
            
        with gr.Tab("Chatbot"):
            chatbot_input = gr.Textbox(label="Pregunta sobre fórmulas o estrategias", lines=2)
            chatbot_btn = gr.Button("Consultar Chatbot")
            chatbot_output = gr.Textbox(label="Respuesta del Chatbot", lines=5)
            chatbot_btn.click(fn=chatbot_response, inputs=chatbot_input, outputs=chatbot_output)
            
    return demo

if __name__ == "__main__":
    demo = build_interface()
    demo.launch()

