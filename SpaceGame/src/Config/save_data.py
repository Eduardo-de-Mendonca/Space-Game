from src.PlanetSurfaceStuff.planet import Planet
from src.Config.planet_templates import PlanetTemplate, EARTH_PLANET, LAVA_PLANET
class SaveData:
    '''
    Guarda todos os dados que planejamos salvar entre sessões de jogo. Saves ainda não estão implementados, mas é bom já ir guardando aqui em vez de usar variáveis globais.
    '''

    def __init__(self):
        self.all_planets = [Planet(seed = 5117,template = EARTH_PLANET)]