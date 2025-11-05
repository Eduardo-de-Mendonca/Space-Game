from settings import *
from planet_templates import colors
from Classes.Others.camera import Camera

class PlanetInSpace:
    '''
    Um objeto representa um planeta no espaço. Tem informações para desenhar e colidir no espaço, além de ter referência para o Planet que será carregado quando o jogador pousar nele
    '''
    def __init__(self, position, planet_data):
        assert isinstance(position, pygame.math.Vector2)
        
        self.position = position
        self.planet_data = planet_data
        
        self.color = colors.blue # Placeholder
        self.radius = PLANET_IN_SPACE_RADIUS

    def draw(self, screen, camera):
        '''
        Desenha o planeta na tela, considerando a posição da câmera.
        '''
        assert isinstance(screen, pygame.Surface)
        assert isinstance(camera, Camera)

        screen_pos = camera.world_to_screen(self.position)
        pygame.draw.circle(screen, self.color, (round(screen_pos.x), round(screen_pos.y)), round(self.radius * camera.zoom)) # Isso tá meio ruim... coloquei pensamento sobre isso em a_fazer.txt

class SpaceShip:
    '''
    Um objeto SpaceShip representa a nave espacial do jogador. Tem muito código repetido de Player. Eu poderia herdar de Player, mas com certeza Player vai mudar para ter coisas de combate, etc., qua não vão funcionar igualmente no espaço.
    '''
    def __init__(self):
        self.position = pygame.math.Vector2(0, 0)
        self.speed = SPACESHIP_SPEED
    
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill('red')

    def input(self):
        '''
        Lê o input e retorna a direção do movimento como um vetor normalizado.
        '''
        keys = pygame.key.get_pressed()
        direction = pygame.math.Vector2()

        # Movement input
        if keys[pygame.K_w]:
            direction.y = -1
        elif keys[pygame.K_s]:
            direction.y = 1
        else:
            direction.y = 0

        if keys[pygame.K_a]:
            direction.x = -1
        elif keys[pygame.K_d]:
            direction.x = 1
        else:
            direction.x = 0

        if direction.magnitude() > 0:
            direction = direction.normalize()

        return direction

    def update(self, dt):
        direction = self.input()
        
        # Update the high-precision position
        self.position += direction * self.speed * dt

    def draw(self, screen, camera):
        '''
        Desenha a nave na tela, considerando a posição da câmera.
        '''
        assert isinstance(screen, pygame.Surface)
        assert isinstance(camera, Camera)

        screen_pos = camera.world_to_screen(self.position)
        rect = self.image.get_rect(center=(round(screen_pos.x), round(screen_pos.y)))
        screen.blit(self.image, rect)