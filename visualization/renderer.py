import pygame
import math

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
    PIXELS_PER_METER = 17.5

    angle_slider = Slider(panel_x + 20, panel_y + 80, 260, 10, 80, 45, "θ (Angle)", "°")
    velocity_slider = Slider(panel_x + 20, panel_y + 140, 260, 8, 32, 18, "v (Velocity)", " m/s")
    height_slider = Slider(panel_x + 20, panel_y + 200, 260, 120, 220, 180, "h (Height)", " cm")

    clock = pygame.time.Clock()
    if not show_start_screen(screen): return

    running = True
    space = create_space()
    body = create_player(space)
    create_ground(space, WIDTH)

    state = "idle" 
    anim_timer = 0.0
    WINDUP_DURATION = 0.4 
    
    show_ui_trajectory = True
    frozen_points = []
    saved_landing = None

    while running:
        dt = clock.tick(60) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False

            if state == "idle":
                angle_slider.handle_event(event)
                velocity_slider.handle_event(event)
                height_slider.handle_event(event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and state == "idle":
                    temp_hand = draw_stickman(screen, body.position, height_slider.value, 0.0)
                    frozen_points, saved_landing = compute_trajectory(
                        temp_hand[0], temp_hand[1],
                        angle_slider.value, velocity_slider.value,
                        PIXELS_PER_METER
                    )
                    
                    state = "windup"
                    anim_timer = 0.0
                    show_ui_trajectory = False

        if state == "windup":
            anim_timer += dt
            if anim_timer >= WINDUP_DURATION:
                state = "throwing"
                release_hand = draw_stickman(screen, body.position, height_slider.value, 1.0)
                apply_throw(body, angle_slider.value, velocity_slider.value, release_hand)

        if state == "throwing":
            if body.position.y >= 600:
                body.velocity = (0, 0)
                body.position = (body.position.x, 600)
                state = "idle"
                show_ui_trajectory = True

        if state == "idle":
            keys = pygame.key.get_pressed()
            apply_input(body, (keys[pygame.K_a], keys[pygame.K_d]))

        step(space, dt)

        screen.blit(background, (0, 0))

        current_swing = 0.0
        if state == "windup":
            current_swing = anim_timer / WINDUP_DURATION
        elif state == "throwing":
            current_swing = 1.0 

        hand_pos = draw_stickman(screen, body.position, height_slider.value, current_swing)

        if show_ui_trajectory:
            pts, landing = compute_trajectory(hand_pos[0], hand_pos[1], angle_slider.value, velocity_slider.value, PIXELS_PER_METER)
            for p in pts: pygame.draw.circle(screen, (255, 255, 0), p, 2)
            if landing:
                pygame.draw.circle(screen, (255, 0, 0), (int(landing[0]), int(landing[1])), 6)
                dist = (landing[0] - hand_pos[0]) / PIXELS_PER_METER
                screen.blit(UI_FONT.render(f"Predicted: {dist:.2f} m", True, (255, 200, 0)), (20, HEIGHT - 40))
        else:
            if saved_landing:
                pygame.draw.circle(screen, (150, 0, 0), (int(saved_landing[0]), int(saved_landing[1])), 6)

        draw_slider_panel(screen, panel_x, panel_y, panel_width, panel_height, "Parameters", [angle_slider, velocity_slider, height_slider], UI_FONT, TITLE_FONT)
        draw_formula_panel(screen, 20, 20, 420, 160, angle_slider.value, velocity_slider.value, height_slider.value, UI_FONT, TITLE_FONT)
        pygame.display.flip()

    pygame.quit()


def draw_stickman(screen, pos, height_cm, swing_factor=0.0):
    x, ground_y = int(pos.x), int(pos.y)
    scale = height_cm / 180
    
    lean = int(10 * swing_factor * scale)
    body_height = int(120 * scale)
    head_y = ground_y - body_height
    head_radius = int(10 * scale)

    pygame.draw.circle(screen, "black", (x + lean, head_y), head_radius)
    body_top, body_bottom = head_y + head_radius, ground_y - int(40 * scale)
    pygame.draw.line(screen, "black", (x + lean, body_top), (x, body_bottom), 3)

    arm_shoulder_y = body_top + int(30 * scale)
    
    reach_x = -25 + (65 * swing_factor)
    reach_y = 0 - (30 * swing_factor)
    
    left_hand = (x + int(reach_x * scale) + lean, arm_shoulder_y + int(reach_y * scale))
    right_hand = (x + int(25 * scale), arm_shoulder_y + int(10 * scale))

    pygame.draw.line(screen, "black", (x + lean, arm_shoulder_y), left_hand, 3)
    pygame.draw.line(screen, "black", (x + lean, arm_shoulder_y), right_hand, 3)

    pygame.draw.line(screen, "black", (x, body_bottom), (x - int(20 * scale), ground_y), 3)
    pygame.draw.line(screen, "black", (x, body_bottom), (x + int(20 * scale), ground_y), 3)
    
    pygame.draw.circle(screen, (255, 0, 0), left_hand, int(6 * scale))

    return left_hand

