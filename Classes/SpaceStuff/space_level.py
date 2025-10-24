from Classes.SpaceStuff.space_classes import SpaceShip, PlanetInSpace
from Classes.PlanetSurfaceStuff.level import *

class SpaceLevel:
    '''
    Um objeto SpaceLevel representa a tela quando você está no espaço, navegando entre planetas
    '''
    def __init__(self, screen, save_data):
        assert isinstance(screen, pygame.Surface)
        assert isinstance(save_data, SaveData)

        self.screen = screen
        
        # The player is created at a WORLD position
        self.space_ship = SpaceShip()
        
        # The camera will follow the player
        self.camera = Camera()

        self.save_data = save_data
        self.planets = [PlanetInSpace(pygame.math.Vector2(500, 300), save_data.all_planets[0])]

        self.sublevel = None # A subtela pode vir a ser um Level, na superfície de um planeta

    def check_collisions(self):
        '''
        Checa colisões entre a nave espacial e planetas. Se houver colisão, retorna o índice do planeta com o qual colidimos. Fora isso, retorna None.
        '''
        for i in range(len(self.planets)):
            planet = self.planets[i]
            distance = self.space_ship.position.distance_to(planet.position)
            if distance < planet.radius:
                return i

        return None

    def run(self, dt):
        if self.sublevel != None:
            # Aqui está a mágica da lógica de subtelas! Se minha subtela não é None, eu apenas rodo ela
            self.sublevel.run(dt)
            return

        self.screen.fill('black')

        # --- Update Phase ---
        self.camera.update(self.space_ship.position)
        self.space_ship.update(dt)

        # -- Collision Check Phase ---
        collided_planet_index = self.check_collisions()
        if collided_planet_index != None:
            destination_id = 0

            self.sublevel = Level(self.screen, self.save_data, self.save_data.all_planets[destination_id])
        
        # --- Draw Phase ---
        self.space_ship.draw(self.screen, self.camera)
        for planet in self.planets:
            planet.draw(self.screen, self.camera)