# Antes de tudo, importar pygame, para os módulos importados já poderem usar pygame
import pygame
pygame.init()

from src.Others.input import InputHandler
from src.Others.helper import draw_text

from src.SpaceStuff.main_ship import *
from src.GameOverStuff.game_over import GameOverScreen, game_over_states

# import temporário
from src.SaveDataStuff.save_data import *

class Game:
    def __init__(self):
        pygame.init() # Initializes pygame 

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) #Tela, tirei o resizable (explicação em melhorar.txt)
        pygame.display.set_caption("SpaceGame Demo")
        self.clock = pygame.time.Clock()

        self.running = True

        self.input_handler = InputHandler()

        self.save_data = SaveData()

        self.level = AsteroidsGame(self.screen, self.input_handler, self.save_data)

    def run(self):
        # The main game loop
        while self.running:
            # Event Handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                # Handle zoom events
                if event.type == pygame.MOUSEWHEEL:
                    self.input_handler.next_input.mousewheel_x = event.x
                    self.input_handler.next_input.mousewheel_y = event.y

                    # Agora, qualquer comportamento que use esse input (como handle_zoom) será chamado dentro da tela correspondente. E todas as telas têm acesso a ele.

            # Logic & Drawing
            dt = self.clock.tick(FPS) / 1000

            self.level.run(dt)

            # Gerenciar game over
            if isinstance(self.level, AsteroidsGame):
                if self.level.state == asteroids_game_states.GAME_OVER:
                    self.level = GameOverScreen(self.screen, self.input_handler)
            elif isinstance(self.level, GameOverScreen):
                if self.level.state == game_over_states.RESTART:
                    self.level = AsteroidsGame(self.screen, self.input_handler, self.save_data)
                elif self.level.state == game_over_states.QUIT:
                    self.running = False

            # Desenhar o FPS para debug
            if DEBUG_SHOW_FPS: draw_text(self.screen, str(int(self.clock.get_fps())), 0, 0)

            # Final Flip
            pygame.display.update()

    pygame.quit()