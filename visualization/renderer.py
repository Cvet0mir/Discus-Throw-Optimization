import pygame

from physics.player_physics import create_space, create_player, create_ground, apply_input, step
from utils.sliders import Slider
from .slider_panel import draw_slider_panel
from .formula_panel import draw_formula_panel

pygame.init()

pygame.display.set_caption("Discus Throw Simulator")

WIDTH, HEIGHT = 1500, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))

background = pygame.image.load("visualization/assets/stadium.jpg")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

UI_FONT = pygame.font.SysFont("Arial", 20)
TITLE_FONT = pygame.font.SysFont("Arial", 28, bold=True)


def show_start_screen(screen):
    font_big = TITLE_FONT
    font_small = UI_FONT

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
    panel_width = 320
    panel_height = 260
    panel_x = WIDTH - panel_width - 20
    panel_y = 20

    angle_slider = Slider(panel_x + 20, panel_y + 80, 260, 10, 80, 45, "θ (Angle)", "°")
    velocity_slider = Slider(panel_x + 20, panel_y + 140, 260, 5, 50, 20, "v (Velocity)", " m/s")
    height_slider = Slider(panel_x + 20, panel_y + 200, 260, 10, 250, 50, "h (Height)", " cm")

    formula_x = 20
    formula_y = 20
    formula_width = 420
    formula_height = 130

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

        draw_slider_panel(
            screen,
            panel_x, panel_y,
            panel_width, panel_height,
            "Parameters",
            [angle_slider, velocity_slider, height_slider],
            UI_FONT,
            TITLE_FONT
        )

        draw_formula_panel(
            screen,
            formula_x, formula_y,
            formula_width, formula_height,
            angle_slider.value,
            velocity_slider.value,
            height_slider.value,
            UI_FONT,
            TITLE_FONT
        )

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

