import gradio as gr
from gui.n_reinas_gui import solve_n_reinas, suggestion_n_reinas
from gui.caballo_gui import solve_caballo, suggestion_caballo
from gui.torres_hanoi_gui import solve_hanoi, suggestion_hanoi
from ia_client import consultar_chatbot

# CSS personalizado para simular una sala arcade retro.
custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');

body {
    background: url('https://i.imgur.com/8QwzV3f.png') no-repeat center center fixed;
    background-size: cover;
    color: #00FF00;
    font-family: 'Press Start 2P', cursive;
    margin: 0;
    padding: 0;
}
.gradio-container {
    background: rgba(0,0,0,0.85);
    border: 4px solid #00FF00;
    border-radius: 15px;
    padding: 20px;
    margin: 20px auto;
    max-width: 900px;
}
.gradio-title, h1, h2, h3, .md {
    color: #00FF00 !important;
}
.gradio-tab label {
    background-color: #222;
    border: 2px solid #00FF00;
    border-radius: 8px;
    padding: 10px 20px;
    cursor: pointer;
}
.gradio-button {
    background-color: #00FF00 !important;
    color: #000 !important;
    border: none;
    font-family: 'Press Start 2P', cursive;
    padding: 10px 20px;
    margin: 5px;
    border-radius: 8px;
}
.gradio-textbox {
    background-color: #000;
    color: #00FF00;
    border: 2px solid #00FF00;
    font-family: 'Press Start 2P', cursive;
    border-radius: 8px;
}
"""

# Función para responder al chatbot
def chatbot_response(question):
    try:
        response = consultar_chatbot(question)
        return response
    except Exception as e:
        return f"Error: {e}"

def build_interface():
    with gr.Blocks(css=custom_css) as demo:
        gr.Markdown("# Máquina Arcade Distribuida con IA\n### ¡Bienvenido al Arcade Retro!")
        
        with gr.Tabs():
            with gr.TabItem("N Reinas"):
                n_input = gr.Number(label="Número de reinas", value=8, precision=0)
                solve_btn = gr.Button("¡Jugar N Reinas!")
                result_n = gr.Textbox(label="Tablero y Solución", lines=10)
                ia_btn_n = gr.Button("Ayuda IA")
                ia_result_n = gr.Textbox(label="Consejo de la IA", lines=5)
                solve_btn.click(fn=solve_n_reinas, inputs=n_input, outputs=result_n)
                ia_btn_n.click(fn=suggestion_n_reinas, inputs=n_input, outputs=ia_result_n)
            
            with gr.TabItem("Recorrido del Caballo"):
                size_input = gr.Number(label="Tamaño del tablero", value=8, precision=0)
                solve_btn_c = gr.Button("¡Jugar Recorrido del Caballo!")
                result_c = gr.Textbox(label="Ruta del Caballo", lines=10)
                ia_btn_c = gr.Button("Ayuda IA")
                ia_result_c = gr.Textbox(label="Consejo de la IA", lines=5)
                solve_btn_c.click(fn=solve_caballo, inputs=size_input, outputs=result_c)
                ia_btn_c.click(fn=suggestion_caballo, inputs=size_input, outputs=ia_result_c)
            
            with gr.TabItem("Torres de Hanói"):
                disks_input = gr.Number(label="Número de discos", value=3, precision=0)
                solve_btn_h = gr.Button("¡Jugar Torres de Hanói!")
                result_h = gr.Textbox(label="Secuencia de Movimientos", lines=10)
                ia_btn_h = gr.Button("Ayuda IA")
                ia_result_h = gr.Textbox(label="Consejo de la IA", lines=5)
                solve_btn_h.click(fn=solve_hanoi, inputs=disks_input, outputs=result_h)
                ia_btn_h.click(fn=suggestion_hanoi, inputs=disks_input, outputs=ia_result_h)
            
            with gr.TabItem("Chatbot Arcade"):
                chatbot_input = gr.Textbox(label="Pregunta (e.g., '¿Cuál es la fórmula para Hanói?')", lines=2)
                chatbot_btn = gr.Button("Hablar con el Experto")
                chatbot_output = gr.Textbox(label="Respuesta del Experto", lines=5)
                chatbot_btn.click(fn=chatbot_response, inputs=chatbot_input, outputs=chatbot_output)
        
        gr.Markdown("### ¡Presiona los botones y diviértete en el Arcade Retro!")
    return demo

if __name__ == "__main__":
    demo = build_interface()
    demo.launch()


