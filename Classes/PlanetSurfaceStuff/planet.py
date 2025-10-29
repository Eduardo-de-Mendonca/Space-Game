import noise
from settings import *
import random

class Planet:
    """
    wip
    """
    def __init__(self, seed=None):
        if seed is None:
            self.seed = random.randint(0, 1000)
        else:
            self.seed = seed
            
        print(f"Initializing planet with seed: {self.seed}")

    def get_continental_noise(self, world_x, world_y):
        # Layer 1: Massive continents. Low frequency, low detail.
        noise_scale_continental = 750 
        
        val = noise.pnoise2(
            world_x / noise_scale_continental, 
            world_y / noise_scale_continental, 
            octaves=2, 
            persistence=0.5, 
            lacunarity=2.0, 
            base=self.seed
        )
        return val
    
    def get_elevation_noise(self, world_x, world_y):
        # Layer 2: Hills and mountains. Medium frequency, high detail.
        noise_scale_elevation = 80.0
        
        val = noise.pnoise2(
            world_x / noise_scale_elevation, 
            world_y / noise_scale_elevation, 
            octaves=6, 
            persistence=0.5, 
            lacunarity=2.0, 
            base=self.seed + 1 # Use a different seed!
        )
        return val

    def generate_chunk_data(self, chunk_x, chunk_y):
        """
        Generates the tile data for a single chunk.
        This is the new core of your world generation.
        """
        chunk_data = []
        for local_y in range(CHUNK_SIZE):
            row = []
            for local_x in range(CHUNK_SIZE):
                
                # Calculate the tile's position in the entire world
                world_x = (chunk_x * CHUNK_SIZE) + local_x
                world_y = (chunk_y * CHUNK_SIZE) + local_y

                # --- Multi-Layer Noise Logic ---
                
                # 1. Get Continental Noise
                continental_val = self.get_continental_noise(world_x, world_y)
                
                tile_type = TILE_TYPE_DEEP_WATER # Default
                
                # 2. Decide Land or Water
                if continental_val < -0.2:
                    tile_type = TILE_TYPE_DEEP_WATER
                elif continental_val < 0.0:
                    tile_type = TILE_TYPE_WATER
                else: 
                    # --- This is LAND. Now check elevation. ---
                    elevation_val = self.get_elevation_noise(world_x, world_y)
                    #elevation_val = 0.1
                    # Apply thresholds to the elevation noise
                    # These are "crammed" around 0.0 to fight the bell-curve
                    if elevation_val < -0.4:
                        tile_type = TILE_TYPE_SAND
                    elif elevation_val < 0.2:
                        tile_type = TILE_TYPE_GRASS
                    elif elevation_val < 0.3:
                        tile_type = TILE_TYPE_FOREST
                    elif elevation_val < 0.5:
                        tile_type = TILE_TYPE_ROCK
                    else:
                        tile_type = TILE_TYPE_SNOW
                
                row.append(tile_type)
            chunk_data.append(row)
        
        return chunk_data

    def generate_debug_map(self):
        """
        Generates a 1-pixel-per-tile map of the *entire* finite world.
        This is your "bird's-eye view" for debugging.
        """
        print("Generating debug map (this may take a moment)...")
        world_width_tiles = WORLD_SIZE_IN_CHUNKS[0] * CHUNK_SIZE
        world_height_tiles = WORLD_SIZE_IN_CHUNKS[1] * CHUNK_SIZE
        
        # Create a surface to draw on
        map_surface = pygame.Surface((world_width_tiles, world_height_tiles))
        
        for cx in range(WORLD_SIZE_IN_CHUNKS[0]):
            for cy in range(WORLD_SIZE_IN_CHUNKS[1]):
                chunk_data = self.generate_chunk_data(cx, cy)
                for local_y, row in enumerate(chunk_data):
                    for local_x, tile_type in enumerate(row):
                        
                        world_x = (cx * CHUNK_SIZE) + local_x
                        world_y = (cy * CHUNK_SIZE) + local_y
                        
                        color = colors.TILE_COLOR_MAP.get(tile_type, colors.black)
                        map_surface.set_at((world_x, world_y), color)
        
        try:
            pygame.image.save(map_surface, "debug_map.png")
            print("Successfully saved debug_map.png to your project folder.")
        except Exception as e:
            print(f"Error saving debug map: {e}")


