import random
import sys
import pygame

from config import (
    BASE_W, BASE_H, WINDOW_W, WINDOW_H, FPS, SHELF_DEFS, DOOR_RECT,
    SNACK_TYPES, INTERACT_RANGE, UI_BG, UI_TEXT, WHITE, YELLOW, GREEN, RED,
)
from utils import load_image
from ui import Popup
from player import Player
from clerk import Clerk

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Late Snack Operation")
        self.window = pygame.display.set_mode((WINDOW_W, WINDOW_H))
        self.canvas = pygame.Surface((BASE_W, BASE_H))
        self.clock = pygame.time.Clock()

        self.font_small = pygame.font.SysFont("arial", 12, bold=True)
        self.font = pygame.font.SysFont("arial", 13)
        self.font_big = pygame.font.SysFont("arial", 26, bold=True)
        self.font_mid = pygame.font.SysFont("arial", 16, bold=True)

        self._load_assets()

        self.shelf_rects = [s["rect"] for s in SHELF_DEFS]
        self.popup = Popup(self.font_mid)

        self.state = "menu"
        self.level = 1
        self.score = 0
        self.transition_timer = 0.0

        self.player = Player(self.player_sprites, self.icon_small)
        self.clerk = None
        self.shelf_snacks = {}
        self.shelf_checked = {}
        self.target_snack = None

        self.new_level(first=True)

    def _load_assets(self):
        self.floor_img = load_image("floor.png")
        self.door_img = load_image("door.png")
        self.shelf_imgs = [load_image(f"{s['name']}.png") for s in SHELF_DEFS]
        self.overlay_img = load_image("black_overlay.png")

        self.static_bg = pygame.Surface((BASE_W, BASE_H), pygame.SRCALPHA)
        self.static_bg.blit(self.floor_img, (0, 0))
        for img in self.shelf_imgs:
            self.static_bg.blit(img, (0, 0))
        self.static_bg.blit(self.door_img, (0, 0))

        self.player_sprites = {
            "left": load_image("maling_l.png", (40, 40)),
            "right": load_image("maling_r.png", (40, 40)),
        }

        self.icon_small = {
            name: load_image(f"{name}.png", (22, 22))
            for name in SNACK_TYPES
        }
        self.icon_tiny = {
            name: load_image(f"{name}.png", (16, 16))
            for name in SNACK_TYPES
        }

    def new_level(self, first=False):
        self.player.reset()

        chosen = random.sample(SNACK_TYPES, k=len(SHELF_DEFS))
        self.shelf_snacks = {
            s["name"]: chosen[i] for i, s in enumerate(SHELF_DEFS)
        }
        self.shelf_checked = {
            s["name"]: False for s in SHELF_DEFS
        }
        self.target_snack = random.choice(chosen)

        self.clerk = Clerk(self.level)
        self.clerk.spawn(
            random_pos=True,
            obstacles=self.shelf_rects,
            exclude_rect=self.player.rect,
        )

        if not first:
            self.popup.show(
                f"Level {self.level}! Cari {self.target_snack.upper()}", 2.2
            )
        self.state = "playing"

    def restart_run(self):
        self.level = 1
        self.score = 0
        self.new_level(first=True)
        self.state = "playing"

    def nearest_shelf(self):
        best, best_dist = None, INTERACT_RANGE
        p = pygame.Vector2(self.player.rect.center)
        for s in SHELF_DEFS:
            r = s["rect"]
            closest = pygame.Vector2(
                max(r.left, min(p.x, r.right)),
                max(r.top, min(p.y, r.bottom)),
            )
            dist = p.distance_to(closest)
            if dist < best_dist:
                best, best_dist = s, dist
        return best

    def try_interact(self):
        shelf = self.nearest_shelf()
        if not shelf:
            return

        name = shelf["name"]
        snack = self.shelf_snacks[name]

        if not self.shelf_checked[name]:
            self.shelf_checked[name] = True
            if snack == self.target_snack and self.player.holding_snack is None:
                self.player.holding_snack = snack
                self.popup.show(
                    f"Dapat {snack.upper()}! Kembali ke pintu!", 1.8
                )
            else:
                self.popup.show(f"Cuma ada {snack.upper()}...", 1.4)
        else:
            self.popup.show(f"({snack.upper()})", 1.0)

    def run(self):
        while True:
            dt = self.clock.tick(FPS) / 1000.0
            dt = min(dt, 0.05)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

                    if event.key == pygame.K_SPACE:
                        if self.state == "menu":
                            self.restart_run()
                        elif self.state == "gameover":
                            self.restart_run()
                        elif self.state == "playing":
                            self.try_interact()

            if self.state == "playing":
                self.update_playing(dt)

            self.draw()

    def update_playing(self, dt):
        self.popup.update(dt)
        self.player.handle_input(dt, self.shelf_rects)
        self.clerk.update(dt, self.player.rect, self.shelf_rects)

        if self.clerk.just_detected:
            self.popup.show("TERDETEKSI!", 1.2)

        if self.clerk.rect.colliderect(self.player.rect.inflate(-4, -4)):
            self.state = "gameover"
            return

        if self.player.holding_snack and DOOR_RECT.colliderect(self.player.rect):
            self.score += 100 * self.level
            self.level += 1
            self.new_level()

    def draw(self):
        c = self.canvas

        if self.state == "menu":
            self.draw_menu(c)
        elif self.state == "gameover":
            self.draw_world(c, dim=True)
            self.draw_gameover(c)
        else:
            self.draw_world(c)

        scaled = pygame.transform.scale(c, (WINDOW_W, WINDOW_H))
        self.window.blit(scaled, (0, 0))
        pygame.display.flip()

    def draw_world(self, c, dim=False):
        c.blit(self.static_bg, (0, 0))

        for s in SHELF_DEFS:
            if self.shelf_checked[s["name"]]:
                snack = self.shelf_snacks[s["name"]]
                icon = self.icon_small[snack]
                r = s["rect"]
                icon_x = r.centerx - icon.get_width() // 2
                if r.top - icon.get_height() - 2 > 22:
                    icon_y = r.top - icon.get_height() - 2
                else:
                    icon_y = r.bottom + 2
                c.blit(icon, (icon_x, icon_y))

        self.clerk.draw(c, self.font_small)
        self.player.draw(c)

        shelf = self.nearest_shelf()
        if shelf and self.state == "playing":
            label = (
                "periksa"
                if not self.shelf_checked[shelf["name"]]
                else "lihat lagi"
            )
            hint = self.font.render(f"[SPACE] {label}", True, WHITE)
            box = pygame.Surface(
                (hint.get_width() + 8, hint.get_height() + 4),
                pygame.SRCALPHA,
            )
            box.fill((0, 0, 0, 150))
            box.blit(hint, (4, 2))
            c.blit(
                box,
                (
                    self.player.rect.centerx - box.get_width() // 2,
                    self.player.rect.top - 42,
                ),
            )

        self.draw_hud(c)
        self.popup.draw(c)

        if dim:
            dark = pygame.Surface((BASE_W, BASE_H), pygame.SRCALPHA)
            dark.fill((0, 0, 0, 140))
            c.blit(dark, (0, 0))

    def draw_hud(self, c):
        bar = pygame.Surface((BASE_W, 20), pygame.SRCALPHA)
        bar.fill((*UI_BG, 210))
        c.blit(bar, (0, 0))

        lvl_txt = self.font.render(f"Level {self.level}", True, UI_TEXT)
        c.blit(lvl_txt, (8, 4))

        score_txt = self.font.render(f"Skor {self.score}", True, UI_TEXT)
        c.blit(score_txt, (110, 4))

        target_label = self.font.render("Target:", True, UI_TEXT)
        c.blit(target_label, (210, 4))
        icon = self.icon_tiny[self.target_snack]
        c.blit(icon, (262, 2))
        name_txt = self.font.render(self.target_snack.upper(), True, YELLOW)
        c.blit(name_txt, (282, 4))

        if self.player.holding_snack:
            hold_txt = self.font.render(
                "Bawa snack! -> pintu keluar", True, GREEN
            )
            c.blit(hold_txt, (BASE_W - hold_txt.get_width() - 8, 4))

    def draw_menu(self, c):
        c.blit(self.static_bg, (0, 0))
        dark = pygame.Surface((BASE_W, BASE_H), pygame.SRCALPHA)
        dark.fill((0, 0, 0, 165))
        c.blit(dark, (0, 0))

        title = self.font_big.render("LATE SNACK OPERATION", True, WHITE)
        c.blit(title, (BASE_W // 2 - title.get_width() // 2, 90))

        sub = self.font.render(
            "Curi snack incaranmu, kabur lewat pintu yang sama tanpa ketahuan clerk.",
            True,
            UI_TEXT,
        )
        c.blit(sub, (BASE_W // 2 - sub.get_width() // 2, 140))

        ctrl = self.font.render(
            "Arrow Keys: gerak   |   SPACE: periksa shelf / mulai   |   ESC: keluar",
            True,
            UI_TEXT,
        )
        c.blit(ctrl, (BASE_W // 2 - ctrl.get_width() // 2, 165))

        prompt = self.font_mid.render(
            "Tekan SPACE untuk mulai", True, YELLOW
        )
        c.blit(prompt, (BASE_W // 2 - prompt.get_width() // 2, 210))

    def draw_gameover(self, c):
        panel = pygame.Surface((300, 110), pygame.SRCALPHA)
        panel.fill((15, 15, 15, 220))

        title = self.font_big.render("TERTANGKAP!", True, RED)
        panel.blit(title, (panel.get_width() // 2 - title.get_width() // 2, 12))

        info = self.font.render(
            f"Level tercapai: {self.level}    Skor: {self.score}",
            True,
            WHITE,
        )
        panel.blit(info, (panel.get_width() // 2 - info.get_width() // 2, 52))

        prompt = self.font.render(
            "Tekan SPACE untuk ulang dari Level 1", True, YELLOW
        )
        panel.blit(prompt, (panel.get_width() // 2 - prompt.get_width() // 2, 78))

        c.blit(
            panel,
            (
                BASE_W // 2 - panel.get_width() // 2,
                BASE_H // 2 - panel.get_height() // 2,
            ),
        )
