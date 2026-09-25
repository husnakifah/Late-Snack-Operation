import os
import pygame

BASE_W, BASE_H = 640, 360
SCALE = 2
WINDOW_W, WINDOW_H = BASE_W * SCALE, BASE_H * SCALE
FPS = 60

ASSET_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 220, 90)
RED = (230, 70, 70)
GREEN = (110, 210, 120)
UI_BG = (20, 24, 30)
UI_TEXT = (235, 235, 235)

PLAY_RECT = pygame.Rect(18, 18, 620 - 18, 340 - 18)

SHELF_DEFS = [
    {"name": "shelf1", "rect": pygame.Rect(72, 112, 48, 161)},
    {"name": "shelf2", "rect": pygame.Rect(172, 112, 48, 161)},
    {"name": "shelf3", "rect": pygame.Rect(272, 112, 48, 161)},
    {"name": "shelf4", "rect": pygame.Rect(394, 148, 48, 161)},
    {"name": "shelf5", "rect": pygame.Rect(494, 148, 48, 161)},
    {"name": "shelf6", "rect": pygame.Rect(56, 17, 128, 49)},
    {"name": "shelf7", "rect": pygame.Rect(256, 17, 128, 49)},
    {"name": "shelf8", "rect": pygame.Rect(433, 32, 187, 87)},
]

DOOR_RECT = pygame.Rect(79, 328, 112, 21)
PLAYER_START = pygame.Vector2(135, 300)

SNACK_TYPES = [
    "biscuit", "candy", "chips", "choco", "cookie",
    "icecream", "milk", "popcorn", "soda", "tortilla",
]

INTERACT_RANGE = 30
PLAYER_SPEED = 135.0
BASE_CLERK_SPEED = 62.0
CHASE_MULT = 1.5
CHASE_DURATION = 10.0
BASE_VISION_RANGE = 118
BASE_VISION_HALF_ANGLE = 33

DIRS = {
    "up": pygame.Vector2(0, -1),
    "down": pygame.Vector2(0, 1),
    "left": pygame.Vector2(-1, 0),
    "right": pygame.Vector2(1, 0),
}
