import pygame
import time
from src.Config.settings import DEFAULT_TRANSITION_SECONDS

class TransitionScreen:
    def __init__(self, screen, message, duration=DEFAULT_TRANSITION_SECONDS):
        assert isinstance(screen, pygame.Surface)

        self.screen = screen
        self.message = message
        self.duration = duration  # segundos
        self.font = pygame.font.SysFont("arial", 36)
        self.active = True
        self.start_time = time.time()

    def run(self):
        """Desenha a tela de transição."""
        self.screen.fill((0, 0, 0))

        # Texto centralizado
        text = self.font.render(self.message, True, (255, 255, 255))
        rect = text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.screen.blit(text, rect)

        # Termina depois do tempo
        if time.time() - self.start_time > self.duration:
            self.active = False