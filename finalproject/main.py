import pygame
import sys
from enemy import Enemy
from tower import Tower

# --- Game Config ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 40

# --- Colors ---
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BACKGROUND_COLOR = (30, 30, 30)

# --- Initialize ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tower Defense")
clock = pygame.time.Clock()

# --- Functions ---
def draw_grid():
    for x in range(0, SCREEN_WIDTH, GRID_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (SCREEN_WIDTH, y))

def build_path():
    return [
        (0, 60), (40, 60), (80, 60), (120, 60), (160, 60), 
        (200, 60), (240, 60), (280, 60), (320, 60), 
        (360, 60), (400, 60), (400, 100), (400, 140),
        (400, 180), (400, 220), (440, 220), (480, 220),
        (520, 220), (560, 220), (600, 220), (640, 220),
        (680, 220), (720, 220)
    ]

def main():
    running = True
    path = build_path()
    enemies = [Enemy(path)]
    towers = []

    while running:
        screen.fill(BACKGROUND_COLOR)
        draw_grid()

        # Update & draw enemies
        for enemy in enemies:
            enemy.update()
            enemy.draw(screen)

        # Draw towers
        for tower in towers:
            tower.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                grid_x = (mouse_x // GRID_SIZE) * GRID_SIZE + GRID_SIZE // 2
                grid_y = (mouse_y // GRID_SIZE) * GRID_SIZE + GRID_SIZE // 2

                # Avoid placing multiple towers in same cell
                if not any(t.x == grid_x and t.y == grid_y for t in towers):
                    towers.append(Tower(grid_x, grid_y))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
