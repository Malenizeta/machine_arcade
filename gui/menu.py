import pygame, sys, os
import textwrap


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

def wrap_text(text, font, max_width):
    lines = []
    for paragraph in text.split('\n'):
        words = paragraph.split(' ')
        line = ''
        for word in words:
            test_line = f"{line} {word}".strip()
            if font.size(test_line)[0] <= max_width:
                line = test_line
            else:
                lines.append(line)
                line = word
        lines.append(line)
    return lines

def abrir_chatbot(screen):
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from ia_client import consultar_chatbot

    font = pygame.font.Font(FONT_PATH, 18)

    # Cargar imagen de fondo desde assets
    background_image = pygame.image.load(os.path.join(os.path.dirname(__file__), "../assets/images/Chatbot.jpg"))
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # Definir zona blanca (ajústala según tu imagen)
    cuadro_x, cuadro_y = 130, 50
    cuadro_ancho, cuadro_alto = 460, 500

    input_box = pygame.Rect(cuadro_x + 180, cuadro_y + cuadro_alto - 40, 50, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    respuesta = ''
    clock = pygame.time.Clock()

    while True:
        screen.blit(background_image, (0, 0))

        # Mostrar respuesta dentro del recuadro blanco
        if respuesta:
            wrapped_lines = wrap_text(respuesta, font, cuadro_ancho - 20)
            for i, line in enumerate(wrapped_lines):
                if i * 24 < cuadro_alto - 200:  # evitar desbordar
                    rendered = font.render(line, True, BLACK)
                    screen.blit(rendered, (cuadro_x + 80, cuadro_y + 50 + i * 24))

        # Entrada de texto
        txt_surface = font.render(text, True, color)
        input_box.w = max(320, txt_surface.get_width() + 10)
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, color, input_box, 2)

        pygame.display.flip()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                active = input_box.collidepoint(event.pos)
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN and active:
                if event.key == pygame.K_RETURN:
                    respuesta = consultar_chatbot(text)
                    text = ''
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode

def draw_menu(screen):
   
    background_image = pygame.image.load(os.path.join(os.path.dirname(__file__), "../assets/images/menu.jpg"))
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    
    screen.blit(background_image, (0, 0))

  
    font = pygame.font.Font(FONT_PATH, 40)  

    
    button_torres = pygame.Rect(150, 310, 300, 50)  
    button_reinas = pygame.Rect(150, 380, 300, 50) 
    button_caballo = pygame.Rect(150, 450, 300, 50)
    button_chatbot = pygame.Rect(150, 520, 300, 50) 

    button_text_torres = font.render("Torres de Hanoi", True, WHITE)
    button_text_reinas = font.render("N-Reinas", True, WHITE)
    button_text_caballo = font.render("Caballo Tour", True, WHITE)
    button_text_chatbot = font.render("Chatbot IA", True, WHITE)


    screen.blit(button_text_torres, (button_torres.x + 10, button_torres.y + 10))
    screen.blit(button_text_reinas, (button_reinas.x + 10, button_reinas.y + 10))
    screen.blit(button_text_caballo, (button_caballo.x + 10, button_caballo.y + 10))
    screen.blit(button_text_chatbot, (button_chatbot.x + 10, button_chatbot.y + 10))
    

    pygame.display.flip()

    return button_torres, button_reinas, button_caballo, button_chatbot


def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Menú Principal")

    # Bucle del menú
    running = True
    while running:
        button_torres, button_reinas, button_caballo, button_chatbot = draw_menu(screen)

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
                elif button_chatbot.collidepoint(mouse_pos):
                    abrir_chatbot(screen)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()


