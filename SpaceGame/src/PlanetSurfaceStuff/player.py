from src.Config.settings import *
from src.Others.input import InputFrame
from src.Others.camera import Camera

from src.SaveDataStuff.item import Item

from pygame.math import Vector2
from math import floor, cos, pi
import random

class Player(pygame.sprite.Sprite):
    def __init__(self, position, group):
        """
        Position is now in WORLD PIXELS, not screen pixels.
        """
        super().__init__(group)
        self.image = pygame.Surface((TILE_SIZE*PLAYER_RELATIVE_SIZE, TILE_SIZE*PLAYER_RELATIVE_SIZE))
        self.image.fill('red')
        
        # Position is now a high-precision Vector2 for physics
        self.position = pygame.math.Vector2(position)
        # Rect is used for drawing and collisions
        self.rect = self.image.get_rect(center=self.position)
        
        self.direction = pygame.math.Vector2()
        self.speed = PLAYER_SPEED

        # Questões de ataque
        self.attack_cooldown = 0.0
        self.attack_radius = 50 # Alcance da espada/soco
        
        self.attack_duration = 0.5 # Duração total da animação em segundos
        self.attack_timer = 0.0
        self.attack_angle = 0.0

        self.attacking = False
        self.attacking_item_image = None
        self.attacking_item_rect = None

        # Vida
        self.lives = 3

    def react_to_input(self, input):
        assert isinstance(input, InputFrame)
        keys = input.pressing

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

    def update(self, input, dt):
        self.react_to_input(input)

        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()
        
        # Update the high-precision position
        self.position += self.direction * self.speed * dt
        
        # Update the integer rect's center to match
        self.rect.center = round(self.position.x), round(self.position.y)
        # Reduz o cooldown do ataque
        if self.attack_cooldown > 0:
            self.attack_cooldown -= dt
            
        # Animação de Ataque
        if self.attacking:
            self.attack_timer += dt
            if self.attack_timer > self.attack_duration:
                self.attacking = False
                self.attack_timer = 0.0
                self.attack_angle = 0.0
            else:
                # Calcula o ângulo de cima para baixo usando uma função cosseno
                # Começa em ~90, vai até ~-90
                progress = self.attack_timer / self.attack_duration
                self.attack_angle = 90 - (180 * progress)

    # NOVO: Método que cria a área do ataque
    def get_attack_hitbox(self):
        """ Retorna a área de ataque """
        center = self.position
        hitbox = pygame.Rect(0, 0, self.attack_radius * 2, self.attack_radius * 2)
        hitbox.center = (int(center.x), int(center.y))
        return hitbox
    
    def draw_attacking_item(self, screen, camera):
        """ Desenha o item animado durante o ataque. Se não estiver atacando, não faz nada."""
        assert isinstance(screen, pygame.Surface)
        assert isinstance(camera, Camera)

        if self.attacking:
            # Rotaciona a imagem da espada
            rotated_sword = pygame.transform.rotate(self.attacking_item_image, self.attack_angle)
            
            # Posição da espada relativa ao jogador (no mundo)
            # Ajuste esses valores (20, 0) para posicionar a espada corretamente na mão
            sword_pos_world = self.position + Vector2(20, 0)
            
            # Calcula a posição na tela
            screen_pos = camera.world_to_screen(sword_pos_world)
            
            # Posiciona o rect rotacionado
            rotated_rect = rotated_sword.get_rect(center=(int(screen_pos.x), int(screen_pos.y)))
            
            # Desenha na tela
            screen.blit(rotated_sword, rotated_rect)

