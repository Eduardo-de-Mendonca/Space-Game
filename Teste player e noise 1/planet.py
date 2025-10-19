import pygame
from perlin_noise import PerlinNoise
from settings import *
import random
NOISE_ZOOM = 150

class Planet:
    def __init__(self, screen, id, group):

        self.all_sprites = group
        self.screen = screen
        #self.id = id
        self.id = random.randint(0,100)

        self.noise_generator = PerlinNoise(octaves=4, seed=self.id)

        self.tile_matrix = []

        self.generate_map()


    def generate_map(self):
        
        self.tile_matrix = []
        for i in range(y_tiles):
            row = []
            for j in range(x_tiles):

                noise_val = self.noise_generator([j / NOISE_ZOOM, i / NOISE_ZOOM])
                
                tt = terrain_thresholds2
                if noise_val < tt[0]:
                    color = colors.dark_blue
                elif noise_val < tt[1]:
                    color = colors.blue
                elif noise_val < tt[2]:
                    color = colors.light_yellow
                elif noise_val < tt[3]:
                    color = colors.light_green
                elif noise_val < tt[4]:
                    color = colors.dark_green
                elif noise_val < tt[5]:
                    color = colors.gray
                else:
                    color = colors.white
                
                row.append(color)
                
            self.tile_matrix.append(row)

    def print_map(self):
        print(self.tile_matrix)

    def draw(self):
        # A lógica de desenho
        for i in range(len(self.tile_matrix)):
            for j in range(len(self.tile_matrix[i])):
                rect = pygame.rect.Rect(j * tile_size_pixels, i * tile_size_pixels, tile_size_pixels, tile_size_pixels)
                
                pygame.draw.rect(self.screen, self.tile_matrix[i][j], rect)