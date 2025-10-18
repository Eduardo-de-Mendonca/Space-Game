from settings import *
import noise

class Planet:
    def __init__(self, deep_water_color, water_color, sand_color, grass_color, forest_color, rock_color, snow_color):
        self.deep_water_color = deep_water_color
        self.water_color = water_color
        self.sand_color = sand_color
        self.grass_color = grass_color
        self.forest_color = forest_color
        self.rock_color = rock_color
        self.snow_color = snow_color

        self.tile_matrix = [[None for _ in range(planet_size_x_tiles)] for _ in range(planet_size_y_tiles)]

        for i in range(planet_size_y_tiles):
            for j in range(planet_size_x_tiles):
                self.tile_matrix[i][j] = self.__generate_noise_color(i, j)

    def __generate_noise_color(self, i, j):
        noise_value = noise.pnoise2(i/noise_scale, j/noise_scale, repeatx=planet_size_x_tiles/noise_scale, repeaty=planet_size_y_tiles/noise_scale, base=noise_seed)
        # repeatx e repeaty garantem que o planeta "se conecta" nas bordas

        tt = terrain_thresholds
        if noise_value < tt[0]:
            color = self.deep_water_color
        elif noise_value < tt[1]:
            color = self.water_color
        elif noise_value < tt[2]:
            color = self.sand_color
        elif noise_value < tt[3]:
            color = self.grass_color
        elif noise_value < tt[4]:
            color = self.forest_color
        elif noise_value < tt[5]:
            color = self.rock_color
        else:
            color = self.snow_color

        return color
    
    def draw(self, surface):
        assert isinstance(surface, pygame.Surface)

        for i in range(len(self.tile_matrix)):
            for j in range(len(self.tile_matrix[i])):

                rect = pygame.rect.Rect(
                    j * tile_size_pixels,
                    i * tile_size_pixels,
                    tile_size_pixels,
                    tile_size_pixels
                )

                pygame.draw.rect(
                    surface,
                    self.tile_matrix[i][j],
                    rect
                )