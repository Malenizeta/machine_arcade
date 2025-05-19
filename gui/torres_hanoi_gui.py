import pygame
import sys
import os
import threading
import customtkinter as ctk
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from games import torres_hanoi as models
from client import enviar_resultado
from ia_client import IAHelperThread

# Define screen constants
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700
# Color constants object
color = models.ColorConstants()

FONT_PATH = os.path.join(os.path.dirname(__file__), "../assets/fonts/mario.ttf")  # Cambia esta ruta según tu estructura
FONT_SIZE = 25
TITLE_FONT_SIZE = 50

# Init pygame
pygame.init()

BACKGROUND_IMAGE_PATH = os.path.join(os.path.dirname(__file__), "../assets/images/Fondo.jpg")  # Cambia esta ruta según tu estructura
background_image = pygame.image.load(BACKGROUND_IMAGE_PATH)
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Redimensionar al tamaño de la pantalla

# Define the screen (and it's properties)
size = [SCREEN_WIDTH, SCREEN_HEIGHT]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Torres de Hanoi")
# Create main menu object
menu = models.MainMenu(SCREEN_WIDTH,SCREEN_HEIGHT)
# Create game object
game = models.Game(SCREEN_WIDTH,SCREEN_HEIGHT)
# Discs' move variables
done = False
drag = False
drop = False
move = False
game_over = False
init_game = False
disc_index = None
last_pos = [0,0]
font = pygame.font.Font(FONT_PATH, FONT_SIZE)
# Moves counter
moves_counter = 0
ia_button_rect = pygame.Rect(SCREEN_WIDTH - 140, 20, 120, 40)
# Manage how fast the screen updates
clock = pygame.time.Clock()

def ventana_ayuda_ia(sugerencia: str):
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("green")

    root = ctk.CTk()
    ruta_icono = os.path.join(os.path.dirname(__file__), "../assets/images/Icono.ico")
    root.iconbitmap(ruta_icono)
    root.title("Ayuda IA - Torres de Hanoi")
    root.geometry("450x280")
    root.resizable(False, False)

    txtbox = ctk.CTkTextbox(root, width=420, height=180, font=("Segoe UI", 11), wrap="word")
    txtbox.pack(padx=10, pady=(15, 10))
    txtbox.insert("0.0", sugerencia)
    txtbox.configure(state="disabled")

    btn_frame = ctk.CTkFrame(root, fg_color="transparent")
    btn_frame.pack(pady=(0, 15))

    btn_cerrar = ctk.CTkButton(
        btn_frame,
        text="Cerrar",
        fg_color="#4682B4",
        hover_color="#1E3C78",
        text_color="white",
        font=("Segoe UI", 11, "bold"),
        corner_radius=8,
        command=root.destroy
    )
    btn_cerrar.pack(side="left", padx=10)

    root.mainloop()

# -------- Main Game Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        # Manejar eventos del menú
        if not init_game:
            user_input = menu.handle_event(event)
            if user_input is not None:
                try:
                    # Validar que el número ingresado sea un entero positivo
                    n_discs = int(user_input)
                    if n_discs > 0:
                        game.set_n_discs(n_discs)
                        game.draw_discs()
                        init_game = True
                        game_over = False
                    else:
                        print("El número de discos debe ser mayor que 0.")
                except ValueError:
                    print("Por favor, ingresa un número válido.")
            if menu.btn_start.is_clicked():
                try:
                    n_discs = int(menu.input_text)
                    if n_discs > 0:
                        game.set_n_discs(n_discs)
                        game.draw_discs()
                        init_game = True
                        game_over = False
                    else:
                        print("El número de discos debe ser mayor que 0.")
                except ValueError:
                    print("Por favor, ingresa un número válido.")

        # Manejar eventos del juego
        elif init_game:
            if event.type == pygame.MOUSEBUTTONDOWN:
                drag = True
                drop = False
                if ia_button_rect.collidepoint(event.pos):
                    estado_texto = "Estado actual de las torres:\n"
                    for i, torre in enumerate(game.positions):
                        discos = [f"D{d.id}" for d in torre.discs]
                        estado_texto += f"Torre {i+1}: {' '.join(discos) if discos else '(vacía)'}\n"

                    def mostrar_sugerencia(resultado):
                        threading.Thread(target=ventana_ayuda_ia, args=(resultado,), daemon=True).start()

                    hilo = IAHelperThread(
                        "TorresHanoi",
                        estado_texto,
                        mostrar_sugerencia
                    )
                    hilo.start()
                    continue
                if not game_over:
                    for i in range(0, game.n_discs):
                        if game.discs[i].is_clicked():
                            current_pos = game.discs[i].current_pos
                            pos_length = len(game.positions[current_pos].discs)
                            if game.discs[i] == game.positions[current_pos].discs[pos_length - 1]:
                                disc_index = i
                                last_pos = [game.discs[i].rect.x, game.discs[i].rect.y]
                                move = True
                else:
                    if menu.btn_quit.is_clicked():
                        done = True

                    if menu.btn_play_again.is_clicked():
                        game.sprites_list.remove(game.discs)
                        game.positions[2].discs = []
                        moves_counter = 0
                        ia_button_rect = pygame.Rect(SCREEN_WIDTH - 140, 20, 120, 40)
                        game.discs = []
                        game.draw_discs()
                        game_over = False

                    if menu.btn_return.is_clicked():
                        # Reiniciar completamente el juego
                        game.sprites_list.empty()
                        game.pos_sprites_list.empty()
                        game.positions = []
                        game.discs = []
                        moves_counter = 0
                        game_over = False
                        init_game = False

                        # Recrear las posiciones del juego (pero sin discos)
                        game.__init__(SCREEN_WIDTH, SCREEN_HEIGHT)

                        # Reiniciar el menú
                        menu.sprites_list.empty()
                        menu.__init__(SCREEN_WIDTH, SCREEN_HEIGHT)
                    
                   
            elif event.type == pygame.MOUSEBUTTONUP:
                drag = False
                drop = True

    # Dibujar la pantalla
    screen.blit(background_image, (0, 0))

    if not init_game:
        # Dibujar el menú
        menu.draw(screen)
    else:
        # Dibujar el juego
        player_moves = font.render("Movimientos: " + str(moves_counter), True, color.BLACK)
        min_moves = font.render("Movimientos minimos: " + str(game.min_moves), True, color.BLACK)
        screen.blit(player_moves, [20, 20])
        screen.blit(min_moves, [20, 50])
        pygame.draw.rect(screen, (30, 60, 120), ia_button_rect)  # Rosa claro
        ia_font = pygame.font.Font(FONT_PATH, 20)
        ia_text = ia_font.render("Ayuda IA", True, (255, 255, 255))
        screen.blit(ia_text, (ia_button_rect.x + 10, ia_button_rect.y + 8))

        if game_over:
            menu.sprites_list.draw(screen)
            screen.blit(background_image, (0, 0))
            if len(game.positions[2].discs) == game.n_discs:
                if moves_counter == game.min_moves:
                    game_over_title = font.render(
                        "Enhorabuena! " \
                        "Has completado el juego con el minimo de movimientos",
                        True,
                        color.WHITE,
                    )
                    screen.blit(game_over_title, [((SCREEN_WIDTH / 2) - (game_over_title.get_width() / 2)), SCREEN_HEIGHT / 2 - 40])
                else:
                    game_over_title = font.render(
                        "Has completado el juego, pero no con el mínimo de movimientos",
                        True,
                        color.WHITE,
                    )
                    screen.blit(game_over_title, [((SCREEN_WIDTH / 2) - (game_over_title.get_width() / 2)), SCREEN_HEIGHT / 2])
        else:
            if drag:
                if move:
                    pos = pygame.mouse.get_pos()
                    game.discs[disc_index].rect.x = pos[0] - (game.discs[disc_index].width / 2)
                    game.discs[disc_index].rect.y = pos[1] - (game.discs[disc_index].height / 2)
            elif drop:
                if move:
                    current_pos = game.discs[disc_index].current_pos
                    new_pos = None
                    change = False
                    turn_back = True
                    position = pygame.sprite.spritecollideany(game.discs[disc_index], game.pos_sprites_list)
                    if position is not None:
                        new_pos = position.pos_index
                        if new_pos != current_pos:
                            disc_length = len(position.discs)
                            if disc_length == 0:
                                turn_back = False
                                change = True
                            elif game.discs[disc_index].id > position.discs[disc_length - 1].id:
                                turn_back = False
                                change = True
                    if change:
                        moves_counter += 1
                        game.positions[current_pos].discs.remove(game.discs[disc_index])
                        game.discs[disc_index].current_pos = new_pos
                        game.positions[new_pos].discs.append(game.discs[disc_index])
                        
                        # Ajustar posición horizontal
                        disc = game.discs[disc_index]
                        disc_width = disc.rect.width
                        disc.rect.x = game.positions[new_pos].rect.x - (disc_width // 2) + (game.POS_WIDTH // 2)

                        # Ajustar posición vertical
                        new_pos_length = len(game.positions[new_pos].discs)
                        disc_height = disc.rect.height
                        disc.rect.y = game.BOARD_Y - disc_height * new_pos_length

                        # Verificar si el juego ha terminado
                        if len(game.positions[2].discs) == game.n_discs:
                            game_over = True
                            menu.sprites_list.add([menu.btn_play_again, menu.btn_quit, menu.btn_return])
                            resultado = {
                            "num_discs": game.n_discs,
                            "moves": moves_counter,
                            "min_moves": game.min_moves,
                            "perfect": moves_counter == game.min_moves
                            }
                            enviar_resultado("Torres de Hanoi", resultado)
                    if turn_back:
                        game.discs[disc_index].rect.x = last_pos[0]
                        game.discs[disc_index].rect.y = last_pos[1]
                    move = False
        game.sprites_list.draw(screen)

    # Actualizar la pantalla
    pygame.display.flip()
    clock.tick(60)

pygame.quit()