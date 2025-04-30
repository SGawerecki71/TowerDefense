import pygame
import sys
import math
from enemy import Enemy
from tower import Tower
from projectile import Projectile
from quadtree import Quadtree, Rectangle, Point

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 40

WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BACKGROUND_COLOR = (30, 30, 30)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tower Defense")
clock = pygame.time.Clock()

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
    spawn_timer = 0
    spawn_interval = 120  
    projectiles = []

    lives = 10
    wave = 1
    enemy_per = 5
    spawned_thiswave = 0
    spawn_timer = 0
    spawn_interval = 60
    wave_cooldown = 180
    wave_timer = 0

    money = 100
    tower_cost = 25
    enemy_reward = 15

    font = pygame.font.SysFont(None, 28)

    while running:
        screen.fill(BACKGROUND_COLOR)
        draw_grid()

        if spawned_thiswave < enemy_per:
            spawn_timer +=1
            if spawn_timer >= spawn_interval:
                enemies.append(Enemy(path))
                spawned_thiswave += 1
                spawn_timer = 0
        else:
            if not enemies:
                wave_timer += 1
                if wave_timer < wave_cooldown:
                    wave += 1
                    spawned_thiswave = 0
                    wave_timer = 0
                    enemy_per += 2

        for enemy in enemies:
            enemy.update()
            enemy.draw(screen)
            if enemy.reached_end:
                lives -= 1
        
        boundary = Rectangle(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        qt = Quadtree(boundary, 4)

        for enemy in enemies:
            qt.insert(Point(enemy.x, enemy.y, enemy))

        for e in enemies:
            if e.health <= 0:
                money += 10

        enemies = [e for e in enemies if e.health > 0 and not e.reached_end]

        for tower in towers:
            nearby = []
            qt.query_circle(tower.x, tower.y, tower.range, nearby)
            proj = tower.update(nearby)
            if proj:
                projectiles.append(proj)
            tower.draw(screen)
            
        for proj in projectiles:
            proj.update()
            proj.draw(screen)

        projectiles = [p for p in projectiles if not p.hit]

        wave_text = font.render(f"Wave: {wave}", True, WHITE)
        lives_text = font.render(f"Lives: {lives}", True, (255, 100, 100))
        money_text = font.render(f"Money: {money}", True, (255, 255, 100))
        screen.blit(wave_text, (10, 10))
        screen.blit(lives_text, (10, 40))
        screen.blit(money_text,(10,70))

        if lives <= 0:
            game_over = font.render("GAME OVER", True, (255, 0, 0))
            screen.blit(game_over, (SCREEN_WIDTH // 2-80, SCREEN_HEIGHT // 2))
            pygame.display.flip()
            pygame.time.wait(3000)
            running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                grid_x = (mouse_x // GRID_SIZE) * GRID_SIZE + GRID_SIZE // 2
                grid_y = (mouse_y // GRID_SIZE) * GRID_SIZE + GRID_SIZE // 2

                if event.button == 1: 
                    if not any(t.x == grid_x and t.y == grid_y for t in towers) and money >= tower_cost:
                        towers.append(Tower(grid_x, grid_y))
                        money -= tower_cost

                elif event.button == 3:
                    for tower in towers:
                        if math.hypot(tower.x - mouse_x, tower.y - mouse_y) < GRID_SIZE:
                            if money >= tower.upgrade_cost:
                                tower.upgrade()
                                money -= tower.upgrade_cost
                                print(f"Tower upgraded to level {tower.level}")
                            break

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
