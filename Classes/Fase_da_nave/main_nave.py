import pygame
import math, random
from classes_nave import Player, Bullet, Asteroid

WIDTH, HEIGHT = 800, 600

class AsteroidsGame:
    def __init__(self, screen):
        self.screen = screen
        self.player = Player(WIDTH//2, HEIGHT//2)
        self.bullets = []
        self.wave = 1
        self.score = 0
        self.lives = 3
        self.font = pygame.font.SysFont("arial", 24)
        self.asteroids = self.spawn_wave(self.wave)
        self.game_over = False

    def spawn_wave(self, wave):
        new_asteroids = []
        for _ in range(2 + wave):
            new_asteroids.append(Asteroid(random.randint(0, WIDTH),
                                          random.randint(0, HEIGHT)))
        return new_asteroids

    def check_collision(self, obj1_x, obj1_y, obj2_x, obj2_y, dist):
        return math.dist((obj1_x, obj1_y), (obj2_x, obj2_y)) < dist

    def run(self):
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
