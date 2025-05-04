# # gui/torres_hanoi_gui.py
import pygame
import sys
import games.torres_hanoi as models
import os

# Define screen constants
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700
# Color constants object
color = models.ColorConstants()

FONT_PATH = os.path.join(os.path.dirname(__file__), "../assets/fonts/arcade.ttf")  # Cambia esta ruta según tu estructura
FONT_SIZE = 30
TITLE_FONT_SIZE = 50

# Init pygame
pygame.init()

BACKGROUND_IMAGE_PATH = os.path.join(os.path.dirname(__file__), "../assets/images/Fondo.jpg")  # Cambia esta ruta según tu estructura
background_image = pygame.image.load(BACKGROUND_IMAGE_PATH)
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Redimensionar al tamaño de la pantalla

# Define the screen (and it's properties)
size = [SCREEN_WIDTH, SCREEN_HEIGHT]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("MG's Tower of Hanoi for Python")
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
# Manage how fast the screen updates
clock = pygame.time.Clock()
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
        player_moves = font.render("Player moves: " + str(moves_counter), True, color.BLACK)
        min_moves = font.render("Minimum of required movements: " + str(game.min_moves), True, color.BLACK)
        screen.blit(player_moves, [20, 80])
        screen.blit(min_moves, [20, 110])

        if game_over:
            menu.sprites_list.draw(screen)
            if len(game.positions[2].discs) == game.n_discs:
                if moves_counter == game.min_moves:
                    game_over_title = font.render(
                        "Congratulations! You just finished the game with the minimum movements! :)",
                        True,
                        color.BLACK,
                    )
                    screen.blit(game_over_title, [((SCREEN_WIDTH / 2) - (game_over_title.get_width() / 2)), SCREEN_HEIGHT / 2])
                else:
                    game_over_title = font.render(
                        "You just finished the game, now try again with the minimum movements! ;)",
                        True,
                        color.BLACK,
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
                            menu.sprites_list.remove([menu.label])
                    if turn_back:
                        game.discs[disc_index].rect.x = last_pos[0]
                        game.discs[disc_index].rect.y = last_pos[1]
                    move = False
        game.sprites_list.draw(screen)

    # Actualizar la pantalla
    pygame.display.flip()
    clock.tick(60)

pygame.quit()