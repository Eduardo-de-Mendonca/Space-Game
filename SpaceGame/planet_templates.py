from dataclasses import dataclass, field
import pygame
from enum import IntEnum # Bonus suggestion!

# Bonus: Use IntEnum for your tiles. It's cleaner.
class TileType(IntEnum):
    DEEP_WATER = 0
    WATER = 1
    SAND = 2
    GRASS = 3
    FOREST = 4
    ROCK = 5
    SNOW = 6
    LAVA = 7
    ASH = 8
    OBSIDIAN = 9

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
    red = (255, 0, 0)
    
    # A mapping to easily convert data to colors
    TILE_COLOR_MAP = {
        TileType.DEEP_WATER: dark_blue,
        TileType.WATER: light_blue,
        TileType.SAND: light_yellow,
        TileType.GRASS: light_green,
        TileType.FOREST: dark_green,
        TileType.ROCK: gray,
        TileType.SNOW: white,
        TileType.LAVA: red,
        TileType.ASH: gray,
        TileType.OBSIDIAN: black
    }

# --- DATA STRUCTURE DEFINITIONS ---
@dataclass
class NoiseConfig:
    scale: float
    octaves: int
    weight: float

@dataclass
class PlanetThresholds:
    deep_water: float
    water: float
    sand: float
    grass: float
    forest: float
    rock: float
    # snow is just anything above 'rock'

@dataclass
class PlanetTileMap:
    deep_water: TileType = TileType.DEEP_WATER
    water: TileType = TileType.WATER
    sand: TileType = TileType.SAND
    grass: TileType = TileType.GRASS
    forest: TileType = TileType.FOREST
    rock: TileType = TileType.ROCK
    snow: TileType = TileType.SNOW

@dataclass
class PlanetTemplate:
    template_id: int
    name: str
    continental_noise: NoiseConfig
    elevation_noise: NoiseConfig
    thresholds: PlanetThresholds
    tile_map: PlanetTileMap


# --- TEMPLATE DEFINITIONS ---
# Now you just create *instances* of your data classes
# Your IDE will help you fill this out!

EARTH_PLANET = PlanetTemplate(
    template_id=1,
    name="Earthen",
    continental_noise=NoiseConfig(scale=750, octaves=2, weight=0.7),
    elevation_noise=NoiseConfig(scale=120, octaves=4, weight=0.3),
    thresholds=PlanetThresholds(
        deep_water=0.46,
        water=0.5,
        sand=0.53,
        grass=0.68,
        forest=0.72,
        rock=0.8
    ),
    tile_map=PlanetTileMap() # Uses all the defaults
)

LAVA_PLANET = PlanetTemplate(
    template_id=2,
    name="Volcanic",
    continental_noise=NoiseConfig(scale=600, octaves=4, weight=0.5),
    elevation_noise=NoiseConfig(scale=75, octaves=2, weight=0.5),
    thresholds=PlanetThresholds(
        deep_water=0.3,
        water=0.45,
        sand=0.6,
        grass=0.7,
        forest=0.8,
        rock=0.85
    ),
    tile_map=PlanetTileMap(
        deep_water=TileType.LAVA,
        water=TileType.LAVA,
        sand=TileType.OBSIDIAN,
        grass=TileType.ASH,
        forest=TileType.ASH,
        rock=TileType.ROCK,
        snow=TileType.ROCK # No snow on a lava planet
    )
)

# --- MANAGER DICTIONARY ---
TEMPLATES_BY_ID = {
    1: EARTH_PLANET,
    2: LAVA_PLANET
}