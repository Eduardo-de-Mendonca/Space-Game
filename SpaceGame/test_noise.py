import noise
import random
import settings
from settings import *

def dumb_noise(x,y):
    NOISE_ZOOM = 10.0
    # sample at tile centers (avoid integer lattice)
    fx = (x + 0.5) / NOISE_ZOOM
    fy = (y + 0.5) / (NOISE_ZOOM*0.7)

    v1 = noise.pnoise2(fx + 0.321, fy - 0.456, octaves=1, base=seed)
    v2 = noise.pnoise2(fx*2.0 + 2.34, fy*2.0 + 1000.0, octaves=2, base=seed+1)
    v3 = noise.pnoise2(fx*3.0 + 0.1, fy*3.0 - 20.0, octaves=1, base=seed+2)

    # map each to 0..1
    v1 = (v1 + 1.0) * 0.5
    v2 = (v2 + 1.0) * 0.5
    v3 = (v3 + 1.0) * 0.5

    # weighted blend
    return (v1 + 0.5 * v2 + 0.25 * v3) / (1.0 + 0.5 + 0.25)

def get_continental_noise(local_x, local_y):
    # Layer 1: Massive continents. Low frequency, low detail.
    noise_scale_continental = 750 
    
    val = noise.snoise2(
        local_x / noise_scale_continental, 
        local_y / noise_scale_continental, 
        octaves=2, 
        persistence=0.5, 
        lacunarity=2.0, 
        base= seed
    )
    return val

def get_elevation_noise(local_x, local_y):
    # Layer 2: Hills and mountains. Medium frequency, high detail.
    noise_scale_elevation = 80
    
    val = noise.snoise2(
        local_x / noise_scale_elevation, 
        local_y / noise_scale_elevation, 
        octaves=4, 
        persistence=0.5, 
        lacunarity=2.0, 
        base= seed + 1
    )
    return val

def generate_terrain(terrain_data):
    for local_y in range(y_tiles):
        row = []
        for local_x in range(x_tiles):
            
            # 1. Get Continental Noise
            continental_val = get_continental_noise(local_x, local_y)
            #continental_val = dumb_noise(local_x,local_y)
            continental_val = (continental_val + 1)/2
            #continental_val = (noise.snoise2(local_x/300, local_y/300, octaves = 3, base = seed) + 1)/2

            tile_type = TILE_TYPE_DEEP_WATER
            
            # 2. Decide Land or Water
            if continental_val < 0.3:
                tile_type = TILE_TYPE_DEEP_WATER
            elif continental_val < 0.5:
                tile_type = TILE_TYPE_WATER
            else: 
                # This is LAND. Now check elevation
                #elevation_val = get_elevation_noise(local_x, local_y)
                #elevation_val = (elevation_val + 1)/2
                elevation_val = 0.5
                # Apply thresholds to the elevation noise
                # These are "crammed" around 0.0 to fight the bell-curve
                if elevation_val < 0.3:
                    tile_type = TILE_TYPE_SAND
                elif elevation_val < 0.6:
                    tile_type = TILE_TYPE_GRASS
                elif elevation_val < 0.7:
                    tile_type = TILE_TYPE_FOREST
                elif elevation_val < 0.8:
                    tile_type = TILE_TYPE_ROCK
                else:
                    tile_type = TILE_TYPE_SNOW
            
            row.append(tile_type)
        terrain_data.append(row)
    print(f"Seed = {seed}")
    return terrain_data

def print_tile_matrix(terrain_data):
    print(terrain_data)

def draw_terrain(terrain_data):
    pass

def generate_debug_map(terrain_data):
    """
    Generates a 1-pixel-per-tile map of the *entire* finite world.
    This is your "bird's-eye view" for debugging.
    """
    print("Generating debug map (this may take a moment)...")
    world_width_tiles = x_tiles
    world_height_tiles = y_tiles
    
    # Create a surface to draw on
    map_surface = pygame.Surface((world_width_tiles, world_height_tiles))
    
    for y, row in enumerate(terrain_data):
        for x, tile_type in enumerate(row):
            
            color = colors.TILE_COLOR_MAP.get(tile_type, colors.black)
            map_surface.set_at((x, y), color)
    
    try:
        pygame.image.save(map_surface, "debug_map.png")
        print("Successfully saved debug_map.png to your project folder.")
    except Exception as e:
        print(f"Error saving debug map: {e}")

def main():
    global seed, x_tiles, y_tiles
    terrain_data = []
    seed = random.randint(0,1000)
    seed = 938
    x_tiles = 1000*5
    y_tiles = 1000*5

    terrain_data = generate_terrain(terrain_data)
    #print_tile_matrix(terrain_data)
    generate_debug_map(terrain_data)

if __name__ == "__main__":
    main()