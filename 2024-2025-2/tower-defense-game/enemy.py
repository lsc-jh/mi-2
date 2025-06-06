import math
import pygame

class Enemy:
    def __init__(self, path, speed=2):
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

