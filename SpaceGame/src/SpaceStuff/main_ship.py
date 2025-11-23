import pygame
import math, random

from src.SpaceStuff.classes_ship import *
from src.Others.camera import CameraWithoutZoom
from src.Others.input import InputHandler
from src.SaveDataStuff.save_data import SaveData
from src.PlanetSurfaceStuff.level import Level
from src.Config.settings import *
from src.TransitionStuff.transition import TransitionScreen

class AsteroidsGame:
    def __init__(self, screen, input_handler, save_data):
        assert isinstance(screen, pygame.Surface)
        assert isinstance(input_handler, InputHandler)
        assert isinstance(save_data, SaveData)

        self.screen = screen
        self.player = Player(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
        self.camera = CameraWithoutZoom()
        self.bullets = []
        self.lives = 3
        self.font = pygame.font.SysFont("arial", 24)
        self.margem = 150
        self.asteroids = self.spawn_wave()
        self.state = asteroids_game_states.RUNNING

        self.input_handler = input_handler
        self.save_data = save_data
        self.planets = save_data.all_planets

        self.sublevel = None
        self.transitionee = None # Relevante quando sublevel é uma tela de transição. Determina para qual tela transicionaremos quando a transição acabar

    def spawn_wave(self):
        new_asteroids = []
        cpos = self.camera.get_offset()
        cx = cpos.x  
        cy = cpos.y  
        w = SCREEN_WIDTH
        h = SCREEN_HEIGHT

        # 2. Definir os limites do SPawn no Mundo com Margem
        # Estes são os limites MÍNIMOS e MÁXIMOS onde o asteroide PODE aparecer.
        min_spawn_x = cx - self.margem
        max_spawn_x = cx + w + self.margem
        min_spawn_y = cy - self.margem
        max_spawn_y = cy + h + self.margem
    
        for _ in range(ASTEROIDS_SPAWNED_PER_WAVE):
            # 3. Escolher o lado do spawn: Topo, Fundo, Esquerda ou Direita
            side = random.choice(['top', 'bottom', 'left', 'right'])
        
            if side == 'top':
                # Spawn no topo (fora da tela, mas na largura da área visível + margem)
                x = random.uniform(min_spawn_x, max_spawn_x)
                y = random.uniform(min_spawn_y, cy) # Coordenada Y entre a margem superior e o limite superior da tela
            elif side == 'bottom':
                # Spawn no fundo
                x = random.uniform(min_spawn_x, max_spawn_x)
                y = random.uniform(cy + h, max_spawn_y) # Coordenada Y entre o limite inferior da tela e a margem inferior
            elif side == 'left':
                # Spawn à esquerda
                x = random.uniform(min_spawn_x, cx) # Coordenada X entre a margem esquerda e o limite esquerdo da tela
                y = random.uniform(cy, cy + h) # Coordenada Y dentro da altura da tela (sem margem no Y)
            elif side == 'right':
                # Spawn à direita
                x = random.uniform(cx + w, max_spawn_x) # Coordenada X entre o limite direito da tela e a margem direita
                y = random.uniform(cy, cy + h) # Coordenada Y dentro da altura da tela (sem margem no Y)
            
        
            new_asteroids.append(Asteroid(x, y))
        
        return new_asteroids

    def check_collision(self, obj1_x, obj1_y, obj2_x, obj2_y, dist):
        return math.dist((obj1_x, obj1_y), (obj2_x, obj2_y)) < dist

    def check_planet_collisions(self):
        '''
        Checa colisões entre a nave espacial e planetas. Se houver colisão, retorna o índice do planeta com o qual colidimos. Fora isso, retorna None.
        '''
        for i in range(len(self.planets)):
            planet = self.planets[i]

            obj1_x = self.player.x
            obj1_y = self.player.y
            obj2_x = planet.position[0]
            obj2_y = planet.position[1]
            dist = planet.radius

            collided = self.check_collision(obj1_x, obj1_y, obj2_x, obj2_y, dist)
            
            if collided:
                return i

        return None
    
    def update_bullets_asteroids(self):
        'A ser chamado 1 vez por frame. Atualiza as balas e os asteroides.'
        # Atualiza bullets
        for b in self.bullets[:]:
            assert isinstance(b, Bullet)
            b.update(SCREEN_WIDTH, SCREEN_HEIGHT)

            if b.lifetime <= 0:
                self.bullets.remove(b)
        
        # Atualiza asteroides
        for a in self.asteroids:
            assert isinstance(a, Asteroid)
            a.update(SCREEN_WIDTH, SCREEN_HEIGHT)

            cpos = self.camera.get_offset()
            cx = cpos[0]
            cy = cpos[1]
            w = SCREEN_WIDTH
            h = SCREEN_HEIGHT

            if a.x < cx - a.size or cx + w + a.size < a.x:
                self.asteroids.remove(a)
            elif a.y < cy - a.size or cy + h+ a.size < a.y:
                self.asteroids.remove(a)

        # Colisões e fragmentação
        for a in self.asteroids[:]:
            assert isinstance(a, Asteroid)
            for b in self.bullets[:]:
                assert isinstance(b, Bullet)
                if self.check_collision(a.x, a.y, b.x, b.y, a.size):
                    self.bullets.remove(b)
                    self.asteroids.remove(a)
                    fragments = a.split()
                    self.asteroids.extend(fragments)
                    break

        if len(self.asteroids) == 0:
            self.asteroids = self.spawn_wave()

    def check_all_collisons(self):
        # Colisão jogador × asteroides
        for a in self.asteroids:
            assert isinstance(a, Asteroid)
            if self.check_collision(a.x, a.y, self.player.x, self.player.y, a.size+10) and self.player.asteroid_iframes == 0:
                self.lives -= 1

                # Em vez de resetar a posição do jogador, vamos dar frames de invulnerabilidade
                self.player.asteroid_iframes = MAX_ASTEROID_IFRAMES

                if self.lives <= 0:
                    self.state = asteroids_game_states.GAME_OVER

        # Colisão jogador x planetas
        collided_planet_index = self.check_planet_collisions()
        if collided_planet_index != None and self.player.planet_iframes == 0:
            destination_id = 0
            self.player.planet_iframes = MAX_PLANET_IFRAMES

            self.transitionee = Level(self.screen, self.input_handler, self.save_data, self.save_data.all_planets[destination_id].planet_data)
            self.sublevel = TransitionScreen(self.screen, 'Pousando no planeta...')

    def run(self, dt):
        if self.sublevel != None:
            # Aqui está o ponto-chave da lógica de subtelas! Se minha subtela não é None, eu apenas rodo ela
            if isinstance(self.sublevel, TransitionScreen):
                if not(self.sublevel.active):
                    self.sublevel = self.transitionee
                    return # Retorno direto para não desenhar esta tela
                else:
                    self.sublevel.run()
                    return
                
            elif isinstance(self.sublevel, Level):
                if not(self.sublevel.running):
                    self.sublevel = None
                    self.lives = 3 # Regenera ao voltar de um planeta
                else:
                    self.sublevel.run(dt)
                    return
        
        'Roda apenas um frame da tela. Não há loop infinito aqui: o loop infinito está em Game.'
        input = self.input_handler.get_input()
        keys = input.pressing

        # Movimenta o jogador
        self.player.update(keys)

        # Dá tiro - era espaço, agora é clique
        if input.mouse_justpressed[0]:
            bx, by, ang = self.player.shoot()
            self.bullets.append(Bullet(bx, by, ang))

        # Atualiza a câmera
        self.camera.update(pygame.Vector2(self.player.x, self.player.y))
        
        # Atualiza as balas e asteroides
        self.update_bullets_asteroids()

        self.check_all_collisons()

        # Desenho
        self.screen.fill((0,0,0))
        self.player.draw(self.screen, self.camera)
        for b in self.bullets:
            assert isinstance(b, Bullet)
            b.draw(self.screen, self.camera)
        for a in self.asteroids:
            assert isinstance(a, Asteroid)
            a.draw(self.screen, self.camera)
        
        for p in self.planets:
            p.draw(self.screen, self.camera)

        hud_lives = self.font.render(f"VIDAS: {self.lives}", True, (255,255,255))
        self.screen.blit(hud_lives, (10,40))
