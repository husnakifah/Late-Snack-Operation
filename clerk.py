import math
import random
import pygame

from config import (
    BASE_W, BASE_H, BASE_CLERK_SPEED, BASE_VISION_RANGE,
    BASE_VISION_HALF_ANGLE, CHASE_MULT, CHASE_DURATION,
    DIRS, PLAY_RECT, RED, WHITE, YELLOW,
)
from utils import line_blocked_by_rects, move_with_collision

class Clerk:
    def __init__(self, level):
        self.level = level
        self.patrol_speed = min(95.0, BASE_CLERK_SPEED + level * 2.5)
        self.vision_range = min(175, BASE_VISION_RANGE + level * 4)
        self.vision_half_angle = BASE_VISION_HALF_ANGLE
        self.rect = pygame.Rect(0, 0, 22, 22)
        self.state = "patrol"
        self.chase_timer = 0.0
        self.wander_timer = 0.0
        self.facing_name = random.choice(list(DIRS.keys()))
        self.just_detected = False
        self.spawn(random_pos=True)

    def spawn(self, random_pos=True, obstacles=None, exclude_rect=None):
        if random_pos:
            for _ in range(200):
                x = random.randint(PLAY_RECT.left + 20, PLAY_RECT.right - 20)
                y = random.randint(PLAY_RECT.top + 20, PLAY_RECT.bottom - 20)
                self.rect.center = (x, y)
                collides = obstacles and any(self.rect.colliderect(o) for o in obstacles)
                too_close = exclude_rect and self.rect.colliderect(exclude_rect.inflate(80, 80))
                if not collides and not too_close:
                    break
        self.state = "patrol"
        self.chase_timer = 0.0
        self.wander_timer = random.uniform(0.8, 2.0)
        self.facing_name = random.choice(list(DIRS.keys()))

    def _pick_new_wander_dir(self):
        self.facing_name = random.choice(list(DIRS.keys()))
        self.wander_timer = random.uniform(0.8, 2.2)

    def update(self, dt, player_rect, obstacles):
        self.just_detected = False

        if self.state == "patrol":
            facing_vec = DIRS[self.facing_name]
            to_player = pygame.Vector2(player_rect.center) - pygame.Vector2(self.rect.center)
            dist = to_player.length()
            if dist <= self.vision_range and dist > 0.01:
                angle_diff = abs(facing_vec.angle_to(to_player))
                angle_diff = min(angle_diff, 360 - angle_diff)
                if angle_diff <= self.vision_half_angle:
                    if not line_blocked_by_rects(self.rect.center, player_rect.center, obstacles):
                        self.state = "chase"
                        self.chase_timer = CHASE_DURATION
                        self.just_detected = True

        if self.state == "chase":
            to_player = pygame.Vector2(player_rect.center) - pygame.Vector2(self.rect.center)
            if to_player.length_squared() > 1:
                move_vec = to_player.normalize() * self.patrol_speed * CHASE_MULT * dt
                move_with_collision(self.rect, move_vec.x, move_vec.y, obstacles, PLAY_RECT)
            self.chase_timer -= dt
            if self.chase_timer <= 0:
                self._pick_new_wander_dir()
                self.state = "patrol"
        else:
            self.wander_timer -= dt
            move_vec = DIRS[self.facing_name] * self.patrol_speed * dt
            blocked = move_with_collision(self.rect, move_vec.x, move_vec.y, obstacles, PLAY_RECT)
            if blocked or self.wander_timer <= 0:
                self._pick_new_wander_dir()

    def vision_polygon(self):
        facing_vec = DIRS[self.facing_name]
        base_angle = math.degrees(math.atan2(facing_vec.y, facing_vec.x))
        points = [pygame.Vector2(self.rect.center)]
        steps = 10
        for i in range(steps + 1):
            a = math.radians(
                base_angle - self.vision_half_angle
                + (2 * self.vision_half_angle) * i / steps
            )
            points.append(pygame.Vector2(
                self.rect.centerx + math.cos(a) * self.vision_range,
                self.rect.centery + math.sin(a) * self.vision_range
            ))
        return points

    def draw(self, surface, font_small):
        color = RED if self.state == "chase" else YELLOW
        cone_surf = pygame.Surface((BASE_W, BASE_H), pygame.SRCALPHA)
        pygame.draw.polygon(cone_surf, (*color, 70), self.vision_polygon())
        surface.blit(cone_surf, (0, 0))

        body_color = (200, 70, 70) if self.state == "chase" else (70, 120, 200)
        pygame.draw.ellipse(
            surface, (0, 0, 0, 90),
            self.rect.move(0, self.rect.height // 2).inflate(4, -14)
        )
        pygame.draw.circle(surface, body_color, self.rect.center, 11)
        pygame.draw.circle(surface, (255, 214, 181),
                           (self.rect.centerx, self.rect.centery - 9), 6)
        if self.state == "chase":
            f = font_small.render("!", True, WHITE)
            surface.blit(f, (self.rect.centerx - 2, self.rect.top - 16))
