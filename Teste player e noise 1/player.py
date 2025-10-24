import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, position, group):
        super().__init__(group)

        self.image = pygame.Surface((tile_size_pixels, tile_size_pixels))
        self.image.fill('red')
        self.rect = self.image.get_rect(center = position)

        # Movement attributes
        self.direction = pygame.math.Vector2()
        self.position = pygame.math.Vector2(self.rect.center)
        self.speed = PLAYER_SPEED

    def input(self):
        keys = pygame.key.get_pressed()

        # Movement input
        if keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_a]:
            self.direction.x = -1
        elif keys[pygame.K_d]:
            self.direction.x = 1
        else:
            self.direction.x = 0

    def update(self, dt):
        self.input()

        # Update last_direction if the player is moving
        if self.direction.magnitude() > 0:
            self.last_direction = self.direction.copy()

        # Normalize movement direction
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        # Update position
        self.position += self.direction * self.speed * dt
        self.rect.center = round(self.position.x), round(self.position.y)

