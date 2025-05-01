import pygame
import sys
import math
import random
from enemy import Enemy
from tower import Tower
from projectile import Projectile
from quadtree import Quadtree, Rectangle, Point

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 40
TOOLBAR_HEIGHT = 100

WIDTH, HEIGHT = 800, 600

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
    return [(0, 100), (200, 100), (200, 300), (600, 300), (600, 150), (800, 150)]

def draw_path(path_points):
    path_color = (100, 100, 100)  # Gray road color
    path_width = 40

    for i in range(len(path_points) - 1):
        start = path_points[i]
        end = path_points[i + 1]
        pygame.draw.line(screen, path_color, start, end, path_width)


def start_menu():
    menu_font = pygame.font.SysFont(None, 48)
    small_font = pygame.font.SysFont(None, 32)
    title_text = menu_font.render("Tower Defense", True, WHITE)

    start_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50)
    quit_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 20, 200, 50)

    stars = [(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)) for _ in range(150)]

    while True:
        screen.fill((10, 10, 30))
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))

        for star in stars:
            brightness = random.randint(180, 255)
            pygame.draw.circle(screen, (brightness, brightness, brightness), star, 1)

        pygame.draw.rect(screen, (0, 150, 0), start_button)
        pygame.draw.rect(screen, (150, 0, 0), quit_button)

        screen.blit(small_font.render("Start Game", True, WHITE), (start_button.x + 40, start_button.y + 10))
        screen.blit(small_font.render("Quit", True, WHITE), (quit_button.x + 75, quit_button.y + 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    return  
                elif quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()
        clock.tick(60)

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

    current_tower_type = "basic"

    wave_in_progress = True
    show_next_wave_button = False

    font = pygame.font.SysFont(None, 28)
    next_wave_button = pygame.Rect(WIDTH - 170, 10, 160, 40)

    while running:
        screen.fill(BACKGROUND_COLOR)
        draw_grid()
        draw_path(path)

        if wave_in_progress and spawned_thiswave < enemy_per:
            spawn_timer +=1
            if spawn_timer >= spawn_interval:
                scaled_health = int(30 * (1.15 ** (wave - 1)))
                #scaled_health = 30 + (wave - 1) * 10  # Increase 10 HP per wave
                enemies.append(Enemy(path, health=scaled_health))
                spawned_thiswave += 1
                spawn_timer = 0
        else:
            if wave_in_progress and spawned_thiswave >= enemy_per and not enemies:
                wave_in_progress = False
                show_next_wave_button = True

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

        if show_next_wave_button:
            pygame.draw.rect(screen, (0, 200, 0), next_wave_button)
            pygame.draw.rect(screen, WHITE, next_wave_button, 2)
            text = font.render("Next Wave", True, WHITE)
            screen.blit(
                text,
                (
                    next_wave_button.centerx - text.get_width() // 2,
                    next_wave_button.centery - text.get_height() // 2
                )
            )


        if lives <= 0:
            game_over = font.render("GAME OVER", True, (255, 0, 0))
            screen.blit(game_over, (SCREEN_WIDTH // 2-80, SCREEN_HEIGHT // 2))
            pygame.display.flip()
            pygame.time.wait(3000)
            running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    current_tower_type = "basic"
                    print("Selected: Basic Tower")
                if event.key == pygame.K_2:
                    current_tower_type = "sniper"
                    print("Selected: Sniper Tower")
                if event.key == pygame.K_3:
                    current_tower_type = "rapid"
                    print("Selected: Rapid Tower")

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                grid_x = (mouse_x // GRID_SIZE) * GRID_SIZE + GRID_SIZE // 2
                grid_y = (mouse_y // GRID_SIZE) * GRID_SIZE + GRID_SIZE // 2

                if show_next_wave_button and next_wave_button.collidepoint(mouse_x, mouse_y):
                    wave += 1
                    enemy_per += 2
                    spawned_thiswave = 0
                    spawn_timer = 0
                    wave_in_progress = True
                    show_next_wave_button = False

                    spawn_interval = max(15, spawn_interval - 5)
                    continue

                if event.button == 1:  # Left click
                    if basic_button_rect.collidepoint(mouse_x, mouse_y):
                        current_tower_type = "basic"
                        print("Selected: Basic Tower")
                    elif sniper_button_rect.collidepoint(mouse_x, mouse_y):
                        current_tower_type = "sniper"
                        print("Selected: Sniper Tower")
                    elif rapid_button_rect.collidepoint(mouse_x, mouse_y):
                        current_tower_type = "rapid"
                        print("Selected: Rapid Tower")
                    else:
                        if mouse_y < HEIGHT - TOOLBAR_HEIGHT:
                            grid_x = (mouse_x // GRID_SIZE) * GRID_SIZE + GRID_SIZE // 2
                            grid_y = (mouse_y // GRID_SIZE) * GRID_SIZE + GRID_SIZE // 2
                            if not any(t.x == grid_x and t.y == grid_y for t in towers) and money >= tower_cost:
                                towers.append(Tower(grid_x, grid_y, tower_type=current_tower_type))

                                money -= tower_cost
                elif event.button == 3:
                    for tower in towers:
                        if math.hypot(tower.x - mouse_x, tower.y - mouse_y) < GRID_SIZE:
                            if money >= tower.upgrade_cost:
                                tower.upgrade()
                                money -= tower.upgrade_cost
                                print(f"Tower upgraded to level {tower.level}")
                            break
                
        pygame.draw.rect(screen, (50, 50, 50), (0, HEIGHT - TOOLBAR_HEIGHT, WIDTH, TOOLBAR_HEIGHT))

        button_size = 60
        padding = 20

        basic_button_rect = pygame.Rect(20, HEIGHT - TOOLBAR_HEIGHT + 20, button_size, button_size)
        sniper_button_rect = pygame.Rect(120, HEIGHT - TOOLBAR_HEIGHT + 20, button_size, button_size)
        rapid_button_rect = pygame.Rect(220, HEIGHT - TOOLBAR_HEIGHT + 20, button_size, button_size)

        pygame.draw.rect(screen, (0, 0, 255), basic_button_rect)   
        pygame.draw.rect(screen, (0, 255, 0), sniper_button_rect)  
        pygame.draw.rect(screen, (255, 0, 0), rapid_button_rect) 

        label_font = pygame.font.SysFont(None, 20)
        basic_label = label_font.render("Basic", True, WHITE)
        sniper_label = label_font.render("Sniper", True, WHITE)
        rapid_label = label_font.render("Rapid", True, WHITE)

        # Position text just above each button
        screen.blit(basic_label, (basic_button_rect.centerx - basic_label.get_width() // 2, basic_button_rect.y - 20))
        screen.blit(sniper_label, (sniper_button_rect.centerx - sniper_label.get_width() // 2, sniper_button_rect.y - 20))
        screen.blit(rapid_label, (rapid_button_rect.centerx - rapid_label.get_width() // 2, rapid_button_rect.y - 20))

        if current_tower_type == "basic":
            pygame.draw.rect(screen, (255, 255, 255), basic_button_rect, 3)
        elif current_tower_type == "sniper":
            pygame.draw.rect(screen, (255, 255, 255), sniper_button_rect, 3)
        elif current_tower_type == "rapid":
            pygame.draw.rect(screen, (255, 255, 255), rapid_button_rect, 3)
                
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    start_menu()
    main()
