import noise
from src.Config.settings import *
import random
from src.Config.planet_templates import *

class Planet:
    """
    This class is now a PURE GENERATOR. It holds no map data.
    Its only job is to answer the question:
    "What is the tile data for the chunk at (chunk_x, chunk_y)?"
    """
    def __init__(self, seed=None, template: PlanetTemplate = EARTH_PLANET):
        if seed is None:
            self.seed = random.randint(0, 10000)
        else:
            self.seed = seed
        
        self.template = template
            
        print(f"Initializing planet with seed: {self.seed}")
        print(f"Initializing planet with template: {self.template.template_id,self.template.name}")

    def get_continental_noise(self, world_x, world_y):
        # Layer 1: Massive continents. Low frequency, low detail.
        noise_scale_continental = self.template.continental_noise.scale
        continental_octaves = self.template.continental_noise.octaves

        val = noise.snoise2(
            world_x / noise_scale_continental, 
            world_y / noise_scale_continental, 
            octaves=continental_octaves, 
            persistence=0.5, 
            lacunarity=2.0, 
            base=self.seed
        )
        val = (val +1)/2
        return val
    
    def get_elevation_noise(self, world_x, world_y):
        # Layer 2: Hills and mountains. Medium frequency, high detail.
        noise_scale_elevation = self.template.elevation_noise.scale
        elevation_octaves = self.template.elevation_noise.octaves
        
        val = noise.snoise2(
            world_x / noise_scale_elevation, 
            world_y / noise_scale_elevation, 
            octaves=elevation_octaves, 
            persistence=0.5, 
            lacunarity=2.0, 
            base=self.seed + 1 # Use a different seed!
        )
        val = (val +1)/2
        return val

    def get_object_noise(self, world_x, world_y):
        noise_scale = 10.0 # Pequeno, para ser "pontilhado"
        val = noise.snoise2(
            world_x / noise_scale, 
            world_y / noise_scale, 
            octaves=1, 
            base=self.seed + 2 # Seed diferente!
        )
        val = (val +1)/2 # 0.0 to 1.0
        return val

    def generate_chunk_data(self, chunk_x, chunk_y):
        """
        Atualizada. Agora o chunk consiste de duas camadas: Terreno e Objeto
        """
        terrain_data = []
        object_data = []

        for local_y in range(CHUNK_SIZE):
            terrain_row = []
            object_row = []
            for local_x in range(CHUNK_SIZE):
                
                # Calculate the tile's position in the entire world
                world_x = (chunk_x * CHUNK_SIZE) + local_x
                world_y = (chunk_y * CHUNK_SIZE) + local_y

                #Usa Domain-Warping para gerar terreno mais realista e distorcido
                q_x = noise.snoise2(world_x / 100, world_y / 100)
                q_y = noise.snoise2(world_x / 100 + 5.2, world_y / 100 + 1.3)

                # Get Terrain Noise
                continental_val = self.get_continental_noise(world_x + (q_x*75), world_y + (q_y*75))
                elevation_val = self.get_elevation_noise(world_x + (q_x*5), world_y + (q_y*5))

                pc,pe = self.template.continental_noise.weight, self.template.elevation_noise.weight #Pesos do template
                final_elevation_val = continental_val*pc + elevation_val*pe #Cálculo dos pesos

                tile_type = self.template.tile_map.deep_water # Default
                
                thresholds = self.template.thresholds #Thresholds

                # Decide Terrain tiles
                if final_elevation_val < thresholds.deep_water:
                    tile_type = self.template.tile_map.deep_water
                elif final_elevation_val < thresholds.water:
                    tile_type = self.template.tile_map.water
                else: 
                    if final_elevation_val< thresholds.sand:
                        tile_type = self.template.tile_map.sand
                    elif final_elevation_val < thresholds.grass:
                        tile_type = self.template.tile_map.grass
                    elif final_elevation_val < thresholds.forest:
                        tile_type = self.template.tile_map.forest
                    elif final_elevation_val < thresholds.rock:
                        tile_type = self.template.tile_map.rock
                    else:
                        tile_type = self.template.tile_map.snow
                
                terrain_row.append(tile_type)

                # Agora gerar e decidir a camada de objetos

                object_type = ObjectType.NONE

                object_noise_val = self.get_object_noise(world_x, world_y)

                if TILE_PROPERTIES[tile_type]["walkable"]:
                    if tile_type == TileType.GRASS:
                        if object_noise_val > 0.8: # "20% de chance" determinístico
                            object_type = ObjectType.TREE

                object_row.append(object_type)

            terrain_data.append(terrain_row)
            object_data.append(object_row)
        
        chunk_data = [terrain_data, object_data]
        return chunk_data

    def generate_debug_map(self):
        """
        Generates a 1-pixel-per-tile map of the *entire* finite world.
        This is your "bird's-eye view" for debugging.
        (Atualizado para desenhar objetos também)
        """
        print("Generating debug map (this may take a moment)...")
        world_width_tiles = WORLD_SIZE_IN_CHUNKS[0] * CHUNK_SIZE
        world_height_tiles = WORLD_SIZE_IN_CHUNKS[1] * CHUNK_SIZE
        
        # Create a surface to draw on
        map_surface = pygame.Surface((world_width_tiles, world_height_tiles))
        
        for cx in range(WORLD_SIZE_IN_CHUNKS[0]):
            for cy in range(WORLD_SIZE_IN_CHUNKS[1]):
                
                # Agora retorna duas camadas
                terrain_data, object_data = self.generate_chunk_data(cx, cy)
                
                for local_y in range(CHUNK_SIZE):
                    for local_x in range(CHUNK_SIZE):
                        
                        world_x = (cx * CHUNK_SIZE) + local_x
                        world_y = (cy * CHUNK_SIZE) + local_y
                        
                        # Camada 1: Terreno
                        tile_type = terrain_data[local_y][local_x]
                        color = colors.TILE_COLOR_MAP.get(tile_type, colors.black)
                        map_surface.set_at((world_x, world_y), color)
                        
                        # Camada 2: Objeto (com fallback de cor)
                        object_type = object_data[local_y][local_x]
                        if object_type != ObjectType.NONE:
                            obj_color = colors.OBJECT_COLOR_MAP.get(object_type)
                            if obj_color:
                                map_surface.set_at((world_x, world_y), obj_color)
        
        try:
            pygame.image.save(map_surface, f"debug_map_{self.seed}_{self.template.name}.png")
            print("Successfully saved debug_map.png to your project folder.")
        except Exception as e:
            print(f"Error saving debug map: {e}")