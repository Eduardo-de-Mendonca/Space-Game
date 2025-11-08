#from Classes.SpaceStuff.space_level import *
from src.SpaceStuff.main_ship import *
from src.Others.input import InputHandler

from src.Others.helper import draw_text

# import temporário
from src.Config.save_data import *

class Game:
    def __init__(self):
        pygame.init() # Initializes pygame 

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) #Tela, tirei o resizable (explicação em melhorar.txt)
        pygame.display.set_caption("SpaceGame Demo")
        self.clock = pygame.time.Clock()

        self.running = True
        # self.state = "Test" - não acho que precisamos de uma máquina de estados aqui. A lógica de subtelas deve resolver isso.

        self.input_handler = InputHandler()

        self.save_data = SaveData()
        #self.level = SpaceLevel(self.screen, self.save_data) # Agora o level começa na tela do espaço! Ela que instancia os Levels de superfície quando necessário
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

            # Desenhar o FPS para debug
            if DEBUG_SHOW_FPS: draw_text(self.screen, str(int(self.clock.get_fps())), 0, 0)

            # Final Flip
            pygame.display.update()

    pygame.quit()