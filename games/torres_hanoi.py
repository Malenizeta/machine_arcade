import pygame
import os

# Color Constants class
class ColorConstants():
    RED = (255, 0, 0)
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    WHITE = (255, 255, 255)
    BACKGROUND = (240, 248, 255)
    BOARD_COLOR = (153, 76, 0)

# Generic Block class
class Block(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.width = width
        self.height = height
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()

    def is_clicked(self):
        return pygame.mouse.get_pressed()[0] and self.rect.collidepoint(pygame.mouse.get_pos())

# Game positions class
class Position(Block):
    def __init__(self, pos_index, color, width, height):
        super().__init__(color, width, height)
        self.pos_index = pos_index
        self.discs = []

# Game discs class
class Disc(Block):
    image_path = os.path.join(os.path.dirname(__file__), "../assets/images/Ladrillo.png")
    
    def __init__(self, current_pos, id, color, width, height):
        super().__init__(color, width, height)
        self.current_pos = current_pos
        self.id = id
        self.original_image = pygame.image.load(self.image_path).convert_alpha()
        self.image = pygame.transform.scale(self.original_image, (int(width), int(height)))
        self.rect = self.image.get_rect()
        self.width = width
        self.height = height

    def is_clicked(self):
        return pygame.mouse.get_pressed()[0] and self.rect.collidepoint(pygame.mouse.get_pos())

# Buttons class
class Button(Block):
    def __init__(self, text, text_color, text_size, text_font, color, width, height):
        super().__init__(color, width, height)
        self.text = text
        self.text_color = text_color
        self.font = pygame.font.SysFont(text_font, text_size, False, False)
        self.text_render = self.font.render(text, 1, text_color)
        self.value = None

    def set_value(self, value):
        self.value = value

    def render_text(self):
        w = (self.width / 2 - self.text_render.get_width() / 2)
        h = (self.height / 2 - self.text_render.get_height() / 2)
        self.image.blit(self.text_render, [w, h])

# Main Menu
class MainMenu(ColorConstants):
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.sprites_list = pygame.sprite.Group()

        # Etiqueta para el cuadro de texto
        self.label = Button("Enter the number of discs:", self.BLACK, 30, 'Calibri', self.WHITE, 500, 30)
        self.label.rect.x = self.SCREEN_WIDTH / 4
        self.label.rect.y = self.SCREEN_HEIGHT / 2 - 80
        self.label.render_text()
        self.sprites_list.add(self.label)

        # Cuadro de texto para ingresar el número de discos
        self.input_box = pygame.Rect(self.SCREEN_WIDTH / 3, self.SCREEN_HEIGHT / 2 - 40, 140, 32)
        self.input_text = ""
        self.input_active = False

        # Botón para iniciar el juego
        self.btn_start = Button("Start Game", self.BLACK, 30, 'Calibri', self.GREEN, 150, 30)
        self.btn_start.rect.x = self.SCREEN_WIDTH / 2 - self.btn_start.image.get_width() / 2
        self.btn_start.rect.y = self.SCREEN_HEIGHT / 2 + 20
        self.btn_start.render_text()
        self.sprites_list.add(self.btn_start)

        # Game over buttons
        self.btn_play_again = Button("Play again", self.BLACK, 30, 'Calibri', self.GREEN, 130, 30)
        self.btn_return = Button("Return to menu", self.BLACK, 30, 'Calibri', self.BACKGROUND, 150, 30)
        self.btn_quit = Button("Quit", self.BLACK, 30, 'Calibri', self.RED, 70, 30)
        self.btn_play_again.rect.x = self.SCREEN_WIDTH / 2 - (self.btn_return.image.get_width() * 2)
        self.btn_play_again.rect.y = self.SCREEN_HEIGHT / 2 - 40
        self.btn_play_again.render_text()
        self.btn_return.rect.x = self.SCREEN_WIDTH / 2 - self.btn_return.image.get_width() / 2
        self.btn_return.rect.y = self.SCREEN_HEIGHT / 2 - 40
        self.btn_return.render_text()
        self.btn_quit.rect.x = self.SCREEN_WIDTH / 2 + (self.btn_return.image.get_width())
        self.btn_quit.rect.y = self.SCREEN_HEIGHT / 2 - 40
        self.btn_quit.render_text()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Activar el cuadro de texto si se hace clic en él
            if self.input_box.collidepoint(event.pos):
                self.input_active = True
            else:
                self.input_active = False

        elif event.type == pygame.KEYDOWN and self.input_active:
            if event.key == pygame.K_RETURN:
                # Retornar el texto ingresado cuando se presiona Enter
                return self.input_text
            elif event.key == pygame.K_BACKSPACE:
                # Eliminar el último carácter
                self.input_text = self.input_text[:-1]
            else:
                # Agregar el carácter ingresado
                self.input_text += event.unicode

        return None

    def draw(self, screen):
        # Dibujar el cuadro de texto
        pygame.draw.rect(screen, self.WHITE, self.input_box, 2 if self.input_active else 1)
        font = pygame.font.Font(None, 30)
        text_surface = font.render(self.input_text, True, self.BLACK)
        screen.blit(text_surface, (self.input_box.x + 5, self.input_box.y + 5))
        self.sprites_list.draw(screen)
        

# Game main class
class Game(ColorConstants):
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        self.sprites_list = pygame.sprite.Group()
        self.pos_sprites_list = pygame.sprite.Group()
        self.BOARD_WIDTH = SCREEN_WIDTH / 2
        self.BOARD_HEIGHT = 50
        self.BOARD_X = SCREEN_WIDTH * 0.25
        self.BOARD_Y = SCREEN_HEIGHT - 55
        self.POS_WIDTH = 20
        self.POS_HEIGHT = 200
        self.DISC_WIDTH = 200
        self.DISC_HEIGHT = self.POS_WIDTH
        self.positions = []
        self.discs = []
        self.game_board = Block(self.BOARD_COLOR, self.BOARD_WIDTH, self.BOARD_HEIGHT)
        self.game_board.rect.x = self.BOARD_X
        self.game_board.rect.y = self.BOARD_Y
        first_pos = Position(0, self.BOARD_COLOR, self.POS_WIDTH, self.POS_HEIGHT)
        first_pos.rect.x = self.BOARD_X
        first_pos.rect.y = self.BOARD_Y - self.POS_HEIGHT
        second_pos = Position(1, self.BOARD_COLOR, self.POS_WIDTH, self.POS_HEIGHT)
        second_pos.rect.x = (self.BOARD_X + (self.BOARD_WIDTH / 2)) - (self.POS_WIDTH / 2)
        second_pos.rect.y = self.BOARD_Y - self.POS_HEIGHT
        third_pos = Position(2, self.BOARD_COLOR, self.POS_WIDTH, self.POS_HEIGHT)
        third_pos.rect.x = (self.BOARD_X + self.BOARD_WIDTH) - self.POS_WIDTH
        third_pos.rect.y = self.BOARD_Y - self.POS_HEIGHT
        self.positions = [first_pos, second_pos, third_pos]
        self.sprites_list.add([self.game_board, self.positions])
        self.pos_sprites_list.add(self.positions)

    def set_n_discs(self, n_discs):
        self.n_discs = n_discs
        self.min_moves = ((2 ** self.n_discs) - 1)

    def draw_discs(self):
        self.discs.clear()
        self.positions[0].discs.clear()

        base_image = pygame.image.load(Disc.image_path).convert_alpha()
        img_width, img_height = base_image.get_size()

        for i in range(self.n_discs):
            width = self.DISC_WIDTH / (i + 1)
            height = self.DISC_HEIGHT  # altura fija

            # Escalado proporcional a la altura
            scale_factor = height / img_height
            tile_width = int(img_width * scale_factor)
            tile_height = int(height)

            scaled_tile = pygame.transform.smoothscale(base_image, (tile_width, tile_height))

            # Calcular cuántas veces cabe en el ancho del disco
            tiles_needed = int(width // tile_width) + 1

            # Crear superficie para el disco
            disc_image = pygame.Surface((int(width), tile_height), pygame.SRCALPHA)
            for j in range(tiles_needed):
                disc_image.blit(scaled_tile, (j * tile_width, 0))

            # Crear el objeto Disc y asignar la imagen
            disc = Disc(0, i, self.BOARD_COLOR, width, height)
            disc.image = disc_image
            disc.rect = disc_image.get_rect()
            disc.rect.x = self.BOARD_X - (width / 2) + (self.POS_WIDTH / 2)
            disc.rect.y = self.BOARD_Y - height - (height * i)

            self.discs.append(disc)
            self.positions[0].discs.append(disc)

        self.sprites_list.add(self.discs)
