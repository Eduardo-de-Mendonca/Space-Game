import pygame

from src.PlanetSurfaceStuff.planet import Planet
from src.SpaceStuff.classes_ship import PlanetInSpace
from src.Config.planet_templates import PlanetTemplate, EARTH_PLANET, LAVA_PLANET

from src.SaveDataStuff.item import ItemKind

class SaveData:
    '''
    Guarda todos os dados que planejamos salvar entre sessões de jogo. Saves ainda não estão implementados, mas é bom já ir guardando aqui em vez de usar variáveis globais.
    '''

    def __init__(self):
        self.all_planets = [
            PlanetInSpace(
                pygame.Vector2(1000, 300),
                Planet(seed = 5117,template = EARTH_PLANET),
                1
            )
        ]

        self.all_item_kinds = self.generate_item_kinds()
        assert isinstance(self.all_item_kinds[0], ItemKind)

        self.inventory = [
            self.all_item_kinds[0].to_item(1)
            ]
        
    def generate_item_kinds(self):
        '''
        Retorna uma lista com vários tipos de item
        '''
        pixel_art = pygame.image.load('src/Assets/icones_armas.png').convert_alpha()
        
        result = []
        total_item_amount = 10*9 + 1
        i = 0
        x = 0
        y = 0
        rarity_multiplier = 1.0
        multiplier_increment = (2.0 - 1.0)/total_item_amount

        while i < total_item_amount:
            img = pixel_art.subsurface((x, y), (32, 32))

            result.append(
                ItemKind(
                    round(rarity_multiplier, 1),
                    img
                )
            )

            i += 1
            x += 32
            if x >= 320:
                x = 0
                y += 32
            rarity_multiplier += multiplier_increment

        return result
