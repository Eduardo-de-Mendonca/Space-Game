import pygame
import math, random

from src.SpaceStuff.classes_ship import *
from src.Others.camera import CameraWithoutZoom
from src.Others.input import InputHandler
from src.Config.save_data import SaveData
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
        self.asteroids = self.spawn_wave()
        self.state = asteroids_game_states.RUNNING

        self.input_handler = input_handler
        self.save_data = save_data
        self.planets = [PlanetInSpace(pygame.math.Vector2(500, 300), save_data.all_planets[0])]

        self.sublevel = None
        self.transitionee = None # Relevante quando sublevel é uma tela de transição. Determina para qual tela transicionaremos quando a transição acabar

    def spawn_wave(self):
        new_asteroids = []
        for _ in range(ASTEROIDS_SPAWNED_PER_WAVE):
            # Spawna em torno do jogador, e não a partir da coordenada 0, agora que há câmera
            cpos = self.camera.get_offset()
            cx = int(cpos[0])
            cy = int(cpos[1])
            w = SCREEN_WIDTH
            h = SCREEN_HEIGHT

            x = random.randint(cx, cx + w)
            y = random.randint(cy, cy + h)

            new_asteroids.append(Asteroid(x,
            y))
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

            self.transitionee = Level(self.screen, self.input_handler, self.save_data, self.save_data.all_planets[destination_id])
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
                else:
                    self.sublevel.run(dt)
                    return
        
        'Roda apenas um frame da tela. Não há loop infinito aqui: o loop infinito está em Game.'
        input = self.input_handler.get_input()
        keys = input.pressing

        # Movimenta o jogador
        self.player.update(keys)

        # Dá tiro
        if input.just_pressed[pygame.K_SPACE]:
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
        
    '''
    def old_run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            dt = clock.tick(60) / 1000
            keys = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        bx, by, ang = self.player.shoot()
                        self.bullets.append(Bullet(bx, by, ang))
                    elif event.key == pygame.K_ESCAPE:
                        running = False  # sai do minigame

            self.player.update(keys, WIDTH, HEIGHT)
            if self.game_over:
                waiting = True
                while waiting:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            exit()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_r:
                                self.__init__(self.screen)  # reinicia
                                waiting = False
                            elif event.key == pygame.K_ESCAPE:
                                waiting = False  # volta para o planeta

                    self.screen.fill((0,0,0))
                    big_font = pygame.font.SysFont("arial", 48)
                    text_game_over = big_font.render("GAME OVER", True, (255,255,255))
                    text_score = self.font.render(f"FINAL SCORE: {self.score}", True, (255,255,255))
                    text_hint = self.font.render("Pressione R para reiniciar ou ESC para voltar ao planeta", True, (200,200,200))
                    self.screen.blit(text_game_over, (WIDTH//2-140, HEIGHT//2-80))
                    self.screen.blit(text_score, (WIDTH//2-90, HEIGHT//2-20))
                    self.screen.blit(text_hint, (WIDTH//2-180, HEIGHT//2+40))
                    pygame.display.flip()
                    pygame.time.Clock().tick(30)

                if not self.game_over:
                    continue  # volta pro jogo
                else:
                    running = False  # encerra o minigame
                    continue

        # Atualiza asteroides
            for a in self.asteroids:
                a.update(WIDTH, HEIGHT)

        # Atualiza bullets
            for b in self.bullets[:]:
                b.update(WIDTH, HEIGHT)
                if b.lifetime <= 0:
                    self.bullets.remove(b)

        # Colisões e fragmentação
            for a in self.asteroids[:]:
                for b in self.bullets[:]:
                    if self.check_collision(a.x, a.y, b.x, b.y, a.size):
                        self.bullets.remove(b)
                        self.asteroids.remove(a)
                        fragments = a.split()
                        self.asteroids.extend(fragments)
                        if a.size > 20: self.score += 20
                        elif a.size > 10: self.score += 50
                        else: self.score += 100
                        break

            if len(self.asteroids) == 0:
                self.wave += 1
                self.asteroids = self.spawn_wave(self.wave)

        # Colisão jogador × asteroides
            for a in self.asteroids:
                if self.check_collision(a.x, a.y, self.player.x, self.player.y, a.size+10):
                    self.lives -= 1
                    self.player.x = WIDTH//2
                    self.player.y = HEIGHT//2
                    self.player.vel_x = 0
                    self.player.vel_y = 0
                    if self.lives <= 0:
                        self.game_over = True

        # Desenho
            self.screen.fill((0,0,0))
            self.player.draw(self.screen)
            for b in self.bullets:
                b.draw(self.screen)
            for a in self.asteroids:
                a.draw(self.screen)
            hud_score = self.font.render(f"SCORE: {self.score}", True, (255,255,255))
            hud_lives = self.font.render(f"LIVES: {self.lives}", True, (255,255,255))
            hud_wave = self.font.render(f"WAVE: {self.wave}", True, (255,255,255))
            self.screen.blit(hud_wave, (10,70))
            self.screen.blit(hud_score, (10,10))
            self.screen.blit(hud_lives, (10,40))

            pygame.display.flip()

        return "exit"
    '''