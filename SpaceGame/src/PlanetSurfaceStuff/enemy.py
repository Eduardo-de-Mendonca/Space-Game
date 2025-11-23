# Em: src/PlanetSurfaceStuff/enemy.py
import pygame
from pygame.math import Vector2
import random

class Enemy(pygame.sprite.Sprite):
    
    def __init__(self, pos_x, pos_y, player_ref):
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
        self.vida_maxima = 3
        self.vida = self.vida_maxima

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
        self.vida -= quantidade
        #print(f"Inimigo tomou {quantidade} de dano. Vida restante: {self.vida}")
        
        # Piscar de vermelho ou recuar (Opcional para o futuro)
        
        if self.vida <= 0:
            self.morrer()

    def morrer(self):
        print("Inimigo derrotado!")
        self.kill() # Remove o sprite de todos os grupos automaticamente