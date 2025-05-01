import pygame

class Enemy:
    def __init__(self, path, health = 30):
        self.path = path
        self.path_index = 0
        self.x, self.y = self.path[self.path_index]
        self.speed = 2
        self.radius = 10
        self.reached_end = False
        self.max_health = health
        self.health = health

    def update(self):
        if self.path_index >= len(self.path) - 1:
            if (abs(self.x - self.path[-1][0]) < 1 and abs(self.y - self.path[-1][1]) < 1):
                self.reached_end = True
            return

        target_x, target_y = self.path[self.path_index + 1]
        dx = target_x - self.x
        dy = target_y - self.y
        distance = (dx ** 2 + dy ** 2) ** 0.5

        if distance < self.speed:
            self.x, self.y = target_x, target_y
            self.path_index += 1
        else:
            dx /= distance
            dy /= distance
            self.x += dx * self.speed
            self.y += dy * self.speed

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), (int(self.x), int(self.y)), self.radius)

        bar_width = 20
        bar_height = 4
        health_ratio = self.health / self.max_health
        pygame.draw.rect(screen, (255, 0, 0), (self.x - bar_width // 2, self.y - 20, bar_width, bar_height))
        pygame.draw.rect(screen, (0, 255, 0), (self.x - bar_width // 2, self.y - 20, bar_width * health_ratio, bar_height))

