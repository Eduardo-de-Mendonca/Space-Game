# Em: src/PlanetSurfaceStuff/enemy.py
import pygame
from pygame.math import Vector2
import random

from src.PlanetSurfaceStuff.surface_settings import *
from src.Others.camera import Camera

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, player_ref, max_hp):
        super().__init__() 
        self.player = player_ref 
        self.image = pygame.Surface((32, 32)) 
        self.image.fill((255, 0, 100)) # Rosa-choque
        self.position = Vector2(pos_x, pos_y) 
        self.rect = self.image.get_rect(center=self.position)
        self.velocidade = 90 
        self.raio_visao = 200 
        self.state = "PATRULHA"
        self.patrol_timer = 0.0 
        self.patrol_direction = Vector2(0, 0)

        self.max_hp = max_hp
        self.hp = self.max_hp

    def update(self, input, dt):
        distancia = self.position.distance_to(self.player.position)
        if distancia < self.raio_visao:
            self.state = "PERSEGUIÇÃO"
        else:
            self.state = "PATRULHA"

        if self.state == "PERSEGUIÇÃO":
            self.perseguir(dt)
        elif self.state == "PATRULHA":
            self.patrulhar(dt)
        
        self.rect.center = self.position

    def perseguir(self, dt):
        if self.player.position == self.position: return
        try:
            direcao = (self.player.position - self.position).normalize()
            self.position += direcao * self.velocidade * dt
        except ValueError:
            pass

    def patrulhar(self, dt):
        self.patrol_timer -= dt
        if self.patrol_timer <= 0:
            self.patrol_timer = random.uniform(2.0, 4.0) 
            self.patrol_direction = Vector2(random.uniform(-1, 1), 
                                            random.uniform(-1, 1))
            if self.patrol_direction.length() > 0:
                self.patrol_direction = self.patrol_direction.normalize()
        
        self.position += self.patrol_direction * (self.velocidade * 0.5) * dt

    def take_damage(self, quantidade):
        self.hp -= quantidade
        #print(f"Inimigo tomou {quantidade} de dano. Vida restante: {self.vida}")
        
        # Piscar de vermelho ou recuar (Opcional para o futuro)
        
        if self.hp <= 0:
            self.morrer()

    def morrer(self):
        print("Inimigo derrotado!")
        self.kill() # Remove o sprite de todos os grupos automaticamente

    def draw_hp_bar(self, screen, camera):
        '''
        Desenha a barra de vida acima do inimigo
        '''
        assert isinstance(screen, pygame.Surface)
        assert isinstance(camera, Camera)

        # Pegar as coordenadas do topleft
        x = self.rect.left
        y = self.rect.top

        # Converter para serem em relação à tela
        wpos = pygame.Vector2(x, y)
        spos = camera.world_to_screen(wpos)
        x = spos[0]
        y = spos[1]

        # Pegar o x do centro, considerando o zoom
        x += (self.rect.width/2)*camera.zoom

        # Offsetar para chegar ao topleft da barra de hp
        x -= HP_BAR_WIDTH//2
        y -= HP_BAR_OFFSET
        y -= HP_BAR_HEIGHT
        
        # Desenhar o retângulo vermelho
        r1 = pygame.rect.Rect(x, y, HP_BAR_WIDTH, HP_BAR_HEIGHT)
        pygame.draw.rect(screen, HP_BAR_BG_COLOR, r1)

        # Desenhar o retângulo verde por cima
        w = (self.hp/self.max_hp)*HP_BAR_WIDTH
        r2 = pygame.rect.Rect(x, y, w, HP_BAR_HEIGHT)
        pygame.draw.rect(screen, HP_BAR_FG_COLOR, r2)