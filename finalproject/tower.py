import pygame
import math
from projectile import Projectile

WHITE = (255, 255, 255)

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
        self.level = 1
        self.upgrade_cost = 50

    def in_range(self, enemy):
        dist = math.hypot(self.x -enemy.x, self.y - enemy.y)
        return dist <= self.range
    
    def upgrade(self):
        self.level += 1
        self.range += 20
        self.damage += 5
        self.fire_rate = max(10, self.fire_rate - 5)
        self.upgrade_cost += 50

    def draw(self, surface):
        pygame.draw.circle(surface, (0, 0, 255), (self.x, self.y), 15)
        pygame.draw.circle(surface, (0, 100, 255), (self.x, self.y), self.range, 1)  # Show range

        font = pygame.font.SysFont(None, 18)
        level_text = font.render(f"{self.level}", True, WHITE)
        surface.blit(level_text, (self.x - 5, self.y - 10))

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
