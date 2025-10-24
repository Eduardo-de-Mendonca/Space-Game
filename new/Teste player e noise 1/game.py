import pygame
from settings import *
from level import Level

class Game:
    def __init__(self):

        pygame.init() # Initializes pygame 

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
            # Event Handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                # Handle zoom events
                if event.type == pygame.MOUSEWHEEL:
                    self.level.camera.handle_zoom(event)
                
                # Handle debug map generation
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        print("Generating debug map...")
                        self.level.generate_debug_map()

            # Logic & Drawing
            dt = self.clock.tick(FPS) / 1000
            self.level.run(dt)
            
            # Final Flip
            pygame.display.update()

    pygame.quit()