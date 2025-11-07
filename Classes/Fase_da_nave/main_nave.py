import pygame
import math, random
from Classes.Fase_da_nave.classes_nave import *
from Classes.Others.camera import *
from Classes.Others.save_data import *
from Classes.PlanetSurfaceStuff.level import Level
from settings import *

class AsteroidsGame:
    def __init__(self, screen, save_data):
        assert isinstance(screen, pygame.Surface)
        assert isinstance(save_data, SaveData)

        self.screen = screen
        self.player = Player(ASTEROID_GAME_WIDTH//2, ASTEROID_GAME_HEIGHT//2)
        self.camera = CameraWithoutZoom()
        self.bullets = []
        self.wave = 1
        self.score = 0
        self.lives = 3
        self.font = pygame.font.SysFont("arial", 24)
        self.asteroids = self.spawn_wave(self.wave)
        self.game_over = False

        self.save_data = save_data
        self.planets = [PlanetInSpace(pygame.math.Vector2(500, 300), save_data.all_planets[0])]

        self.sublevel = None

    def spawn_wave(self, wave):
        new_asteroids = []
        for _ in range(2 + wave):
            # Spawna em torno do jogador, e não a partir da coordenada 0, agora que há câmera
            cpos = self.camera.get_offset()
            cx = int(cpos[0])
            cy = int(cpos[1])
            w = ASTEROID_GAME_WIDTH
            h = ASTEROID_GAME_HEIGHT

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
            b.update(ASTEROID_GAME_WIDTH, ASTEROID_GAME_HEIGHT)

            if b.lifetime <= 0:
                self.bullets.remove(b)
        
        # Atualiza asteroides
        for a in self.asteroids:
            assert isinstance(a, Asteroid)
            a.update(ASTEROID_GAME_WIDTH, ASTEROID_GAME_HEIGHT)

            cpos = self.camera.get_offset()
            cx = cpos[0]
            cy = cpos[1]
            w = ASTEROID_GAME_WIDTH
            h = ASTEROID_GAME_HEIGHT

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
                    if a.size > 20: self.score += 20
                    elif a.size > 10: self.score += 50
                    else: self.score += 100
                    break

        if len(self.asteroids) == 0:
            self.wave += 1
            self.asteroids = self.spawn_wave(self.wave)

    def run(self, dt):
        if self.sublevel != None:
            # Aqui está a mágica da lógica de subtelas! Se minha subtela não é None, eu apenas rodo ela
            assert isinstance(self.sublevel, Level)
            if not(self.sublevel.running):
                self.sublevel = None
                self.player.x = 0
                self.player.y = 0
            else:
                self.sublevel.run(dt)
                return
        
        'Roda apenas um frame da tela. Não há loop infinito aqui: o loop infinito está em Game.'
        keys = pygame.key.get_pressed()

        # Movimenta o jogador
        self.player.update(keys, ASTEROID_GAME_WIDTH, ASTEROID_GAME_HEIGHT)

        # Dá tiro
        if keys[pygame.K_SPACE]:
            bx, by, ang = self.player.shoot()
            self.bullets.append(Bullet(bx, by, ang))

        # Atualiza a câmera
        self.camera.update(pygame.Vector2(self.player.x, self.player.y))
        
        # Atualiza as balas e asteroides
        self.update_bullets_asteroids()

        # Colisão jogador × asteroides
        for a in self.asteroids:
            assert isinstance(a, Asteroid)
            if self.check_collision(a.x, a.y, self.player.x, self.player.y, a.size+10):
                self.lives -= 1
                self.player.x = ASTEROID_GAME_WIDTH//2
                self.player.y = ASTEROID_GAME_HEIGHT//2
                self.player.vel_x = 0
                self.player.vel_y = 0
                if self.lives <= 0:
                    self.game_over = True

        # Colisão jogador x planetas
        collided_planet_index = self.check_planet_collisions()
        if collided_planet_index != None:
            destination_id = 0

            self.sublevel = Level(self.screen, self.save_data, self.save_data.all_planets[destination_id])

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

        hud_score = self.font.render(f"SCORE: {self.score}", True, (255,255,255))
        hud_lives = self.font.render(f"LIVES: {self.lives}", True, (255,255,255))
        hud_wave = self.font.render(f"WAVE: {self.wave}", True, (255,255,255))
        self.screen.blit(hud_wave, (10,70))
        self.screen.blit(hud_score, (10,10))
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