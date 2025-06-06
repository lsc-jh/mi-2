import pygame
import math
from projectile import Projectile

class Tower:
    def __init__(self, x, y, range_px=150, fire_rate=1000):
        self.pos = (x, y)
        self.range = range_px
        self.fire_rate = fire_rate
        self.time_since_last_shot = 0
        self.projectiles = []

    def update(self, dt, enemies):
        self.time_since_last_shot += dt

        target = None
        min_dist = float("inf")
        for enemy in enemies:
            if enemy.reached_end:
                continue
            ex, ey = enemy.pos
            dist = math.hypot(ex - self.pos[0], ey - self.pos[1])
            if dist <= self.range and dist < min_dist:
                target = enemy
                min_dist = dist

        if target and self.time_since_last_shot >= self.fire_rate:
            self.projectiles.append(Projectile(self.pos, target))
            self.time_since_last_shot = 0

        for p in self.projectiles:
            p.update()

        self.projectiles = [p for p in self.projectiles if not p.hit]

    def draw(self, screen):
        pygame.draw.circle(screen, (0, 100, 200), self.pos, 15)
        pygame.draw.circle(screen, (0, 100, 200), self.pos, self.range, 1)
        for p in self.projectiles:
            p.draw(screen)