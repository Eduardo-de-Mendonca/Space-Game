from settings import *

class Camera:
    def __init__(self):
        # Offset is the camera's top-left corner in *world* pixel coordinates
        self.offset = pygame.math.Vector2(0, 0)
        
        self.zoom = 0.25
        self.min_zoom = 0.25
        self.max_zoom = 4.0
        self.zoom_speed = 0.05

    def update(self, position):
        """
        Updates the camera's offset to smoothly follow the target position.
        """
        # Dudu: mudei isso. Em vez de receber o target e ler position, recebe logo a position. Isso torna mais fácil a câmera seguir diferentes tipos de objetos
        
        assert isinstance(position, pygame.math.Vector2)
        # Calculate target position to center the player
        # We divide by zoom to correct the offset as we zoom in/out
        target_pos = position - pygame.math.Vector2(SCREEN_WIDTH / (2 * self.zoom), SCREEN_HEIGHT / (2 * self.zoom))
        
        # Use linear interpolation (lerp) for smooth, dampened movement
        # The 0.1 is the "lag" factor. Higher = snappier, Lower = smoother
        self.offset += (target_pos - self.offset) * 0.1 

    def handle_zoom(self, event):
        """
        Handles zoom controls via the mouse wheel.
        """
        if event.y > 0: # Scroll up
            self.zoom = min(self.max_zoom, self.zoom * (1 + self.zoom_speed))
        elif event.y < 0: # Scroll down
            self.zoom = max(self.min_zoom, self.zoom * (1 - self.zoom_speed))

    def world_to_screen(self, world_pos):
        """
        Converts world pixel coordinates to screen pixel coordinates.
        """
        screen_pos = (world_pos - self.offset) * self.zoom
        return screen_pos

    def get_visible_chunk_coords(self):
        """
        Calculates the range of chunk coordinates that are currently visible.
        """
        # Top-left corner of the camera's view in world coordinates
        start_world_pos = self.offset
        # Bottom-right corner
        end_world_pos = self.offset + pygame.math.Vector2(SCREEN_WIDTH / self.zoom, SCREEN_HEIGHT / self.zoom)

        # Convert world pixel coordinates to chunk coordinates
        start_chunk_x = floor(start_world_pos.x / CHUNK_SIZE_PIXELS)
        start_chunk_y = floor(start_world_pos.y / CHUNK_SIZE_PIXELS)
        
        end_chunk_x = floor(end_world_pos.x / CHUNK_SIZE_PIXELS)
        end_chunk_y = floor(end_world_pos.y / CHUNK_SIZE_PIXELS)

        # Return a range of chunks to load, with a small buffer
        return range(start_chunk_x - (LOAD_RADIUS_CHUNKS - 1), end_chunk_x + LOAD_RADIUS_CHUNKS), range(start_chunk_y - (LOAD_RADIUS_CHUNKS - 1), end_chunk_y + LOAD_RADIUS_CHUNKS)
