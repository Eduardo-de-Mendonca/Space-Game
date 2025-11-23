import pygame

from src.Others.camera import Camera
from src.SaveDataStuff.item import Item

from src.PlanetSurfaceStuff.surface_settings import *

class DroppedItem:
    def __init__(self, item, center):
        assert isinstance(item, Item)
        assert isinstance(center, pygame.Vector2)

        self.item = item
        self.center = center

    def get_rect(self):
        w = DROPPED_ITEM_WIDTH
        h = DROPPED_ITEM_HEIGHT
        left = self.center[0] - w/2
        top = self.center[1] - h/2

        return pygame.Rect(left, top, w, h)

    def draw(self, screen, camera):
        assert isinstance(screen, pygame.Surface)
        assert isinstance(camera, Camera)

        w = DROPPED_ITEM_WIDTH
        h = DROPPED_ITEM_HEIGHT
        left = self.center[0] - w/2
        top = self.center[1] - h/2

        wpos = pygame.Vector2(left, top)
        spos = camera.world_to_screen(wpos)

        zoomed_width = (w * camera.zoom)
        zoomed_height = (h * camera.zoom)

        scaled_image = pygame.transform.scale(self.item.image, (zoomed_width, zoomed_height))

        screen.blit(scaled_image, spos)