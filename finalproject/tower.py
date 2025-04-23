import pygame

class Tower:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.range = 100  # For later targeting
        self.color = (0, 200, 255)
        self.radius = 15

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
