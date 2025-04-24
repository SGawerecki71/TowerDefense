import pygame
import math
from projectile import Projectile

class Tower:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.range = 100
        self.color = (0, 200, 255)
        self.radius = 15
        self.cooldown = 0  
        self.fire_rate = 60  
        self.damage = 20

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
        pygame.draw.circle(screen, (0, 100, 255), (self.x, self.y), self.range, 1)

    def update(self, enemies):
        if self.cooldown > 0:
            self.cooldown -= 1
            return

        for enemy in enemies:
            if enemy.reached_end:
                continue
            dx = self.x - enemy.x
            dy = self.y - enemy.y
            distance = math.hypot(dx, dy)
            if distance <= self.range:
                enemy.health -= 20
                self.cooldown = self.fire_rate
                return Projectile(self.x, self.y, enemy, self.damage)
            return None
