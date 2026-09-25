import pygame
from config import PLAYER_START, PLAYER_SPEED, PLAY_RECT
from utils import move_with_collision

class Player:
    def __init__(self, sprites, icons):
        self.sprites = sprites
        self.icons = icons
        self.pos = pygame.Vector2(PLAYER_START)
        self.rect = pygame.Rect(0, 0, 20, 16)
        self.rect.midbottom = (int(self.pos.x), int(self.pos.y))
        self.facing = "right"
        self.holding_snack = None
        self.alive = True

    def reset(self):
        self.pos = pygame.Vector2(PLAYER_START)
        self.rect.midbottom = (int(self.pos.x), int(self.pos.y))
        self.facing = "right"
        self.holding_snack = None

    def handle_input(self, dt, obstacles):
        keys = pygame.key.get_pressed()
        dx = dy = 0.0
        if keys[pygame.K_LEFT]:
            dx -= 1
        if keys[pygame.K_RIGHT]:
            dx += 1
        if keys[pygame.K_UP]:
            dy -= 1
        if keys[pygame.K_DOWN]:
            dy += 1

        if dx != 0 or dy != 0:
            vec = pygame.Vector2(dx, dy)
            if vec.length_squared() > 0:
                vec = vec.normalize() * PLAYER_SPEED * dt
            if dx > 0:
                self.facing = "right"
            elif dx < 0:
                self.facing = "left"
            move_with_collision(self.rect, vec.x, vec.y, obstacles, PLAY_RECT)
            self.pos.update(self.rect.midbottom)

    def draw(self, surface):
        sprite = self.sprites[self.facing]
        dest = sprite.get_rect(midbottom=(self.rect.centerx, self.rect.bottom + 4))
        surface.blit(sprite, dest)
        if self.holding_snack:
            icon = self.icons[self.holding_snack]
            surface.blit(icon, (self.rect.centerx - icon.get_width() // 2,
                                dest.top - icon.get_height() - 2))
