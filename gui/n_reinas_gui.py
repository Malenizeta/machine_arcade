import pygame, sys, random, os
import datetime
from pygame.locals import *
import math


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from client import enviar_resultado
from games import n_reinas


BASICFONTSIZE = 20

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

    while True:
        for row in range(n):
            c_indx = row % 2
            for col in range(n):
                the_square = (col * sq_sz, row * sq_sz, sq_sz, sq_sz)
                display_surface.fill(colors[c_indx], the_square)
                c_indx = (c_indx + 1) % 2

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONDOWN:
                mousex, mousey = event.pos
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
    width, height = 400, 200
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Tamaño del tablero")
    font = pygame.font.SysFont('arial', 36)
    input_text = ''
    input_active = True

    while True:
        screen.fill((200, 200, 200))
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
