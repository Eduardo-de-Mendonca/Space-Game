#from Classes.SpaceStuff.space_level import *
from Classes.Fase_da_nave.main_nave import *

# import temporário
from Classes.Others.save_data import *

class Game:
    def __init__(self):
        pygame.init() # Initializes pygame 

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) #Tela, tirei o resizable (explicação em melhorar.txt)
        pygame.display.set_caption("SpaceGame Demo")
        self.clock = pygame.time.Clock()

        self.running = True
        # self.state = "Test" - não acho que precisamos de uma máquina de estados aqui. A lógica de subtelas deve resolver isso.

        self.save_data = SaveData()
        #self.level = SpaceLevel(self.screen, self.save_data) # Agora o level começa na tela do espaço! Ela que instancia os Levels de superfície quando necessário
        self.level = AsteroidsGame(self.screen, self.save_data)

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