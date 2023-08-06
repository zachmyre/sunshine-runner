import pygame

class Game:
    def __init__(self, width, height) -> None:
        # pygame setup
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0
        return
