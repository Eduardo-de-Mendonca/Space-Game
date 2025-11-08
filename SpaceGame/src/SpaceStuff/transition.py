import pygame
import time

class TransitionScreen:
    def __init__(self, screen, message="Entrando na nave...", duration=2):
        self.screen = screen
        self.message = message
        self.duration = duration  # segundos
        self.font = pygame.font.SysFont("arial", 36)
        self.active = True
        self.start_time = time.time()

    def run(self):
        """Desenha a tela de transição por alguns segundos"""
        while self.active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            self.screen.fill((0, 0, 0))

            # Texto centralizado
            text = self.font.render(self.message, True, (255, 255, 255))
            rect = text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
            self.screen.blit(text, rect)

            pygame.display.flip()

            # Termina depois do tempo
            if time.time() - self.start_time > self.duration:
                self.active = False