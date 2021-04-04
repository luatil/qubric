import pygame
from screen import Menu
from entity import Mixer

class Game:
    def __init__(self):
        self.running = False
        self.display_surface = None
        self.display_flags =  pygame.HWSURFACE
        self.set_size((1920, 1080))
        self.screen = None

    def set_size(self, size):
        self.size = self.width, self.height = size

    def on_init(self):
        pygame.init()
        pygame.display.set_caption('Qubric')
        self.display_surface = pygame.display.set_mode(self.size, self.display_flags)
        self.set_size(pygame.display.get_surface().get_size())
        self.running = True
        self.screen = Menu(self)
        self.sound = Mixer()
        self.sound.play_music()

    def stop(self):
        self.running = False

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self.stop()
        else:
            self.screen = self.screen.on_event(event)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.sound.click()

    def on_loop(self):
        self.screen = self.screen.on_loop()

    def on_render(self):
        self.screen.on_render()
        pygame.display.update()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        self.on_init()

        while self.running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()
