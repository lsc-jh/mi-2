import math
import pygame

class Enemy:
    def __init__(self, path, speed=2, max_hp=100):
        self.max_hp = max_hp
        self.hp = max_hp
        self.path = path
        self.speed = speed
        self.pos = list(path[0])
        self.current_target = 1
        self.reached_end = False

    def update(self):
        if self.reached_end or self.current_target >= len(self.path):
            self.reached_end = True
            return

        target = self.path[self.current_target]
        dx = target[0] - self.pos[0]
        dy = target[1] - self.pos[1]
        dist = math.hypot(dx, dy)

        if dist < self.speed:
            self.pos = list(target)
            self.current_target += 1
        else:
            self.pos[0] += dx / dist * self.speed
            self.pos[1] += dy / dist * self.speed

    def draw(self, screen):
        pygame.draw.circle(
            screen,
            (255, 0, 0),
            (self.pos[0], self.pos[1]),
            10
        )

        bar_width = 20
        bar_height = 4
        hp_ratio = self.hp / self.max_hp
        x = int(self.pos[0] - bar_width / 2)
        y = int(self.pos[1] - 18)
        pygame.draw.rect(screen, (255, 0, 0), (x, y, bar_width, bar_height))
        pygame.draw.rect(screen, (0, 255, 0), (x, y, int(bar_width * hp_ratio), bar_height))

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.reached_end = True
