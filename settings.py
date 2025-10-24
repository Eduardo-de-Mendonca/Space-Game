from math import floor
import pygame

# Screen dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

# --- Player Settings ---
PLAYER_SPEED = 300
PLAYER_START_POS = (100, 100) # Starting in world pixels

# --- World & Chunk Settings ---
TILE_SIZE = 16 # Pixel size of a single tile
CHUNK_SIZE = 16 # How many tiles in one chunk (16x16)
CHUNK_SIZE_PIXELS = TILE_SIZE * CHUNK_SIZE

# Define a FINITE world size in chunks (e.g., 64x64 chunks)
# For an "infinite" world, you would remove this check
WORLD_SIZE_IN_CHUNKS = (64, 64)
WORLD_SIZE_PIXELS = (
    WORLD_SIZE_IN_CHUNKS[0] * CHUNK_SIZE_PIXELS,
    WORLD_SIZE_IN_CHUNKS[1] * CHUNK_SIZE_PIXELS
)
# How many chunks to load around the player (e.g., 5x5 grid)
LOAD_RADIUS_CHUNKS = 2 

# --- Tile Data Markers ---
# We store data in our map, not colors
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
        TILE_TYPE_DEEP_WATER: dark_blue,
        TILE_TYPE_WATER: light_blue,
        TILE_TYPE_SAND: light_yellow,
        TILE_TYPE_GRASS: light_green,
        TILE_TYPE_FOREST: dark_green,
        TILE_TYPE_ROCK: gray,
        TILE_TYPE_SNOW: white
    }


