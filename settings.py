import pygame
import random

class colors:
    black = pygame.Color(0, 0, 0)

    dark_blue = pygame.Color(0, 0, 153)
    blue = pygame.Color(51, 102, 255)
    light_yellow = pygame.Color(255, 255, 153)
    light_green = pygame.Color(102, 255, 102)
    dark_green = pygame.Color(0, 102, 0)
    gray = pygame.Color(153, 153, 153)
    white = pygame.Color(255, 255, 255)

FPS = 60

planet_size_x_tiles = 100
planet_size_y_tiles = 100
tile_size_pixels = 5
noise_scale = 10.0

terrain_thresholds = []
for i in range(1, 7):
    terrain_thresholds.append(-1.0 + (i * (2.0 / 7.0)))

noise_seed = random.randint(0, 100)
print(noise_seed)
'''
O noise sempre retorna 0.0 para números inteiros. Para chamar noise, dividiremos as coordenadas na matriz de tiles pelo noise_scale. noise_scale é maior que 1. Quanto mais próximo de 1, mais rápido o terreno varia. Quanto maior, mais suave ele fica.
'''

