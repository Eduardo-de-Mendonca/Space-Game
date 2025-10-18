from classes import *

class PlanetSurfaceScreen:
    def __init__(self, surface, planet):
        assert isinstance(surface, pygame.Surface)
        assert isinstance(planet, Planet)

        self.surface = surface # Uma referência para a "superfície" do pygame, onde faremos os desenhos
        self.planet = planet

    def tick(self):
        self.surface.fill(colors.black)
        self.planet.draw(self.surface)