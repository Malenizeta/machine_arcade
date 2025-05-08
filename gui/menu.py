import pygame, sys, os


SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


FONT_PATH = os.path.join(os.path.dirname(__file__), "../assets/fonts/mario.ttf")

pygame.init()


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


def draw_menu(screen):
   
    background_image = pygame.image.load(os.path.join(os.path.dirname(__file__), "../assets/images/menu.jpg"))
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    
    screen.blit(background_image, (0, 0))

  
    font = pygame.font.Font(FONT_PATH, 40)  

    
    button_torres = pygame.Rect(150, 350, 300, 50)  
    button_reinas = pygame.Rect(150, 420, 300, 50) 
    button_caballo = pygame.Rect(150, 490, 300, 50)  

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
                    run_torres_hanoi() 
                elif button_reinas.collidepoint(mouse_pos):
                    run_n_reinas()  
                elif button_caballo.collidepoint(mouse_pos):
                    run_caballo_tour()  

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
