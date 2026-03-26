
import pygame
pygame.init()

background = pygame.image.load("visualization/assets/stadium.jpg")
background = pygame.transform.scale(background, (1390, 745))

def render_game():
    screen = pygame.display.set_mode((1390, 745))
    clock = pygame.time.Clock()
    running = True
    dt = 0

    player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        background = pygame.image.load("visualization/assets/stadium.jpg")
        background = pygame.transform.scale(background, (1390, 745))

        screen.blit(background, (0, 0))

        draw_stickman(screen, player_pos)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player_pos.y -= 300 * dt
        if keys[pygame.K_s]:
            player_pos.y += 300 * dt
        if keys[pygame.K_a]:
            player_pos.x -= 300 * dt
        if keys[pygame.K_d]:
            player_pos.x += 300 * dt

        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(60) / 1000

    pygame.quit()


def draw_stickman(screen, pos):
    x, y = pos
    # head
    pygame.draw.circle(screen, "black", (x, y), 10)
    # body
    pygame.draw.line(screen, "black", (x, y+10), (x, y+40), 2)
    # arms
    pygame.draw.line(screen, "black", (x-15, y+25), (x+15, y+25), 2)
    # legs
    pygame.draw.line(screen, "black", (x, y+40), (x-10, y+60), 2)
    pygame.draw.line(screen, "black", (x, y+40), (x+10, y+60), 2)
