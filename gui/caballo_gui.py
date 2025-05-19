import pygame, sys, os
import datetime
import threading
import tkinter as tk
from tkinter import scrolledtext
import customtkinter as ctk


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from games import caballo_tour as ct
from client import enviar_resultado
from ia_client import IAHelperThread

def ventana_ayuda_ia(sugerencia: str):
    ctk.set_appearance_mode("light")  
    ctk.set_default_color_theme("green")  

    root = ctk.CTk()
    ruta_icono = os.path.join(os.path.dirname(__file__), "../assets/images/Icono.ico")
    root.iconbitmap(ruta_icono)
    root.title("Ayuda IA - Caballo Tour")
    root.geometry("450x280")
    root.resizable(False, False)

    # Texto scrollable más pequeño
    txtbox = ctk.CTkTextbox(root, width=420, height=180, font=("Segoe UI", 11), wrap="word")
    txtbox.pack(padx=10, pady=(15, 10))
    txtbox.insert("0.0", sugerencia)
    txtbox.configure(state="disabled")

    btn_frame = ctk.CTkFrame(root, fg_color="transparent")
    btn_frame.pack(pady=(0, 15))

    # Botón cerrar ajustado
    btn_cerrar = ctk.CTkButton(
        btn_frame,
        text="Cerrar",
        fg_color="#68E054",
        hover_color="#55B946",
        text_color="white",
        font=("Segoe UI", 11, "bold"),
        corner_radius=8,
        command=root.destroy
    )
    btn_cerrar.pack(side="left", padx=10)

    root.mainloop()

def caballo_tour(n):
    pygame.init()
    cell_size = 60
    yoshi_image = pygame.image.load(os.path.join(os.path.dirname(__file__), "../assets/images/yoshi.png"))
    yoshi_image = pygame.transform.scale(yoshi_image, (cell_size, cell_size)) 
    huevo_image = pygame.image.load(os.path.join(os.path.dirname(__file__), "../assets/images/huevo.png"))
    huevo_image = pygame.transform.scale(huevo_image, (50, 60))
    screen = pygame.display.set_mode((n * cell_size, n * cell_size + 50))  # espacio extra para botón IA
    pygame.display.set_caption("Recorrido del Caballo")
    font = pygame.font.SysFont(None, 24)

    board = ct.create_board(n)
    move_num = 0
    current_pos = None
    recorrido_completo = False

    ia_button_rect = pygame.Rect(10, n * cell_size + 10, 120, 30)

    def estado_a_texto(board, current_pos, move_num, n):
        estado_str = f"Movimiento actual: {move_num}, Posición caballo: {current_pos}\nTablero:\n"
        for fila in board:
            # Cada celda es número (movimiento) o '.' si -1
            estado_str += " ".join(str(c) if c != -1 else "." for c in fila) + "\n"
        return estado_str

    def draw_board():
        screen.fill((85, 185, 70))  # fondo neutro para IA
        for row in range(n):
            for col in range(n):
                rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                color = (255, 255, 255) if (row + col) % 2 == 0 else (104, 224, 84)
                pygame.draw.rect(screen, color, rect)
                if board[row][col] != -1:
                    screen.blit(huevo_image, (col * cell_size, row * cell_size))
                    move_text = font.render(str(board[row][col]), True, (0, 100, 0))  
                    text_rect = move_text.get_rect(center=(col * cell_size + cell_size // 2, row * cell_size + cell_size // 2))
                    screen.blit(move_text, text_rect)
        if current_pos:
            screen.blit(yoshi_image, (current_pos[1] * cell_size, current_pos[0] * cell_size))

        # Dibuja botón IA
        pygame.draw.rect(screen, (104, 224, 84), ia_button_rect)
        ia_text = font.render("Ayuda IA", True, (255, 255, 255))
        screen.blit(ia_text, (ia_button_rect.x + 10, ia_button_rect.y + 5))
        pygame.display.flip()

    running = True
    while running:
        draw_board()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()

                if ia_button_rect.collidepoint(mx, my):
                    if current_pos is None:
                        print("Inicia el juego antes de pedir ayuda a la IA.")
                    else:
                        estado_texto = estado_a_texto(board, current_pos, move_num, n)  

                        def mostrar_sugerencia(resultado):
                            threading.Thread(target=ventana_ayuda_ia, args=(resultado,), daemon=True).start()

                        hilo = IAHelperThread(
                            "CaballoTour",
                            estado_texto,
                            mostrar_sugerencia 
                        )
                        hilo.start()
                    continue  # evita que siga evaluando clic como movimiento del caballo

                col = mx // cell_size
                row = my // cell_size
                if row >= n or col >= n:
                    continue  # fuera del tablero

                if current_pos is None:
                    current_pos = (row, col)
                    board[row][col] = move_num
                    move_num += 1
                else:
                    if board[row][col] == -1 and ct.is_valid_knight_move(current_pos[0], current_pos[1], row, col):
                        current_pos = (row, col)
                        board[row][col] = move_num
                        move_num += 1
                        if move_num == n * n:
                            print("¡Recorrido completo!")
                            enviar_resultado("Caballo Tour", {
                                "board_size": n,
                                "result": "won",
                                "moves": move_num,
                            })
                    else:
                        print("Movimiento inválido")

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    caballo_tour(8)
