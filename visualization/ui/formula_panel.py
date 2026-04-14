import pygame

def draw_formula_panel(screen, x, y, width, height, theta, velocity, height_cm, ui_font, title_font):
    panel = pygame.Surface((width, height))
    panel.set_alpha(140)
    panel.fill((0, 0, 0))
    screen.blit(panel, (x, y))

    title = title_font.render("Discus Motion", True, (220, 50, 50))
    screen.blit(title, (x + 80, y + 10))

    formula_img = pygame.image.load("visualization/assets/formula.png")
    screen.blit(formula_img, (x + 10, y + 45))

    line3 = ui_font.render("Inputs: θ, v, h", True, "gray")

    h_m = height_cm / 100.0
    line4 = ui_font.render(
        f"θ={int(theta)}°   v={int(velocity)} m/s   h={h_m:.2f} m",
        True,
        (255, 200, 0)
    )

    screen.blit(line3, (x + 10, y + 110))
    screen.blit(line4, (x + 10, y + 130))

