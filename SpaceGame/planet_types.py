import settings
import pygame

class Universal_tilemap:
    '''Earth-like basic tiles'''
    TILE_TYPE_DEEP_WATER = 0
    TILE_TYPE_WATER = 1
    TILE_TYPE_SAND = 2
    TILE_TYPE_GRASS = 3
    TILE_TYPE_FOREST = 4
    TILE_TYPE_ROCK = 5
    TILE_TYPE_SNOW = 6

# --- Colors ---
class colors:
    black = pygame.Color(0, 0, 0)
    dark_blue = pygame.Color(0, 0, 153)
    blue = pygame.Color(80, 102, 255)
    light_blue = pygame.Color(80, 160, 255)
    light_yellow = pygame.Color(255, 255, 153)
    light_green = pygame.Color(102, 255, 102)
    dark_green = pygame.Color(0, 102, 0)
    gray = pygame.Color(153, 153, 153)
    white = pygame.Color(255, 255, 255)
    
    # A mapping to easily convert data to colors
    TILE_COLOR_MAP = {
        Universal_tilemap.TILE_TYPE_DEEP_WATER: dark_blue,
        Universal_tilemap.TILE_TYPE_WATER: light_blue,
        Universal_tilemap.TILE_TYPE_SAND: light_yellow,
        Universal_tilemap.TILE_TYPE_GRASS: light_green,
        Universal_tilemap.TILE_TYPE_FOREST: dark_green,
        Universal_tilemap.TILE_TYPE_ROCK: gray,
        Universal_tilemap.TILE_TYPE_SNOW: white
    }

class Planet_templates:
    
    EARTH_PLANET = {
        "template_id" : 1,

        "noise_continental": {"scale": 750, "octaves": 2, "weight": 0.7},
        "noise_elevation": {"scale": 80, "octaves": 4, "weight": 0.3},

        "tile_types" : [0,1,2,3,4,5,6],

        "thresholds": {
        "deep_water": 0.46,
        "water": 0.5,
        "sand": 0.53,
        "grass": 0.68,
        "forest": 0.72,
        "rock": 0.8
        },
    }