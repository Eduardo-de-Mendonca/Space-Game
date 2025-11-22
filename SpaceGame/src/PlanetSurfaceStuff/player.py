from src.Config.settings import *
from src.Others.input import InputFrame
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

        self.attack_cooldown = 0.0
        self.raio_ataque = 50 # Alcance da espada/soco
        self.dano_ataque = 1
        # Animação da Espada
        self.sword_image = pygame.image.load("src/Assets/espada.png").convert_alpha()
        self.sword_rect = self.sword_image.get_rect()
        self.attacking = False
        self.attack_duration = 0.5 # Duração total da animação em segundos
        self.attack_timer = 0.0
        self.attack_angle = 0.0

        # Redimensiona se a imagem for muito grande (Pixel art as vezes vem pequena ou enorme)
        # Ajuste (32, 32) para o tamanho que ficar bom no seu jogo
        self.sword_image = pygame.transform.scale(self.sword_image, (60, 60))
        
        self.sword_rect = self.sword_image.get_rect()

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
        hitbox = pygame.Rect(0, 0, self.raio_ataque * 2, self.raio_ataque * 2)
        hitbox.center = (int(center.x), int(center.y))
        return hitbox
    
    def draw_sword(self, screen, camera):
        """ Desenha a espada animada durante o ataque """
        if self.attacking:
            # Rotaciona a imagem da espada
            rotated_sword = pygame.transform.rotate(self.sword_image, self.attack_angle)
            
            # Posição da espada relativa ao jogador (no mundo)
            # Ajuste esses valores (20, 0) para posicionar a espada corretamente na mão
            sword_pos_world = self.position + Vector2(20, 0)
            
            # Calcula a posição na tela
            screen_pos = camera.world_to_screen(sword_pos_world)
            
            # Posiciona o rect rotacionado
            rotated_rect = rotated_sword.get_rect(center=(int(screen_pos.x), int(screen_pos.y)))
            
            # Desenha na tela
            screen.blit(rotated_sword, rotated_rect)

