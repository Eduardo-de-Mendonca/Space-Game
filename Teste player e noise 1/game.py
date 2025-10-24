import pygame
from settings import *
from level import Level

class Game:
    def __init__(self):

        pygame.init() #Initializes pygame 

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE) #Tela
        pygame.display.set_caption("SpaceGame Demo")
        self.clock = pygame.time.Clock()

        self.running = True
        self.state = "Test"
        self.destination_id = 0

        self.level = Level(self.screen, self.destination_id)

    def run(self):
        # The main game loop
        while self.running:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
        
            #Game running logic

            dt = self.clock.tick(FPS) / 1000

            if (1):
                self.level.run(dt)

            pygame.display.update()

    pygame.quit()