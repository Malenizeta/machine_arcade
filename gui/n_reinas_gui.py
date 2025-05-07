import pygame, sys, random, os
from pygame.locals import *
import math


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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
    colors = [(255, 255, 255), (0, 0, 0)]

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

        for sprite in all_sprites:
            if sprite.dragging:
                sprite.posn = (mousex - peach_image.get_width() // 2,
                       mousey - peach_image.get_height() // 2)
            else:
                sprite.update()
            sprite.draw(display_surface)

        if is_win:
            display_surface.blit(pygame.image.load(os.path.dirname(__file__), "../assets/images/Fin.jpg"), (0, 0))

        pygame.display.update()
        fpsClock.tick(FPS)

if __name__ == '__main__':
    draw_board(8)
