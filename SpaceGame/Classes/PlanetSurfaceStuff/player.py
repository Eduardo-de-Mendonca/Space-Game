from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, position, group):
        """
        Position is now in WORLD PIXELS, not screen pixels.
        """
        super().__init__(group)
        self.image = pygame.Surface((TILE_SIZE*0.7, TILE_SIZE*0.7))
        self.image.fill('red')
        
        # Position is now a high-precision Vector2 for physics
        self.position = pygame.math.Vector2(position)
        # Rect is used for drawing and collisions
        self.rect = self.image.get_rect(center=self.position)
        
        self.direction = pygame.math.Vector2()
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

        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()
        
        # Update the high-precision position
        self.position += self.direction * self.speed * dt
        
        # Update the integer rect's center to match
        self.rect.center = round(self.position.x), round(self.position.y)

