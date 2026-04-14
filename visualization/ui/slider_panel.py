import pygame

def draw_slider_panel(screen, panel_x, panel_y, panel_width, panel_height, title, sliders, ui_font, title_font):
    panel = pygame.Surface((panel_width, panel_height))
    panel.set_alpha(140)
    panel.fill((0, 0, 0))
    screen.blit(panel, (panel_x, panel_y))

    title_text = title_font.render(title, True, (220, 50, 50))
    screen.blit(title_text, (panel_x + 80, panel_y + 15))

    for slider in sliders:
        slider.draw(screen, ui_font)

