import pygame
from entity import Text, Selector, GUIBoard, Image
from players import Human, SequentialBot, StallerBot, RandomBot

class Screen:
    def on_render(self):
        pass

    def on_event(self, event):
        return self

    def on_loop(self):
        return self

class Help(Screen):
    def __init__(self, game):
        self.game = game
        self.title = Text(160, 'COMO JOGAR?')
        self.back = Text(80, 'VOLTAR')
        with open("assets/help_screen.txt", "r") as help_text:
            text = help_text.read()
        self.text = Selector(65, text.split('\n'), height=game.height * 0.6)
        self.update_positions()

    def update_positions(self):
        height = self.game.height
        middle = self.game.width * 0.5
        self.title.set_position((middle, height * 0.125))
        self.text.set_position((middle, height * 0.5))
        self.back.set_position((middle, height * 0.9))

    def on_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            if event.button == 1:
                if self.back.collidepoint(mouse_pos):
                    return Menu(self.game)
            if self.text.collidepoint(mouse_pos):
                if event.button == 4:
                    self.text.scroll(-1)
                if event.button == 5:
                    self.text.scroll(1)
        return self

    def on_render(self):
        display_surface = self.game.display_surface
        display_surface.fill((255,255,255))

        self.title.blit_in(display_surface)
        self.back.blit_in(display_surface)
        self.text.blit_in(display_surface)

class Menu(Screen):
    def __init__(self, game):
        self.game = game

        self.title = Text(160, 'QUBRIC')

        self.toggle_mute = [Image("un" * i + "mute.png") for i in range(2)]
        for img in self.toggle_mute:
            img.scale(0.3)

        self.set_options()
        self.update_positions()

    def set_options(self):
        options = ['JOGAR', 'COMO JOGAR','SAIR']
        self.selector = Selector(80, options)

    def update_positions(self):
        width = self.game.width
        middle = width/2
        height = self.game.height
        self.title.set_position((middle, height * 0.25))
        self.selector.set_position((middle, height * 0.6))

        for i in range(len(self.toggle_mute)):
            self.toggle_mute[i].set_position(pygame.Vector2(width, height) * 0.9)

    def on_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()

                if self.selector.collidepoint(mouse_pos):
                    self.selector.select(mouse_pos)

                    if self.selector.selected == 0:
                        return PlayerSelection(self.game)
                    elif self.selector.selected == 1:
                        return Help(self.game)
                    elif self.selector.selected == 2:
                        self.game.stop()

                if self.toggle_mute[0].collidepoint(mouse_pos):
                    self.game.sound.toggle_mute()

        return self

    def on_render(self):
        display_surface = self.game.display_surface

        display_surface.fill((255,255,255))

        self.title.blit_in(display_surface)
        self.selector.blit_in(display_surface)

        if self.game.sound.muted:
            self.toggle_mute[0].blit_in(display_surface)
        else:
            self.toggle_mute[1].blit_in(display_surface)

class PlayerSelection(Screen):
    def __init__(self, game):
        self.game = game
        big_font_size = 120
        small_font_size = 75

        self.title = Text(big_font_size, 'SELECAO DE JOGADORES')
        self.player1 = Text(small_font_size, 'JOGADOR X')
        self.player2 = Text(small_font_size, 'JOGADOR O')
        self.start = Text(small_font_size, "JOGAR")
        self.back = Text(small_font_size, 'VOLTAR')
        self.set_options()
        self.update_positions()

    def set_options(self):
        self.players = ["HUMANO", "ESTABANADO", "COME-CRU", "FANFARRAO"]
        self.playersCreated = [Human, RandomBot, SequentialBot, StallerBot]
        self.selectors = [Selector(70, self.players, (0, 0, 0), (255, 0, 0), 0) for i in range(2)]

    def update_positions(self):
        width, height = self.game.size

        self.title.set_position((width * 0.5, height * 0.2))
        self.player1.set_position((width * 0.25, height * 0.4))
        self.player2.set_position((width * 0.75, height * 0.4))
        self.start.set_position((width * 0.5, height * 0.825))
        self.back.set_position((width * 0.5, height * 0.9))

        for i in range(len(self.selectors)):
            self.selectors[i].set_position((width * (0.25 + 0.5 * i), height * 0.6))

    def on_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()

            if self.back.collidepoint(mouse_pos):
                return Menu(self.game)

            if self.start.collidepoint(mouse_pos):
                players = [self.playersCreated[self.selectors[0].selected]("X"),
                           self.playersCreated[self.selectors[1].selected]("O") ]
                return GameScreen(self.game, players)

            for sel in self.selectors:
                if sel.collidepoint(mouse_pos):
                    sel.select(mouse_pos)

        return self

    def on_render(self):
        display_surface = self.game.display_surface
        display_surface.fill((255, 255, 255))
        self.title.blit_in(display_surface)
        self.player1.blit_in(display_surface)
        self.player2.blit_in(display_surface)
        self.back.blit_in(display_surface)
        self.start.blit_in(display_surface)

        for sel in self.selectors:
            sel.blit_in(display_surface)

class GameScreen(Screen):
    def __init__(self, game, players):
        self.game = game
        self.board = GUIBoard()
        self.players = players

        self.rotation_buttons = [Image(i * "counter" + "ClockArrow.png") for i in range(2)]

        self.turn_indicator = [Image("X.png"), Image("O.png")]
        for ind in self.turn_indicator:
            ind.scale(0.35)

        self.round_counter = 0
        self.move_timer = None
        self.bot_delay = 750
        self.last_selected_move = None
        self.update_positions()

    def update_positions(self):
        width, height = size = self.game.size
        self.board.set_position(pygame.Vector2(size) / 2)

        for i in range(len(self.rotation_buttons)):
            self.rotation_buttons[i].set_position(( width * (2 - i)/3, height/2))

        for i in range(len(self.turn_indicator)):
            self.turn_indicator[i].set_position((width  * (4 * i + 1)/6, height/2))

    def on_event(self, event):
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                return PauseMenu(self.game, self)

            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                self.board.rotate(-1)

            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                self.board.rotate(1)

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos(event)

            if self.board.collidepoint(mouse_pos):
                self.last_selected_move = self.board.select_move(mouse_pos)

            for i in range(len(self.rotation_buttons)):
                if self.rotation_buttons[i].collidepoint(mouse_pos):
                    self.board.rotate(1 - 2 * i)

        return self

    def is_turn_finished(self):
        now = pygame.time.get_ticks()
        return self.move_timer == None or now - self.move_timer >= self.bot_delay

    def on_loop(self):
        self.current_player =  [None, 0, None, 1][self.round_counter % 4]
        current_player = self.current_player
        if current_player == None:
            if self.board.is_finished():
                return EndScreen(self.game, self.board)

            self.last_selected_move = None
            self.move_timer = None
            self.round_counter += 1

        else:
            if self.players[current_player].automatic == True:
                if self.move_timer == None:
                    self.move_timer = pygame.time.get_ticks()
                    self.players_move = self.players[current_player].get_move(self.board)

            else:
                self.players_move = self.players[current_player].get_move(self.board, self.last_selected_move)

            if self.is_turn_finished() and self.board.play_move(self.players_move):
                self.round_counter += 1

        return self

    def on_render(self):
        display_surface = self.game.display_surface
        display_surface.fill((255,255,255))
        self.board.blit_in(display_surface)

        for rotation_button in self.rotation_buttons:
            rotation_button.blit_in(display_surface)

        if self.current_player != None:
            self.turn_indicator[self.current_player].blit_in(display_surface)


class PauseMenu(Screen):
    def __init__(self, game, game_screen):
        self.game = game
        self.game_screen = game_screen
        self.selector = Selector(70, ["CONTINUAR", "MENU", "SAIR"], height=200)
        self.selector.set_position(pygame.Vector2(game.size) / 2)

    def on_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return self.game_screen

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos(event)

            if self.selector.collidepoint(mouse_pos):
                self.selector.select(mouse_pos)

                sel = self.selector.selected
                if sel == 0:
                    return self.game_screen
                if sel == 1:
                    return Menu(self.game)
                if sel == 2:
                    self.game.stop()

        return self

    def on_render(self):
        display_surface = self.game.display_surface
        display_surface.fill((255,255,255))

        self.selector.blit_in(display_surface)

class EndScreen(Screen):
    def __init__(self, game, board):
        self.board = board
        self.game = game

        self.set_result_entities()

        options = ["JOGAR NOVAMENTE", "MENU", "SAIR"]
        self.selector = Selector(70, options)
        self.update_positions()

    def set_result_entities(self):

        if self.board.is_drawn():
            self.result_text = Text(100, "VELHA??")
            self.result_image = Image("draw.jpg")
            self.result_image.scale(0.70)
        else:
            player_id = self.board.get_winning_player_id()
            if player_id == self.board.playerX_id:
                self.result_image = Image("X.png")
            else:
                self.result_image = Image("O.png")
            self.result_image.scale(0.45)
            self.result_text = Text(100, "GANHOU!!!")

    def update_positions(self):
        width, height = self.game.size

        self.board.set_position((width/4, height/2))
        self.selector.set_position((width * 3/4, height * 3/4))
        self.result_image.set_position((width * 3/4, height/4))
        self.result_text.set_position((width * 3/4, height/4))
        self.result_text.rect.top += self.result_image.rect.height/2 + self.result_text.rect.height * 0.7

    def on_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self.board.rotate(1)
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                self.board.rotate(-1)

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos(event)

            if self.selector.collidepoint(mouse_pos):
                self.selector.select(mouse_pos)

                sel = self.selector.selected
                if sel == 0:
                    return PlayerSelection(self.game)
                if sel == 1:
                    return Menu(self.game)
                if sel == 2:
                    self.game.stop()

        return self

    def on_render(self):
        display_surface = self.game.display_surface
        display_surface.fill((255,255,255))

        self.selector.blit_in(display_surface)
        self.result_text.blit_in(display_surface)
        self.result_image.blit_in(display_surface)
        self.board.blit_in(display_surface)

