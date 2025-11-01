import noise
from settings import *
import random
import settings

class Planet:
    """
    This class is now a PURE GENERATOR. It holds no map data.
    Its only job is to answer the question:
    "What is the tile data for the chunk at (chunk_x, chunk_y)?"
    """
    def __init__(self, seed=None):
        if seed is None:
            self.seed = random.randint(0, 10000)
        else:
            self.seed = seed
            
        print(f"Initializing planet with seed: {self.seed}")

    def get_continental_noise(self, world_x, world_y):
        # Layer 1: Massive continents. Low frequency, low detail.
        noise_scale_continental = 750 
        
        val = noise.snoise2(
            world_x / noise_scale_continental, 
            world_y / noise_scale_continental, 
            octaves=2, 
            persistence=0.5, 
            lacunarity=2.0, 
            base=self.seed
        )
        val = (val +1)/2
        return val
    
    def get_elevation_noise(self, world_x, world_y):
        # Layer 2: Hills and mountains. Medium frequency, high detail.
        noise_scale_elevation = 120
        
        val = noise.snoise2(
            world_x / noise_scale_elevation, 
            world_y / noise_scale_elevation, 
            octaves=4, 
            persistence=0.5, 
            lacunarity=2.0, 
            base=self.seed + 1 # Use a different seed!
        )
        val = (val +1)/2
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
                q_x = noise.snoise2(world_x / 100, world_y / 100)
                q_y = noise.snoise2(world_x / 100 + 5.2, world_y / 100 + 1.3)
                # 1. Get Continental Noise
                continental_val = self.get_continental_noise(world_x + (q_x*75), world_y + (q_y*75))
                elevation_val = self.get_elevation_noise(world_x + (q_x*5), world_y + (q_y*5))

                final_elevation_val = continental_val*0.7 + elevation_val*0.3

                tile_type = TILE_TYPE_DEEP_WATER # Default
                
                # 2. Decide Land or Water
                if final_elevation_val < 0.46:
                    tile_type = TILE_TYPE_DEEP_WATER
                elif final_elevation_val < 0.5:
                    tile_type = TILE_TYPE_WATER
                else: 
                    #final_elevation_val = 0.6
                    if final_elevation_val< 0.53:
                        tile_type = TILE_TYPE_SAND
                    elif final_elevation_val < 0.68:
                        tile_type = TILE_TYPE_GRASS
                    #elif final_elevation_val < 0.72:
                    #    tile_type = TILE_TYPE_FOREST
                    elif final_elevation_val < 0.8:
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
            pygame.image.save(map_surface, f"debug_map_{self.seed}.png")
            print("Successfully saved debug_map.png to your project folder.")
        except Exception as e:
            print(f"Error saving debug map: {e}")


