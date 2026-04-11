import pygame


class Slider:
    def __init__(self, x, y, w, min_val, max_val, start_val, label, unit=""):
        self.rect = pygame.Rect(x, y, w, 6)
        self.min = min_val
        self.max = max_val
        self.value = start_val
        self.handle_x = x + (start_val - min_val) / (max_val - min_val) * w
        self.dragging = False
        self.label = label
        self.unit = unit

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            handle_rect = pygame.Rect(self.handle_x - 10, self.rect.y - 10, 20, 20)
            if handle_rect.collidepoint(event.pos):
                self.dragging = True

        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False

        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.handle_x = max(self.rect.x, min(event.pos[0], self.rect.x + self.rect.w))
            ratio = (self.handle_x - self.rect.x) / self.rect.w
            self.value = self.min + ratio * (self.max - self.min)

    def draw(self, screen, font):
        pygame.draw.rect(screen, "white", self.rect)
        pygame.draw.circle(screen, "red", (int(self.handle_x), self.rect.y + 3), 8)

        if isinstance(self.value, float):
            val = round(self.value, 1)
        else:
            val = int(self.value)

        text = font.render(f"{self.label}: {val}{self.unit}", True, "white")
        screen.blit(text, (self.rect.x, self.rect.y - 25))
    
