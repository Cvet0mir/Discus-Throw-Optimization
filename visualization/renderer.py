import pygame

from physics.player_physics import create_space, create_player, create_ground, apply_input, step
from physics.throw import apply_throw
from physics.trajectory import compute_trajectory

from utils.sliders import Slider
from .ui.slider_panel import draw_slider_panel
from .ui.formula_panel import draw_formula_panel

pygame.init()

pygame.display.set_caption("Discus Throw Simulator")

WIDTH, HEIGHT = 1500, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))

background = pygame.image.load("visualization/assets/stadium.jpg")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

UI_FONT = pygame.font.SysFont("Arial", 20)
TITLE_FONT = pygame.font.SysFont("Arial", 28, bold=True)


def show_start_screen(screen):
    start_time = pygame.time.get_ticks()
    duration = 2500

    while pygame.time.get_ticks() - start_time < duration:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

        screen.fill((30, 30, 30))

        title = TITLE_FONT.render("Discus Throwing Simulator", True, "white")
        subtitle = UI_FONT.render("Loading...", True, "white")

        screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2 - 60))
        screen.blit(subtitle, (WIDTH//2 - subtitle.get_width()//2, HEIGHT//2 + 20))

        pygame.display.flip()

    return True


def render_game():
    panel_width = 320
    panel_height = 260
    panel_x = WIDTH - panel_width - 20
    panel_y = 20

    GROUND_Y = 600

    PIXELS_PER_METER = 17.5

    angle_slider = Slider(panel_x + 20, panel_y + 80, 260, 10, 80, 45, "θ (Angle)", "°")
    velocity_slider = Slider(panel_x + 20, panel_y + 140, 260, 8, 32, 18, "v (Velocity)", " m/s")
    height_slider = Slider(panel_x + 20, panel_y + 200, 260, 120, 220, 180, "h (Height)", " cm")

    clock = pygame.time.Clock()

    if not show_start_screen(screen):
        return

    running = True

    space = create_space()
    body = create_player(space)
    create_ground(space, WIDTH)

    trajectory_points = []
    landing_point = None

    while running:
        dt = clock.tick(60) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            angle_slider.handle_event(event)
            velocity_slider.handle_event(event)
            height_slider.handle_event(event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:

                    hand_pos = draw_stickman(
                        screen,
                        body.position,
                        height_slider.value
                    )

                    apply_throw(
                        body,
                        angle_slider.value,
                        velocity_slider.value,
                        hand_pos
                    )

                    trajectory_points, landing_point = compute_trajectory(
                        hand_pos[0],
                        hand_pos[1],
                        angle_slider.value,
                        velocity_slider.value,
                        PIXELS_PER_METER
                    )

        keys = pygame.key.get_pressed()
        apply_input(body, (keys[pygame.K_a], keys[pygame.K_d]))

        step(space, dt)

        screen.blit(background, (0, 0))

        hand_pos = draw_stickman(
            screen,
            body.position,
            height_slider.value
        )

        trajectory_points, landing_point = compute_trajectory(
            hand_pos[0],
            hand_pos[1],
            angle_slider.value,
            velocity_slider.value,
            PIXELS_PER_METER
        )

        for point in trajectory_points:
            pygame.draw.circle(screen, (255, 255, 0), point, 2)

        if landing_point:
            pygame.draw.circle(
                screen,
                (255, 0, 0),
                (int(landing_point[0]), int(landing_point[1])),
                6
            )

            distance_px = landing_point[0] - hand_pos[0]
            distance_m = distance_px / PIXELS_PER_METER

            text = UI_FONT.render(
                f"Distance: {distance_m:.2f} m",
                True,
                (255, 200, 0)
            )
            screen.blit(text, (20, HEIGHT - 40))

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
            20, 20,
            420, 160,
            angle_slider.value,
            velocity_slider.value,
            height_slider.value,
            UI_FONT,
            TITLE_FONT
        )

        pygame.display.flip()

    pygame.quit()


def draw_stickman(screen, pos, height_cm):
    x = int(pos.x)
    ground_y = int(pos.y)

    reference_height = 180
    scale = height_cm / reference_height

    body_height = int(120 * scale)

    head_y = ground_y - body_height
    head_radius = int(10 * scale)

    pygame.draw.circle(screen, "black", (x, head_y), head_radius)

    body_top = head_y + head_radius
    body_bottom = ground_y - int(40 * scale)

    pygame.draw.line(screen, "black", (x, body_top), (x, body_bottom), 3)

    arm_y = body_top + int(30 * scale)
    left_hand = (x - int(25 * scale), arm_y)
    right_hand = (x + int(25 * scale), arm_y)

    pygame.draw.line(screen, "black", left_hand, right_hand, 3)

    pygame.draw.line(screen, "black",
                     (x, body_bottom),
                     (x - int(20 * scale), ground_y), 3)

    pygame.draw.line(screen, "black",
                     (x, body_bottom),
                     (x + int(20 * scale), ground_y), 3)

    pygame.draw.circle(screen, (255, 0, 0), left_hand, int(6 * scale))

    return left_hand

