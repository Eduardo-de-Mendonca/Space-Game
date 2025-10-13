import pygame

class StartScreen:
    def __init__(self, surface):
        self.surface = surface # Uma referência para a "superfície" do pygame, onde faremos os desenhos

    def tick(self):
        # Toda tela tem um método tick, que é chamado todo frame em main.py

        assert isinstance(self.surface, pygame.Surface) # Para o highlighting de sintaxe funcionar direitinho nos métodos de self.surface. Esse "assert isinstance" é algo de que devemos usar e abusar ao longo do projeto, pois ele evita erros de execução e sugere boas práticas na hora de organizar o código

        # Exemplo: desenhar um círculo
        color1 = pygame.Color(200, 200, 200)
        color2 = pygame.Color(100, 100, 100)
        center = pygame.Vector2(100, 100)
        radius = 50

        self.surface.fill(color1)
        pygame.draw.circle(self.surface, color2, center, radius)