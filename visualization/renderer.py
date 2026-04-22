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
RESULT_FONT = pygame.font.SysFont("Arial", 48, bold=True)
TUTORIAL_FONT = pygame.font.SysFont("Arial", 24, italic=True)


def show_start_screen(screen):
    start_time = pygame.time.get_ticks()
    duration = 2500
    while pygame.time.get_ticks() - start_time < duration:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return False
        
        screen.fill((30, 30, 30))
        title = TITLE_FONT.render("Discus Throwing Simulator", True, "white")
        subtitle = UI_FONT.render("Loading...", True, "white")
        
        screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2 - 60))
        screen.blit(subtitle, (WIDTH//2 - subtitle.get_width()//2, HEIGHT//2 + 20))
        
        pygame.display.flip()
    return True


def render_game():
    panel_width, panel_height = 320, 260
    panel_x, panel_y = WIDTH - panel_width - 20, 20
    PIXELS_PER_METER = 17.5

    angle_slider = Slider(panel_x + 20, panel_y + 80, 260, 10, 80, 45, "θ (Angle)", "°")
    velocity_slider = Slider(panel_x + 20, panel_y + 140, 260, 8, 32, 18, "v (Velocity)", " m/s")
    height_slider = Slider(panel_x + 20, panel_y + 200, 260, 120, 220, 180, "h (Height)", " cm")

    clock = pygame.time.Clock()
    if not show_start_screen(screen): return

    space = create_space()
    player_body = create_player(space)
    create_ground(space, WIDTH)

    state = "idle" 
    anim_timer = 0.0
    WINDUP_DURATION = 0.4 
    
    discus_pos = None
    discus_velocity = [0, 0]
    GRAVITY_PX = 9.81 * PIXELS_PER_METER
    
    show_ui_trajectory = True
    saved_landing = None
    final_distance = 0.0

    running = True
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
                    state = "windup"
                    anim_timer = 0.0
                    show_ui_trajectory = False
                
                if event.key == pygame.K_r and state == "landed":
                    state = "idle"
                    show_ui_trajectory = True
                    discus_pos = None

        if state == "windup":
            anim_timer += dt
            if anim_timer >= WINDUP_DURATION:
                state = "throwing"
                release_hand = draw_stickman(screen, player_body.position, height_slider.value, 1.0)
                
                discus_pos = list(release_hand)
                angle_rad = math.radians(angle_slider.value)
                speed_px = velocity_slider.value * PIXELS_PER_METER * 0.83
                discus_velocity = [speed_px * math.cos(angle_rad), -speed_px * math.sin(angle_rad)]
                
                _, saved_landing = compute_trajectory(discus_pos[0], discus_pos[1], angle_slider.value, velocity_slider.value, PIXELS_PER_METER)
                final_distance = (saved_landing[0] - release_hand[0]) / PIXELS_PER_METER

        elif state == "throwing":
            discus_velocity[1] += GRAVITY_PX * dt
            discus_pos[0] += discus_velocity[0] * dt
            discus_pos[1] += discus_velocity[1] * dt

            if discus_pos[1] >= 600:
                discus_pos[1] = 600
                state = "landed"

        if state == "idle":
            keys = pygame.key.get_pressed()
            apply_input(player_body, (keys[pygame.K_a], keys[pygame.K_d]))

        step(space, dt)

        screen.blit(background, (0, 0))

        swing_f = (anim_timer / WINDUP_DURATION) if state == "windup" else (1.0 if state != "idle" else 0.0)
        hand_pos = draw_stickman(screen, player_body.position, height_slider.value, swing_f, hold_discus=(state in ["idle", "windup"]))

        if state in ["throwing", "landed"] and discus_pos:
            pygame.draw.circle(screen, (255, 0, 0), (int(discus_pos[0]), int(discus_pos[1])), int(10 * (height_slider.value/180)))

        if show_ui_trajectory:
            pts, landing = compute_trajectory(hand_pos[0], hand_pos[1], angle_slider.value, velocity_slider.value, PIXELS_PER_METER)
            for p in pts: pygame.draw.circle(screen, (255, 255, 0), p, 2)
            if landing:
                pygame.draw.circle(screen, (255, 0, 0), (int(landing[0]), int(landing[1])), 6)
                
                dist_m = (landing[0] - hand_pos[0]) / PIXELS_PER_METER
                dist_text = UI_FONT.render(f"Predicted Distance: {dist_m:.2f} m", True, (255, 200, 0))
                screen.blit(dist_text, (20, HEIGHT - 40))

            instr_box = pygame.Surface((400, 80), pygame.SRCALPHA)
            instr_box.fill((0, 0, 0, 150))
            screen.blit(instr_box, (WIDTH//2 - 200, HEIGHT - 100))
            
            move_hint = TUTORIAL_FONT.render("A / D to Move Player", True, "white")
            throw_hint = TUTORIAL_FONT.render("SPACE to Throw Discus", True, (255, 200, 0))
            
            screen.blit(move_hint, (WIDTH//2 - move_hint.get_width()//2, HEIGHT - 90))
            screen.blit(throw_hint, (WIDTH//2 - throw_hint.get_width()//2, HEIGHT - 60))
        
        elif state == "landed":
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 120))
            screen.blit(overlay, (0, 0))
            
            panel_rect = pygame.Rect(WIDTH//2 - 300, HEIGHT//2 - 120, 600, 240)
            pygame.draw.rect(screen, (40, 40, 40), panel_rect, border_radius=20)
            pygame.draw.rect(screen, (255, 200, 0), panel_rect, 4, border_radius=20)
            
            msg = "Incredible Throw!" if final_distance > 60 else "Nice Attempt!"
            msg_text = RESULT_FONT.render(msg, True, (255, 200, 0))
            res_text = RESULT_FONT.render(f"You threw {final_distance:.2f} meters", True, "white")
            retry_text = UI_FONT.render("PRESS 'R' TO RETRY", True, (255, 200, 0))
            
            screen.blit(msg_text, (WIDTH//2 - msg_text.get_width()//2, HEIGHT//2 - 80))
            screen.blit(res_text, (WIDTH//2 - res_text.get_width()//2, HEIGHT//2 - 20))
            screen.blit(retry_text, (WIDTH//2 - retry_text.get_width()//2, HEIGHT//2 + 50))

        draw_slider_panel(screen, panel_x, panel_y, panel_width, panel_height, "Parameters", [angle_slider, velocity_slider, height_slider], UI_FONT, TITLE_FONT)
        draw_formula_panel(screen, 20, 20, 420, 160, angle_slider.value, velocity_slider.value, height_slider.value, UI_FONT, TITLE_FONT)
        
        pygame.display.flip()

    pygame.quit()


def draw_stickman(screen, pos, height_cm, swing_factor=0.0, hold_discus=True):
    x, ground_y = int(pos.x), int(pos.y)
    scale = height_cm / 180
    lean = int(10 * swing_factor * scale)
    body_h = int(120 * scale)
    head_y = ground_y - body_h
    head_r = int(10 * scale)

    pygame.draw.circle(screen, "black", (x + lean, head_y), head_r)
    body_top, body_bot = head_y + head_r, ground_y - int(40 * scale)
    pygame.draw.line(screen, "black", (x + lean, body_top), (x, body_bot), 3)

    sh_y = body_top + int(30 * scale)
    reach_x, reach_y = -25 + (65 * swing_factor), 0 - (30 * swing_factor)
    l_hand = (x + int(reach_x * scale) + lean, sh_y + int(reach_y * scale))
    r_hand = (x + int(25 * scale), sh_y + int(10 * scale))

    pygame.draw.line(screen, "black", (x + lean, sh_y), l_hand, 3)
    pygame.draw.line(screen, "black", (x + lean, sh_y), r_hand, 3)

    pygame.draw.line(screen, "black", (x, body_bot), (x - int(20 * scale), ground_y), 3)
    pygame.draw.line(screen, "black", (x, body_bot), (x + int(20 * scale), ground_y), 3)
    
    if hold_discus:
        pygame.draw.circle(screen, (255, 0, 0), l_hand, int(10 * scale))

    return l_hand

