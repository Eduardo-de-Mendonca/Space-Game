import math
import random
import pygame

from src.Others.camera import *
from src.Config.planet_templates import *

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0
        self.vel_x = 0
        self.vel_y = 0
        self.acc = 0.2
        self.drag = 0.99

        # 🔹 Carrega e ajusta a imagem da nave
        self.image_original = pygame.image.load("src/Assets/nave.png").convert_alpha()
        self.image_original = pygame.transform.scale(self.image_original, (60, 60))  # ajuste de tamanho
        self.image = self.image_original # imagem que será desenhada
        self.rect = self.image_original.get_rect(center=(self.x, self.y)) 

    def update(self, keys, width, height):
        # Rotação
        if keys[pygame.K_a]:
            self.angle -= 4
        if keys[pygame.K_d]:
            self.angle += 4

        # Aceleração
        if keys[pygame.K_w]:
            self.vel_x += math.cos(math.radians(self.angle)) * self.acc
            self.vel_y += math.sin(math.radians(self.angle)) * self.acc

        # Atualiza posição
        self.x += self.vel_x
        self.y += self.vel_y

        # Atrito
        self.vel_x *= self.drag
        self.vel_y *= self.drag

        # Wrap-around (teleporta para o outro lado da tela): removido, porque agora há câmera
        '''
        if self.x < 0: self.x = width
        if self.x > width: self.x = 0
        if self.y < 0: self.y = height
        if self.y > height: self.y = 0
        '''

    def draw(self, screen, camera, keys=None):
        assert isinstance(screen, pygame.Surface)
        assert isinstance(camera, CameraWithoutZoom)
        # 🔹 Rotaciona a imagem conforme o ângulo atual
        # (a imagem padrão aponta para cima, então compensamos com -90 graus se estiver lateral)
        rotated_image = pygame.transform.rotate(self.image_original, -self.angle - 90)

        world_pos = pygame.Vector2(self.x, self.y)
        x, y = camera.world_to_screen(world_pos)
        # Calcular a posição para desenhar
        rect = rotated_image.get_rect(center=(x, y))

        # 🔹 Desenha a nave
        screen.blit(rotated_image, rect.topleft)

        # 🔹 Efeito de propulsão (opcional)
        if keys and keys[pygame.K_UP]:
            fx = self.x - math.cos(math.radians(self.angle)) * 25
            fy = self.y - math.sin(math.radians(self.angle)) * 25
            pygame.draw.circle(screen, (255, 150, 0), (int(fx), int(fy)), 5)

    def shoot(self):
        angle_rad = math.radians(self.angle)
        bullet_x = self.x + math.cos(angle_rad) * 20
        bullet_y = self.y + math.sin(angle_rad) * 20
        return bullet_x, bullet_y, self.angle


    #def draw(self, screen):
        #angle_rad = math.radians(self.angle)
        #points = [
            #(self.x + math.cos(angle_rad) * 20, self.y + math.sin(angle_rad) * 20),
            #(self.x + math.cos(angle_rad + 2.5) * 20, self.y + math.sin(angle_rad + 2.5) * 20),
            #(self.x + math.cos(angle_rad - 2.5) * 20, self.y + math.sin(angle_rad - 2.5) * 20),
       # ]
       # pygame.draw.polygon(screen, (255,255,255), points)

class Asteroid:
    def __init__(self, x, y, size=40):
        self.x = x
        self.y = y
        self.size = size
        self.vel_x = random.uniform(-2, 2)
        self.vel_y = random.uniform(-2, 2)

    def update(self, width, height):
        self.x += self.vel_x
        self.y += self.vel_y

    def draw(self, screen, camera):
        assert isinstance(camera, CameraWithoutZoom)

        world_pos = pygame.Vector2(self.x, self.y)
        x, y = camera.world_to_screen(world_pos)

        pygame.draw.circle(screen, (255,255,255), (int(x), int(y)), self.size, 2)

    def split(self):
        """Retorna uma lista com fragmentos menores. Se muito pequeno, retorna lista vazia."""
        if self.size > 15:  # grande -> médio, médio -> pequeno
            new_size = self.size // 2
            return [
                Asteroid(self.x, self.y, new_size),
                Asteroid(self.x, self.y, new_size)
            ]
        else:
            return []  # pequeno desaparece

class Bullet:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = 8
        self.lifetime = 60  # frames (~1 segundo a 60 FPS)

    def update(self, width, height):
        self.x += math.cos(math.radians(self.angle)) * self.speed
        self.y += math.sin(math.radians(self.angle)) * self.speed
        self.lifetime -= 1

    def draw(self, screen, camera):
        assert isinstance(camera, CameraWithoutZoom)

        world_pos = pygame.Vector2(self.x, self.y)
        x, y = camera.world_to_screen(world_pos)

        pygame.draw.circle(screen, (255,255,255), (int(x), int(y)), 3)

class PlanetInSpace:
    '''
    Um objeto representa um planeta no espaço. Tem informações para desenhar e colidir no espaço, além de ter referência para o Planet que será carregado quando o jogador pousar nele
    '''
    def __init__(self, position, planet_data):
        assert isinstance(position, pygame.math.Vector2)
        
        self.position = position
        self.planet_data = planet_data
        
        self.color = colors.blue # Placeholder
        self.radius = PLANET_IN_SPACE_RADIUS

    def draw(self, screen, camera):
        '''
        Desenha o planeta na tela, considerando a posição da câmera.
        '''
        assert isinstance(screen, pygame.Surface)
        assert isinstance(camera, CameraWithoutZoom)

        screen_pos = camera.world_to_screen(self.position)
        pygame.draw.circle(screen, self.color, (round(screen_pos.x), round(screen_pos.y)), round(self.radius)) # Isso tá meio ruim... coloquei pensamento sobre isso em a_fazer.txt


