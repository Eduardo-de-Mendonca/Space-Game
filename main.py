from screens import *

pygame.init()

surface = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
pygame.display.set_caption("Space Game")

clock = pygame.time.Clock()

earth = Planet(
    colors.dark_blue,
    colors.blue,
    colors.light_yellow,
    colors.light_green,
    colors.dark_green,
    colors.gray,
    colors.white
)
start_screen = PlanetSurfaceScreen(surface, earth)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    start_screen.tick()

    pygame.display.update()
    clock.tick(FPS)