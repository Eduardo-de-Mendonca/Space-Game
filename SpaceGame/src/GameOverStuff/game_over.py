import pygame

from src.Config.settings import SCREEN_HEIGHT, SCREEN_WIDTH
from src.Others.input import InputHandler

class game_over_states:
    'O state será lido pela tela-pai para determinar o que fazer quando deixarmos de estar running'
    RUNNING = 0
    RESTART = 1
    QUIT = 2

class GameOverScreen:
    'Representa a tela quando sofremos GameOver. Essa tela, quando existir, sempre será subtela da tela principal (no momento, será diretamente o level do Game, pois não há menu principal)'

    def __init__(self, screen, input_handler):
        assert isinstance(screen, pygame.Surface)
        assert isinstance(input_handler, InputHandler)
        self.screen = screen
        self.input_handler = input_handler
        self.font = pygame.font.SysFont("arial", 24)
        self.big_font = pygame.font.SysFont("arial", 48)

        self.state = game_over_states.RUNNING

    def run(self, dt):
        # Ler o input
        input = self.input_handler.get_input()
        if input.just_pressed[pygame.K_r]:
            self.state = game_over_states.RESTART
        if input.just_pressed[pygame.K_ESCAPE]:
            self.state = game_over_states.QUIT

        # Desenhar tudo
        self.screen.fill((0,0,0))
        big_font = self.big_font

        text_game_over = big_font.render("GAME OVER", True, (255,255,255))
        text_hint = self.font.render("Pressione R para reiniciar ou ESC para fechar o jogo", True, (200,200,200))

        self.screen.blit(text_game_over, (SCREEN_WIDTH//2-140, SCREEN_HEIGHT//2-80))
        self.screen.blit(text_hint, (SCREEN_WIDTH//2-180, SCREEN_HEIGHT//2+40))