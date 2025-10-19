from math import floor
import pygame

# Screen dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

# Player settings
PLAYER_SPEED = 300

tile_size_pixels = 5

x_tiles = floor(1280/tile_size_pixels)
y_tiles= floor(x_tiles*(72/128))

terrain_thresholds1 = [0.3, 0.4, 0.5, 0.75, 0.8 , 0.9]
terrain_thresholds2 = [0.001, 0.01, 0.045, 0.2, 0.35 , 0.4]

class colors:
    black = pygame.Color(0, 0, 0)
    dark_blue = pygame.Color(0, 0, 153)
    blue = pygame.Color(51, 102, 255)
    light_yellow = pygame.Color(255, 255, 153)
    light_green = pygame.Color(102, 255, 102)
    dark_green = pygame.Color(0, 102, 0)
    gray = pygame.Color(153, 153, 153)
    white = pygame.Color(255, 255, 255)
