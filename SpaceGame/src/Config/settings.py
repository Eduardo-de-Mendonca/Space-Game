from math import floor
import src.Others.helper as helper
import pygame
#import planet_types

# Screen dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

# --- Player Settings ---
PLAYER_SPEED = 100
PLAYER_START_POS = (100, 100) # Starting in world pixels
PLAYER_RELATIVE_SIZE = 0.5

# --- World & Chunk Settings ---
TILE_SIZE = 16*2 # Pixel size of a single tile
CHUNK_SIZE = 16 # How many tiles in one chunk (16x16)
CHUNK_SIZE_PIXELS = TILE_SIZE * CHUNK_SIZE

# Define a FINITE world size in chunks (e.g., 64x64 chunks)
# For an "infinite" world, you would remove this check
WORLD_SIZE_IN_CHUNKS = (64*1, 64*1)
WORLD_SIZE_PIXELS = (
    WORLD_SIZE_IN_CHUNKS[0] * CHUNK_SIZE_PIXELS,
    WORLD_SIZE_IN_CHUNKS[1] * CHUNK_SIZE_PIXELS
)
# How many chunks to load around the player (e.g., 5x5 grid)
LOAD_RADIUS_CHUNKS = 1

# -- Agora as settings do espaço
PLANET_IN_SPACE_RADIUS = 100

ASTEROID_GAME_WIDTH = SCREEN_WIDTH
ASTEROID_GAME_HEIGHT = SCREEN_HEIGHT