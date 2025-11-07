from Classes.PlanetSurfaceStuff.planet import Planet
from planet_templates import PlanetTemplate,EARTH_PLANET,LAVA_PLANET

class SaveData:
    '''
    Guarda todos os dados que planejamos salvar entre sessões de jogo. Saves ainda não estão implementados, mas é bom já ir guardando aqui em vez de usar variáveis globais.
    '''

    def __init__(self):
        self.all_planets = [Planet(template = LAVA_PLANET)]