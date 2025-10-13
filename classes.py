import pygame

class StartScreen:
    def __init__(self, screen):
        self.screen = screen

    def tick(self):
        assert isinstance(self.screen, pygame.Surface)

        color1 = pygame.Color(200, 200, 200)
        color2 = pygame.Color(100, 100, 100)
        center = pygame.Vector2(100, 100)
        radius = 50

        self.screen.fill(color1)
        pygame.draw.circle(self.screen, color2, center, radius)