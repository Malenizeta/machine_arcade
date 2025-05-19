import pygame, sys, random, os
import datetime
from pygame.locals import *
import math
import threading
import customtkinter as ctk
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ia_client import IAHelperThread

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from client import enviar_resultado
from games import n_reinas
FONT_PATH = os.path.join(os.path.dirname(__file__), "../assets/fonts/mario.ttf")
BACKGROUND_IMAGE_PATH = os.path.join(os.path.dirname(__file__), "../assets/images/Fondo.jpg")  # Cambia esta ruta según tu estructura
background_image = pygame.image.load(BACKGROUND_IMAGE_PATH)
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

BASICFONTSIZE = 20

def ventana_ayuda_ia(sugerencia: str):
    ctk.set_appearance_mode("light")  
    ctk.set_default_color_theme("green")  

    root = ctk.CTk()
    ruta_icono = os.path.join(os.path.dirname(__file__), "../assets/images/Icono.ico")
    root.iconbitmap(ruta_icono)
    root.title("Ayuda IA - N-Reinas")
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
        fg_color="#F499BD",
        hover_color="#CF82A1",
        text_color="white",
        font=("Segoe UI", 11, "bold"),
        corner_radius=8,
        command=root.destroy
    )
    btn_cerrar.pack(side="left", padx=10)

    root.mainloop()

class PeachSprite:

    def __init__(self, img, target_posn):
        self.image = img
        self.target_posn = target_posn
        self.posn = self.target_posn
        self.y_velocity = 0
        self.dragging = False

    def update(self):
        return

    def drag_with_mouse(self, mousex, mousey):
        sprite_rect = self.image.get_rect(topleft=self.posn)
        return sprite_rect.collidepoint(mousex, mousey)

    def mouse_touch_sprite(self, mousex, mousey):
        return self.drag_with_mouse(mousex, mousey)

    def draw(self, surface):
        surface.blit(self.image, self.posn)

def draw_board(n):
    pygame.init()
    colors = [(244, 153, 189), (255, 252, 201)]
    

    surface_sz = 480
    sq_sz = surface_sz // n
    surface_sz = n * sq_sz

    display_surface = pygame.display.set_mode((surface_sz, surface_sz))
    pygame.display.set_caption('N-Reinas')
    BASICFONT = pygame.font.SysFont('arial', BASICFONTSIZE)

    peach_image = pygame.image.load(os.path.join(os.path.dirname(__file__), "../assets/images/Peach.png"))
    peach_image.convert()
    peach_image = pygame.transform.rotozoom(peach_image, 0, 0.15)
    peach_offset = (sq_sz - peach_image.get_width()) // 2

    all_sprites = []
    chess_board = [-1] * n
    FPS = 30
    fpsClock = pygame.time.Clock()
    is_win = False
    mousex, mousey = 0, 0
    movimientos = 0

    ia_button_rect = pygame.Rect(10, surface_sz + 10, 120, 30)
    display_surface = pygame.display.set_mode((surface_sz, surface_sz + 50))

    while True:
        display_surface.fill((207, 130, 161))
        for row in range(n):
            c_indx = row % 2
            for col in range(n):
                the_square = (col * sq_sz, row * sq_sz, sq_sz, sq_sz)
                display_surface.fill(colors[c_indx], the_square)
                c_indx = (c_indx + 1) % 2
                
        # Botón de Ayuda IA
        pygame.draw.rect(display_surface, (244, 153, 189), ia_button_rect)
        ia_text = BASICFONT.render("Ayuda IA", True, (255, 255, 255))
        display_surface.blit(ia_text, (ia_button_rect.x + 10, ia_button_rect.y + 5))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONDOWN:
                mousex, mousey = event.pos

                # Si clic en botón IA
                if ia_button_rect.collidepoint(mousex, mousey):
                    estado_texto = f"Estado actual del tablero ({n}x{n}):\n"
                    for i, col in enumerate(chess_board):
                        fila = ["."] * n
                        if col != -1:
                            fila[col] = "Q"
                        estado_texto += " ".join(fila) + "\n"

                    def mostrar_sugerencia(resultado):
                        threading.Thread(target=ventana_ayuda_ia, args=(resultado,), daemon=True).start()

                    hilo = IAHelperThread(
                        "NReinas",
                        estado_texto,
                        mostrar_sugerencia
                    )
                    hilo.start()
                    continue

                # Clic fuera del tablero
                if mousey >= surface_sz:
                    continue  # ignorar clic fuera del área de tablero

                col_index = mousex // sq_sz
                row_index = mousey // sq_sz
                for item in all_sprites:
                    if item.mouse_touch_sprite(mousex, mousey):
                        item.dragging = True
                        chess_board[row_index] = -1
                        break
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                col_index = mousex // sq_sz
                row_index = mousey // sq_sz

                # Verificar que estamos dentro del tablero
                if row_index >= n or col_index >= n:
                    continue  # Ignorar clic fuera del área válida

                if chess_board[row_index] != -1 or (col_index in chess_board):
                    print("conflict horizontal or vertical")
                    print(chess_board)
                else:
                    chess_board[row_index] = col_index
                    print(chess_board)
                    if n_reinas.has_clashes_2(chess_board):
                        print("conflict diagonal")
                        chess_board[row_index] = -1
                        print(chess_board)
                    else:
                        movimientos += 1
                        drag_existing = False
                        for item in all_sprites:
                            if item.dragging:
                                drag_existing = True
                                item.dragging = False
                                item.posn = (col_index * sq_sz + peach_offset,
                                             row_index * sq_sz + peach_offset)
                                break
                        if not drag_existing:
                            new_queen = PeachSprite(peach_image,
                                                    (col_index * sq_sz + peach_offset,
                                                     row_index * sq_sz + peach_offset))
                            all_sprites.append(new_queen)
                        if -1 not in chess_board:
                            is_win = True
                            print("Has ganado!")
                            resultado = {
                                "board_size": n,
                                "result": "won",
                                "moves": movimientos,
                                #"timestamp": datetime.datetime.now().isoformat()
                            }
                            enviar_resultado("N Reinas", resultado)

        for sprite in all_sprites:
            if sprite.dragging:
                sprite.posn = (mousex - peach_image.get_width() // 2,
                       mousey - peach_image.get_height() // 2)
            else:
                sprite.update()
            sprite.draw(display_surface)

        # if is_win:
        #     display_surface.blit(pygame.image.load(os.path.dirname(__file__), "../assets/images/Fin.jpg"), (0, 0))

        pygame.display.update()
        fpsClock.tick(FPS)

def menu_inicio():
    pygame.init()
    width, height = 450, 350
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Tamaño del tablero")
    font = pygame.font.Font(FONT_PATH, 36)
    input_text = ''
    input_active = True

    while True:
        screen.blit(background_image, (0, 0))
        label = font.render("Introduce N (4 a 16):", True, (0, 0, 0))
        screen.blit(label, (50, 30))

        input_box = pygame.Rect(50, 80, 300, 50)
        pygame.draw.rect(screen, (255, 255, 255), input_box)
        pygame.draw.rect(screen, (0, 0, 0), input_box, 2)

        text_surface = font.render(input_text, True, (0, 0, 0))
        screen.blit(text_surface, (input_box.x + 10, input_box.y + 5))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and input_active:
                if event.key == K_RETURN:
                    if input_text.isdigit():
                        n = int(input_text)
                        if 4 <= n <= 16:
                            return n 
                elif event.key == K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.unicode.isdigit() and len(input_text) < 2:
                    input_text += event.unicode

        pygame.display.flip()
        
if __name__ == '__main__':
    n = menu_inicio()
    draw_board(n)
