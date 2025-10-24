
from Classes.PlanetSurfaceStuff.player import *
from Classes.Others.camera import Camera
from Classes.Others.save_data import *

class Level: #Level é um cenário genérico, acho que é tipo o screen que o Edu usava
    '''
    Um objeto Level representa a tela quando você está na superfície de um planeta
    '''
    def __init__(self, screen, save_data, planet, camera):
        assert isinstance(screen, pygame.Surface)
        assert isinstance(save_data, SaveData)
        assert isinstance(planet, Planet)

        self.screen = screen
        self.all_sprites = pygame.sprite.Group()

        # The Planet is now just a seed and a generator
        self.planet = planet
        
        # The player is created at a WORLD position
        self.player = Player(PLAYER_START_POS, self.all_sprites)
        
        # The camera will follow the player
        self.camera = camera
        
        # This dictionary will hold the *active* chunk data
        self.loaded_chunks = {}

    def manage_chunks(self):
        """
        Loads new chunks that enter the camera's view and unloads old ones.
        """
        visible_chunks_x, visible_chunks_y = self.camera.get_visible_chunk_coords()
        
        # --- Load new chunks ---
        chunks_to_load = set()
        for cx in visible_chunks_x:
            for cy in visible_chunks_y:
                # Check if chunk is within finite world bounds
                if not (0 <= cx < WORLD_SIZE_IN_CHUNKS[0] and 0 <= cy < WORLD_SIZE_IN_CHUNKS[1]):
                    continue # Skip chunks outside the world
                    
                chunk_coord = (cx, cy)
                if chunk_coord not in self.loaded_chunks:
                    # Not loaded yet, so generate it and add to dictionary
                    self.loaded_chunks[chunk_coord] = self.planet.generate_chunk_data(cx, cy)

        # --- Unload old chunks ---
        chunks_to_unload = set()
        for chunk_coord in self.loaded_chunks:
            cx, cy = chunk_coord
            if cx not in visible_chunks_x or cy not in visible_chunks_y:
                chunks_to_unload.add(chunk_coord)
                
        for chunk_coord in chunks_to_unload:
            del self.loaded_chunks[chunk_coord]

    def draw_world(self):
        """
        Draws only the visible tiles from the loaded chunks.
        """
        zoomed_tile_size = floor(TILE_SIZE * self.camera.zoom)
        if zoomed_tile_size <= 0: return # Don't draw if tiles are invisible
        
        for chunk_coord, chunk_data in self.loaded_chunks.items():
            chunk_x, chunk_y = chunk_coord
            
            for local_y, row in enumerate(chunk_data):
                for local_x, tile_type in enumerate(row):
                    
                    # Get tile's world pixel position
                    world_x = (chunk_x * CHUNK_SIZE + local_x) * TILE_SIZE
                    world_y = (chunk_y * CHUNK_SIZE + local_y) * TILE_SIZE
                    
                    # Convert to screen position using the camera
                    screen_pos = self.camera.world_to_screen(pygame.math.Vector2(world_x, world_y))
                    
                    # Create the zoomed rect
                    rect = pygame.Rect(
                        floor(screen_pos.x),
                        floor(screen_pos.y),
                        zoomed_tile_size,
                        zoomed_tile_size
                    )
                    
                    # Draw the tile
                    color = colors.TILE_COLOR_MAP.get(tile_type, colors.black)
                    pygame.draw.rect(self.screen, color, rect)

    def draw_sprites(self):
        """
        Draws all sprites, correctly offset by the camera.
        """
        for sprite in self.all_sprites:
            # Get sprite's world rect
            world_rect = sprite.rect
            assert isinstance(world_rect, pygame.Rect)
            
            # Convert to screen rect
            screen_pos = self.camera.world_to_screen(world_rect.topleft)
            zoomed_width = floor(world_rect.width * self.camera.zoom)
            zoomed_height = floor(world_rect.height * self.camera.zoom)
            
            screen_rect = pygame.Rect(
                floor(screen_pos.x),
                floor(screen_pos.y),
                zoomed_width,
                zoomed_height
            )
            
            # Scale the image if needed (can be slow, better to pre-scale)
            scaled_image = pygame.transform.scale(sprite.image, (zoomed_width, zoomed_height))
            self.screen.blit(scaled_image, screen_rect)

    def run(self, dt):
        self.screen.fill('black')

        # --- Update Phase ---
        self.camera.update(self.player.position)
        self.all_sprites.update(dt)
        self.manage_chunks()
        
        # --- Draw Phase ---
        self.draw_world()
        self.draw_sprites()
        
    def generate_debug_map(self):
        self.planet.generate_debug_map()