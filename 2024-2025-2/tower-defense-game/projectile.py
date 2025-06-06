import pygame
import math

class Projectile:
    def __init__(self, start_pos, target, speed=6, damage=25):
        self.pos = list(start_pos)
        self.target = target
        self.speed = speed
        self.hit = False
        self.damage = damage

    def update(self):
        if self.target.reached_end:
            self.hit = True
            return

        target = self.target.pos
        dx = target[0] - self.pos[0]
        dy = target[1] - self.pos[1]
        dist = math.hypot(dx, dy)

        if dist < self.speed:
            self.hit = True
            self.target.take_damage(self.damage)
        else:
            self.pos[0] += dx / dist * self.speed
            self.pos[1] += dy / dist * self.speed

    def draw(self, screen):
        pygame.draw.circle(
            screen,
            (255, 255, 255),
            (int(self.pos[0]), int(self.pos[1])),
            4
        )