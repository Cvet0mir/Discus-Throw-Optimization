import pygame
from physics.player_physics import create_space, create_player, create_ground, apply_input, step
from utils.sliders import Slider

pygame.init()

pygame.display.set_caption("Discus Throw Simulator")

WIDTH, HEIGHT = 1500, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))

background = pygame.image.load("visualization/assets/stadium.jpg")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))


def show_start_screen(screen):
    font_big = pygame.font.SysFont("Arial", 60)
    font_small = pygame.font.SysFont("Arial", 30)

    start_time = pygame.time.get_ticks()
    duration = 2500

    while pygame.time.get_ticks() - start_time < duration:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

        screen.fill((30, 30, 30))

        title = font_big.render("Discus Throwing Simulator", True, "white")
        subtitle = font_small.render("Loading...", True, "white")

        screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2 - 60))
        screen.blit(subtitle, (WIDTH//2 - subtitle.get_width()//2, HEIGHT//2 + 20))

        pygame.display.flip()

    return True


def render_game():
    font = pygame.font.SysFont("Arial", 20)

    panel_width = 320
    panel_height = 260
    panel_x = WIDTH - panel_width - 20
    panel_y = 20
    
    angle_slider = Slider(panel_x + 20, panel_y + 80, 260, 10, 80, 45, "θ (Angle)")
    velocity_slider = Slider(panel_x + 20, panel_y + 140, 260, 5, 50, 20, "v (Velocity)")
    height_slider = Slider(panel_x + 20, panel_y + 200, 260, 0, 100, 20, "h (Height)")

    clock = pygame.time.Clock()

    if not show_start_screen(screen):
        return

    running = True

    space = create_space()
    body = create_player(space)
    create_ground(space, WIDTH)

    while running:
        dt = clock.tick(60) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            angle_slider.handle_event(event)
            velocity_slider.handle_event(event)
            height_slider.handle_event(event)

        keys = pygame.key.get_pressed()
        apply_input(body, (keys[pygame.K_a], keys[pygame.K_d]))

        step(space, dt)

        screen.blit(background, (0, 0))
        draw_stickman(screen, body.position)

        panel = pygame.Surface((panel_width, panel_height))
        panel.set_alpha(140)
        panel.fill((0, 0, 0))
        screen.blit(panel, (panel_x, panel_y))

        title_font = pygame.font.SysFont("Arial", 32, bold=True)
        title = title_font.render("Parameters", True, (220, 50, 50))
        screen.blit(title, (panel_x + 80, panel_y + 15))

        angle_slider.draw(screen, font)
        velocity_slider.draw(screen, font)
        height_slider.draw(screen, font)

        pygame.display.flip()

    pygame.quit()


def draw_stickman(screen, pos):
    x, y = int(pos.x), int(pos.y)

    scale = 0.6
    head_radius = int(20 * scale)

    pygame.draw.circle(screen, "black", (x, y), head_radius)

    pygame.draw.line(screen, "black",
                     (x, y + int(20 * scale)),
                     (x, y + int(80 * scale)), 3)

    pygame.draw.line(screen, "black",
                     (x - int(30 * scale), y + int(50 * scale)),
                     (x + int(30 * scale), y + int(50 * scale)), 3)

    pygame.draw.line(screen, "black",
                     (x, y + int(80 * scale)),
                     (x - int(20 * scale), y + int(120 * scale)), 3)

    pygame.draw.line(screen, "black",
                     (x, y + int(80 * scale)),
                     (x + int(20 * scale), y + int(120 * scale)), 3)

