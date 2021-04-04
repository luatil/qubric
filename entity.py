import pygame
import numpy as np
from board import Board, Slice, Move

class Mixer:
    def __init__(self):
        self.click_sound = pygame.mixer.Sound("./assets/sounds/click.wav")
        self.click_sound.set_volume(0.1)
        self.muted = False

    def click(self):
        self.click_sound.play(0)

    def play_music(self):
        pygame.mixer.music.load("./assets/sounds/music.wav")
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)

    def toggle_mute(self):
        if self.muted:
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.pause()
        self.muted = not self.muted

class Entity:
    def collidepoint(self, pos):
        return self.rect.collidepoint(pos)

    def set_position(self, pos, offset = 0):
        if offset == 0:
            self.rect.center = pos
        else:
            self.rect.topleft = pos - pygame.Vector2(offset)

    def create_surface(self, size):
        surface = pygame.Surface(size, pygame.SRCALPHA, 32)
        surface.convert_alpha()
        return surface

class Image(Entity):
    def __init__(self, img_name):
        self.image = pygame.image.load("./assets/images/" + img_name)
        self.rect = self.image.get_rect()

    def scale(self, factor):
        new_size = tuple(map(int, tuple(pygame.Vector2(self.rect.size) * factor)))
        self.image = pygame.transform.smoothscale(self.image, new_size)
        rect_center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = rect_center

    def blit_in(self, surface):
        surface.blit(self.image, self.rect)

class Text(Entity):
    def __init__(self, font_size, string, color = (0, 0, 0), pos = (0, 0)):
        self.font = pygame.font.Font('./assets/fonts/golden_age_shad.ttf', font_size)
        self.string = string
        self.render_color(color)
        self.rect = self.surface.get_rect()
        self.set_position(pos)

    def blit_in(self, surface):
        surface.blit(self.surface, self.rect)

    def render_color(self, color):
        self.surface = self.font.render(self.string, True, color)

class Selector(Entity):
    def __init__(self, font_size, strings, color = (0, 0, 0), selected_color = (0,0,0), selected = None, height = 300, pos = (0, 0)):
        self.texts = []
        self.selected = selected
        self.color = color
        self.selected_color = selected_color

        width = 0
        for i in range(len(strings)):
            self.texts.append(Text(font_size, strings[i], color))
            width = max(width, self.texts[i].rect.width)

        self.spacing = self.texts[0].font.get_height() * 1.6
        self.scroll_pos = 0
        self.max_scroll_pos = self.spacing * (len(self.texts) - 1)

        if selected != None:
            self.texts[selected].render_color(self.selected_color)

        self.rect = pygame.Rect((0, 0), (width, height))
        self.set_position(pos)
        self.update_positions()

    def update_positions(self):
        for i in range(len(self.texts)):
            offset = pygame.Vector2(self.texts[i].rect.width/2, 0)
            self.texts[i].set_position((self.rect.width/2, i * self.spacing - self.scroll_pos), offset)

    def scroll(self, direction):
        self.scroll_pos += direction * 20
        self.scroll_pos = min(max(0, self.scroll_pos), self.max_scroll_pos)
        self.update_positions()

    def select(self, mouse_pos):
        mouse_pos -= pygame.Vector2(self.rect.topleft)
        for i in range(len(self.texts)):
            if self.texts[i].collidepoint(mouse_pos):

                if self.selected != None:
                    self.texts[self.selected].render_color(self.color)

                self.selected = i
                self.texts[i].render_color(self.selected_color)

    def blit_in(self, surface):
        selector_surface = self.create_surface(self.rect.size)

        for text in self.texts:
            text.blit_in(selector_surface)

        surface.blit(selector_surface, self.rect)

class GUIBoard(Entity, Board):
    def __init__(self):
        Board.__init__(self)
        self.scale = 0.75
        self.update_slices_positions()
        self.rect = self.unscaled_rect.copy()
        self.rect.size = pygame.Vector2(self.rect.size) * self.scale

    def generate_board(self):
        self.board = [GUISlice(self.size, self.playerX_id, self.playerO_id) for i in range(self.size)]

    def update_slices_positions(self):
        for i in range(self.size):
            pos = (0, self.board[i].rect.height * i)
            self.board[i].set_position(pos, (0, 0))
        self.unscaled_rect = self.board[0].rect.unionall(list(map(lambda x: x.rect, self.board[1:])))

    def rotate(self, side):
        for slc in self.board:
            slc.rotate(side)
        self.update_slices_positions()

    def select_move(self, mouse_pos):
        mouse_pos = pygame.Vector2(mouse_pos)
        mouse_pos -= self.rect.topleft
        mouse_pos *= 1/self.scale
        for index, slc in enumerate(self.board):
            if slc.collidepoint(mouse_pos):
                selected_move = slc.select_move(mouse_pos)
                if selected_move != None:
                    selected_move.z = index
                    return selected_move

    def blit_in(self, surface):
        board_surface = self.create_surface(self.unscaled_rect.size)

        for slc in self.board:
            slc.blit_in(board_surface)

        surface.blit(pygame.transform.smoothscale(board_surface, self.rect.size), self.rect)

class GUISlice(Entity, Slice):
    def __init__(self, size, playerX_id, playerO_id):
        Slice.__init__(self, size, playerX_id, playerO_id)
        self.rotation = 0
        self.update_sprites()

        self.horizontal_offset = 178
        self.horizontal_spacing = 152

        self.vertical_offset = 76
        self.vertical_spacing = 65

        self.generate_bounds()
        self.linear_transform = np.matmul(np.array([[107, -107], [46, 46]]), np.array([[1/self.horizontal_spacing, 0], [0, 1/self.vertical_spacing]]))

    def update_sprites(self):
        angle = self.rotation % 2 * 45
        self.sprite = Image("board" + str(angle) + ".png")
        self.rect = self.sprite.rect
        self.Xsprite = Image("X" + str(angle) + ".png")
        self.Osprite = Image("O" + str(angle) + ".png")

    def get_symbol_sprite(self, symbol):
        if symbol == self.playerX_id:
            return self.Xsprite
        if symbol == self.playerO_id:
            return self.Osprite
        return None

    def generate_bounds(self):
        first_bound = self.horizontal_offset - self.horizontal_spacing/2
        self.horizontal_bounds = [i * self.horizontal_spacing + first_bound for i in range(self.size + 1)]

        first_bound = self.vertical_offset - self.vertical_spacing/2
        self.vertical_bounds   = [i * self.vertical_spacing + first_bound for i in range(self.size + 1)]

    def rotate(self, side):
        self.rotation += side
        self.rotation %= 8
        self.update_sprites()

    def rotate_move(self, x, y):
        for i in range(4 + int(self.rotation/2) % 4):
            x, y = y, 3 - x

        return x, y

    def set_rotated_move_symbol(self, x, y, content):
        x, y = self.rotate_move(x, y)
        return self.set_symbol(x, y, content)

    def get_rotated_move_symbol(self, x, y):
        x, y = self.rotate_move(x, y)
        return self.get_symbol(x, y)

    def is_slanted(self):
        return self.rotation % 2

    def vector_to_matrix(self, vector):
        return np.transpose(np.array([tuple(vector)]))

    def matrix_to_vector(self, matrix):
        return pygame.Vector2(tuple(np.transpose(matrix)[0]))

    def ortogonal_to_slanted(self, v):
        v -= pygame.Vector2(self.horizontal_offset, self.vertical_offset)
        v = self.vector_to_matrix(v)
        v = np.matmul(self.linear_transform, v)
        return self.matrix_to_vector(v) + (self.rect.width/2, self.Xsprite.rect.height/2)

    def slanted_to_ortogonal(self, v):
        v -= (self.rect.width/2, self.Xsprite.rect.height/2)
        v = self.vector_to_matrix(v)
        v = np.matmul(np.linalg.inv(self.linear_transform), v)
        return self.matrix_to_vector(v) + pygame.Vector2(self.horizontal_offset, self.vertical_offset)

    def select_move(self, mouse_pos):
        mouse_pos -= self.rect.topleft

        if self.is_slanted():
            mouse_pos = self.slanted_to_ortogonal(mouse_pos)

        x = y = -1

        for i in range(self.size + 1):
            if mouse_pos.x > self.horizontal_bounds[i]:
                x = i

            if mouse_pos.y > self.vertical_bounds[i]:
                y = i

        if 0 <= x < self.size and 0 <= y < self.size:
            x, y = self.rotate_move(x, y)
            return Move('', x, y, 0)

        return None

    def blit_in(self, surface):
        slice_surface = self.create_surface(self.rect.size)

        self.sprite.blit_in(surface)

        for i in range(self.size):
            for j in range(self.size):
                symbol = self.get_rotated_move_symbol(i, j)
                symbol_sprite = self.get_symbol_sprite(symbol)
                if symbol_sprite != None:

                    symbol_center = (self.horizontal_offset + self.horizontal_spacing * i, self.vertical_offset + self.vertical_spacing * j)
                    if self.rotation % 2 == 1:
                        symbol_center = self.ortogonal_to_slanted(symbol_center)

                    symbol_sprite.set_position(symbol_center)
                    symbol_sprite.blit_in(slice_surface)

        surface.blit(slice_surface, self.rect)
