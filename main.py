import pygame
from settings import *
from classes import *

pygame.init()

surface = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
pygame.display.set_caption("Space Game")

clock = pygame.time.Clock()

start_screen = StartScreen(surface)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    start_screen.tick()

    pygame.display.update()
    clock.tick(FPS)