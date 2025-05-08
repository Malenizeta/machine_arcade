import pygame, sys, os

# Definir constantes para colores y tamaños de pantalla
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 300
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

pygame.init()

# Funciones que inician los juegos
def run_torres_hanoi():
    print("Iniciando Torres de Hanoi...")
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from gui import torres_hanoi_gui
    torres_hanoi_gui.main()

def run_n_reinas():
    print("Iniciando N-Reinas...")
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from gui import n_reinas_gui
    n = n_reinas_gui.menu_inicio()
    n_reinas_gui.draw_board(n)

def run_caballo_tour():
    print("Iniciando Caballo Tour...")
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from gui import caballo_gui
    caballo_gui.caballo_tour(8)

# Función que dibuja el menú con los botones
def draw_menu(screen):
    font = pygame.font.SysFont(None, 40)
    title = font.render("Menú de Juegos", True, BLACK)
    screen.fill(WHITE)
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 20))

    # Botones para los juegos
    button_torres = pygame.Rect(100, 100, 200, 50)
    button_reinas = pygame.Rect(100, 160, 200, 50)
    button_caballo = pygame.Rect(100, 220, 200, 50)

    pygame.draw.rect(screen, BLACK, button_torres)
    pygame.draw.rect(screen, BLACK, button_reinas)
    pygame.draw.rect(screen, BLACK, button_caballo)

    button_text_torres = font.render("Torres de Hanoi", True, WHITE)
    button_text_reinas = font.render("N-Reinas", True, WHITE)
    button_text_caballo = font.render("Caballo Tour", True, WHITE)

    screen.blit(button_text_torres, (button_torres.x + 10, button_torres.y + 10))
    screen.blit(button_text_reinas, (button_reinas.x + 10, button_reinas.y + 10))
    screen.blit(button_text_caballo, (button_caballo.x + 10, button_caballo.y + 10))

    pygame.display.flip()

    return button_torres, button_reinas, button_caballo

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Menú Principal")

    # Bucle del menú
    running = True
    while running:
        button_torres, button_reinas, button_caballo = draw_menu(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if button_torres.collidepoint(mouse_pos):
                    run_torres_hanoi()  # Llamada a la función de Torres de Hanoi
                elif button_reinas.collidepoint(mouse_pos):
                    run_n_reinas()  # Llamada a la función de N-Reinas
                elif button_caballo.collidepoint(mouse_pos):
                    run_caballo_tour()  # Llamada a la función de Caballo Tour

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
