import pygame

from src.PlanetSurfaceStuff.planet import Planet
from src.SpaceStuff.classes_ship import PlanetInSpace
from src.Config.planet_templates import PlanetTemplate, EARTH_PLANET, LAVA_PLANET

from src.SaveDataStuff.item import Item

class SaveData:
    '''
    Guarda todos os dados que planejamos salvar entre sessões de jogo. Saves ainda não estão implementados, mas é bom já ir guardando aqui em vez de usar variáveis globais.
    '''

    def __init__(self):
        self.all_planets = [
            PlanetInSpace(
                pygame.Vector2(500, 300),
                Planet(seed = 5117,template = EARTH_PLANET),
                3
            )
        ]

        self.inventory = [
            Item('Graveto nível 6', 3, pygame.image.load('src/Assets/graveto.png').convert_alpha()),
            Item('Espada nível 1', 1, pygame.image.load('src/Assets/espada.png').convert_alpha())]