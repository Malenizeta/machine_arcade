import pygame, sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from games import caballo_tour as ct

def manual_knights_tour(n):
    pygame.init()
    cell_size = 60
    yoshi_image = pygame.image.load(os.path.join(os.path.dirname(__file__), "../assets/images/yoshi.png"))
    yoshi_image = pygame.transform.scale(yoshi_image, (cell_size, cell_size)) 
    huevo_image = pygame.image.load(os.path.join(os.path.dirname(__file__), "../assets/images/huevo.png"))
    huevo_image = pygame.transform.scale(huevo_image, (50, 60))
    screen = pygame.display.set_mode((n * cell_size, n * cell_size))
    pygame.display.set_caption("Recorrido del Caballo")
    font = pygame.font.SysFont(None, 24)

    board = ct.create_board(n)
    move_num = 0
    current_pos = None

    def draw_board():
        for row in range(n):
            for col in range(n):
                rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                color = (255, 255, 255) if (row + col) % 2 == 0 else (104, 224, 84)
                pygame.draw.rect(screen, color, rect)
                #pygame.draw.rect(screen, (100, 100, 100), rect, 1)
                if board[row][col] != -1:
                    screen.blit(huevo_image, (col * cell_size, row * cell_size))
                    move_text = font.render(str(board[row][col]), True, (0, 100, 0))  
                    text_rect = move_text.get_rect(center=(col * cell_size + cell_size // 2, row * cell_size + cell_size // 2))
                    screen.blit(move_text, text_rect)
        if current_pos:
            screen.blit(yoshi_image, (current_pos[1] * cell_size, current_pos[0] * cell_size))
        pygame.display.flip()

    running = True
    while running:
        draw_board()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                col = mx // cell_size
                row = my // cell_size
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
                    else:
                        print("Movimiento inválido")

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    manual_knights_tour(8)