import math
import random
import pygame

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
        self.image_original = pygame.image.load("C:\\Users\\joaoc\\OneDrive\\Desktop\\teste_1\\Projeto_Final_Esperança\\nave.png").convert_alpha()
        self.image_original = pygame.transform.scale(self.image_original, (60, 60))  # ajuste de tamanho
        self.image = self.image_original # imagem que será desenhada
        self.rect = self.image_original.get_rect(center=(self.x, self.y)) 

    def update(self, keys, width, height):
        # Rotação
        if keys[pygame.K_LEFT]:
            self.angle -= 4
        if keys[pygame.K_RIGHT]:
            self.angle += 4

        # Aceleração
        if keys[pygame.K_UP]:
            self.vel_x += math.cos(math.radians(self.angle)) * self.acc
            self.vel_y += math.sin(math.radians(self.angle)) * self.acc

        # Atualiza posição
        self.x += self.vel_x
        self.y += self.vel_y

        # Atrito
        self.vel_x *= self.drag
        self.vel_y *= self.drag

        # Wrap-around (teleporta para o outro lado da tela)
        if self.x < 0: self.x = width
        if self.x > width: self.x = 0
        if self.y < 0: self.y = height
        if self.y > height: self.y = 0

    def draw(self, screen, keys=None):
        # 🔹 Rotaciona a imagem conforme o ângulo atual
        # (a imagem padrão aponta para cima, então compensamos com -90 graus se estiver lateral)
        rotated_image = pygame.transform.rotate(self.image_original, -self.angle - 90)
        rect = rotated_image.get_rect(center=(self.x, self.y))

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

        if self.x < 0: self.x = width
        if self.x > width: self.x = 0
        if self.y < 0: self.y = height
        if self.y > height: self.y = 0

    def draw(self, screen):
        pygame.draw.circle(screen, (255,255,255), (int(self.x), int(self.y)), self.size, 2)

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

        # Se sair da tela, desaparece (sem wrap, igual Asteroids original)
        if (self.x < 0 or self.x > width or
            self.y < 0 or self.y > height):
            self.lifetime = 0

    def draw(self, screen):
        pygame.draw.circle(screen, (255,255,255), (int(self.x), int(self.y)), 3)




