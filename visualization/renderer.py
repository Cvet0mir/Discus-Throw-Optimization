import pygame
from physics.player_physics import create_space, create_player, create_ground, apply_input, step

pygame.init()

WIDTH, HEIGHT = 1390, 745

background = pygame.image.load("visualization/assets/stadium.jpg")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))


def render_game():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    running = True

    space = create_space()
    body = create_player(space)
    create_ground(space, WIDTH)

    while running:
        dt = clock.tick(60) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        apply_input(body, (keys[pygame.K_a], keys[pygame.K_d]))

        step(space, dt)

        screen.blit(background, (0, 0))
        draw_stickman(screen, body.position)

        pygame.display.flip()

    pygame.quit()


def draw_stickman(screen, pos):
    x, y = int(pos.x), int(pos.y)

    pygame.draw.circle(screen, "black", (x, y), 20)
    pygame.draw.line(screen, "black", (x, y+20), (x, y+80), 4)
    pygame.draw.line(screen, "black", (x-30, y+50), (x+30, y+50), 4)
    pygame.draw.line(screen, "black", (x, y+80), (x-20, y+120), 4)
    pygame.draw.line(screen, "black", (x, y+80), (x+20, y+120), 4)


