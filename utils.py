import os
import pygame
from config import ASSET_DIR, PLAY_RECT

def load_image(name, size=None):
    path = os.path.join(ASSET_DIR, name)
    img = pygame.image.load(path).convert_alpha()
    if size:
        img = pygame.transform.smoothscale(img, size)
    return img

def move_with_collision(rect, dx, dy, obstacles, bounds):
    blocked_x = blocked_y = False

    rect.x += round(dx)
    for obs in obstacles:
        if rect.colliderect(obs):
            if dx > 0:
                rect.right = obs.left
            elif dx < 0:
                rect.left = obs.right
            blocked_x = True
    if rect.left < bounds.left:
        rect.left = bounds.left
        blocked_x = True
    if rect.right > bounds.right:
        rect.right = bounds.right
        blocked_x = True

    rect.y += round(dy)
    for obs in obstacles:
        if rect.colliderect(obs):
            if dy > 0:
                rect.bottom = obs.top
            elif dy < 0:
                rect.top = obs.bottom
            blocked_y = True
    if rect.top < bounds.top:
        rect.top = bounds.top
        blocked_y = True
    if rect.bottom > bounds.bottom:
        rect.bottom = bounds.bottom
        blocked_y = True

    return blocked_x or blocked_y

def line_blocked_by_rects(p1, p2, rects):
    for r in rects:
        if r.clipline(p1, p2):
            return True
    return False
