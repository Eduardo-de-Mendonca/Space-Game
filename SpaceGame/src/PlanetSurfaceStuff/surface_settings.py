import pygame
from src.Config.settings import *

# Configurações que afetam apenas a superfície
HUD_MARGIN = (10, 40)
HUD_COLOR = pygame.Color(255, 255, 255)
HUD_ANTIALIASING = True

MAX_DAMAGE_COOLDOWN = 100

# Barra de vida
HP_BAR_OFFSET = 20
HP_BAR_HEIGHT = 20
HP_BAR_WIDTH = 100

HP_BAR_BG_COLOR = pygame.Color(255, 0, 0)
HP_BAR_FG_COLOR = pygame.Color(0, 255, 0)

# Inimigos e spawn
ENEMY_MIN_X_DIST = 250
ENEMY_MIN_Y_DIST = 150
ENEMY_MAX_X_DIST = 500
ENEMY_MAX_Y_DIST = 300

ENEMY_AMOUNT = 5