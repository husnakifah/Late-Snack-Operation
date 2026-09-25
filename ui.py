import pygame
from config import BASE_W, WHITE

class Popup:
    def __init__(self, font):
        self.font = font
        self.text = ""
        self.timer = 0.0
        self.duration = 1.6

    def show(self, text, duration=1.6):
        self.text = text
        self.duration = duration
        self.timer = duration

    def update(self, dt):
        if self.timer > 0:
            self.timer = max(0.0, self.timer - dt)

    def draw(self, surface):
        if self.timer <= 0 or not self.text:
            return
        alpha = int(255 * min(1.0, self.timer / (self.duration * 0.4)))
        alpha = max(0, min(255, alpha))
        label = self.font.render(self.text, True, WHITE)
        box = pygame.Surface((label.get_width() + 24, label.get_height() + 14), pygame.SRCALPHA)
        box.fill((0, 0, 0, min(180, alpha)))
        label.set_alpha(alpha)
        box.blit(label, (12, 7))
        surface.blit(box, (BASE_W // 2 - box.get_width() // 2, 60))
