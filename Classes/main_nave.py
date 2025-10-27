import pygame
from classes_nave import Player
from classes_nave import Bullet
from classes_nave import Asteroid
import random
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

player = Player(WIDTH//2, HEIGHT//2)
bullets = []
wave = 1
score = 0
lives = 3
font = pygame.font.SysFont("arial", 24)

def check_collision(obj1_x, obj1_y, obj2_x, obj2_y, dist):
    return math.dist((obj1_x, obj1_y), (obj2_x, obj2_y)) < dist

def draw_game_over(screen, score, font):
    big_font = pygame.font.SysFont("arial", 48)
    text_game_over = big_font.render("GAME OVER", True, (255, 255, 255))
    text_score = font.render(f"FINAL SCORE: {score}", True, (255, 255, 255))
    text_restart = font.render("Press R to Restart", True, (255, 255, 255))
    text_quit = font.render("Press ESC to Quit", True, (255, 255, 255))

    screen.blit(text_game_over, (WIDTH//2 - 140, HEIGHT//2 - 80))
    screen.blit(text_score, (WIDTH//2 - 90, HEIGHT//2 - 20))
    screen.blit(text_restart, (WIDTH//2 - 90, HEIGHT//2 + 20))
    screen.blit(text_quit, (WIDTH//2 - 90, HEIGHT//2 + 50))

def spawn_wave(wave):
    new_asteroids = []
    for _ in range(2 + wave):  # Wave 1 = 3 asteroides, Wave 2 = 4, etc
        new_asteroids.append(Asteroid(
            random.randint(0, WIDTH),
            random.randint(0, HEIGHT)
        ))
    return new_asteroids

asteroids = spawn_wave(wave)
running = True
game_over = False
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bx, by, ang = player.shoot()
            bullets.append(Bullet(bx, by, ang))

    keys = pygame.key.get_pressed()
    player.update(keys, WIDTH, HEIGHT)

    if game_over:
        screen.fill((0, 0, 0))
        draw_game_over(screen, score, font)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:  # restart
        # Resetar o jogo
            player.x = WIDTH // 2
            player.y = HEIGHT // 2
            player.vel_x = 0
            player.vel_y = 0
            bullets.clear()
            asteroids = [Asteroid(100, 100), Asteroid(600, 300), Asteroid(300, 500)]
            score = 0
            lives = 3
            game_over = False

        if keys[pygame.K_ESCAPE]:
            running = False

        pygame.display.flip()
        continue  # impede o resto do loop (não atualiza jogo)

    # Atualiza asteroides
    for a in asteroids:
        a.update(WIDTH, HEIGHT)

    # Atualiza bullets
    for b in bullets[:]:
        b.update(WIDTH, HEIGHT)
        if b.lifetime <= 0:
            bullets.remove(b)

    # Colisão: tiro × asteroide
    for a in asteroids[:]:
        for b in bullets[:]:
            if check_collision(a.x, a.y, b.x, b.y, a.size):
                bullets.remove(b)
                asteroids.remove(a)

            # Fragmentação
                fragments = a.split()
                asteroids.extend(fragments)
                if a.size > 20:
                    score += 20
                elif a.size > 10:
                    score += 50
                else:
                    score += 100
                break
    if len(asteroids) == 0 and not game_over:
        wave += 1
        asteroids = spawn_wave(wave)

    # Colisão: nave × asteroide (GAME OVER)
    for a in asteroids:
        if check_collision(a.x, a.y, player.x, player.y, a.size + 10):
            lives -= 1
            player.x = WIDTH // 2
            player.y = HEIGHT // 2
            player.vel_x = 0
            player.vel_y = 0

            if lives <= 0:
                game_over = True


    screen.fill((0, 0, 0))

    player.draw(screen)
    for b in bullets:
        b.draw(screen)
    for a in asteroids:
        a.draw(screen)

    hud_score = font.render(f"SCORE: {score}", True, (255,255,255))
    hud_lives = font.render(f"LIVES: {lives}", True,  (255,255 ,255))
    hud_wave = font.render(f"WAVE: {wave}", True, (255,255,255))
    screen.blit(hud_wave, (10, 70))
    screen.blit(hud_score, (10, 10))
    screen.blit(hud_lives, (10, 40))

    pygame.display.flip()

pygame.quit()
