import pygame
from planet import Planet
from player import Player
from settings import *

class Level: #Level é um cenário genérico, acho que é tipo o screen que o Edu usava
    def __init__(self, screen, destination_id):
        
        self.all_sprites = pygame.sprite.Group()

        self.screen = screen
        self.destination_id = destination_id
        #Diferenciar depois?
        self.planet = Planet(self.screen, self.destination_id, self.all_sprites)
        self.player = Player((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), self.all_sprites)

    def run(self, dt):
        self.screen.fill('black')

        self.planet.draw() #Desenho é da classe planeta. O planeta é gerado on demand e o level determina os parâmetros
        #Na realidade não tem condição de usar array de arrays para terreno. Tem que usar outro sistema
        
        self.all_sprites.update(dt)
        self.all_sprites.draw(self.screen)
    
    def cleanse(self):
        self.screen.fill('black')