import pygame
import sys

# 1. Инициализация
pygame.init()
TILE_SIZE = 40
GRID_WIDTH = 20
GRID_HEIGHT = 15
WIDTH = TILE_SIZE * GRID_WIDTH
HEIGHT = TILE_SIZE * GRID_HEIGHT

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dungeon Run")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24) # Шрифт для текста

# 2. Создаем карту (1 - стена, 0 - пол)
level_map = []
for y in range(GRID_HEIGHT):
    row = []
    for x in range(GRID_WIDTH):
        if x == 0 or x == GRID_WIDTH - 1 or y == 0 or y == GRID_HEIGHT - 1:
            row.append(1) 
        else:
            row.append(0)
    level_map.append(row)

# 3. Создаем Игрока
player_x, player_y = 10, 7
player_hp = 100
player_atk = 25 # Сколько урона бьет игрок

# 4. Создаем Врага (Слизня)
enemy_x, enemy_y = 5, 5
enemy_hp = 50
enemy_atk = 10
enemy_alive = True

# Функция для хода врага
def enemy_turn():
    global player_hp, enemy_x, enemy_y
    if not enemy_alive:
        return

    # Считаем расстояние до игрока
    dx = player_x - enemy_x
    dy = player_y - enemy_y

    # Если враг стоит вплотную (на соседней клетке) - он атакует
    if abs(dx) + abs(dy) == 1:
        player_hp -= enemy_atk
        print(f"Слизень укусил тебя! Твое HP: {player_hp}")
    else:
        # Если далеко - делает шаг в сторону игрока
        step_x, step_y = 0, 0
        if dx > 0: step_x = 1
        elif dx < 0: step_x = -1
        elif dy > 0: step_y = 1
        elif dy < 0: step_y = -1

        # Проверяем, не стена ли там
        if level_map[enemy_y + step_y][enemy_x + step_x] == 0:
            enemy_x += step_x
            enemy_y += step_y

# Главный цикл игры
running = True
while running:
    # Обработка событий (Ход Игрока)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            new_x, new_y = player_x, player_y
            
            if event.key == pygame.K_w: new_y -= 1
            elif event.key == pygame.K_s: new_y += 1
            elif event.key == pygame.K_a: new_x -= 1
            elif event.key == pygame.K_d: new_x += 1
            elif event.key == pygame.K_ESCAPE: running = False
            
            # Проверка границ и стен
            if 0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT:
                if level_map[new_y][new_x] == 0:
                    
                    # Если на пути враг - АТАКУЕМ
                    if enemy_alive and new_x == enemy_x and new_y == enemy_y:
                        enemy_hp -= player_atk
                        print(f"Ты ударил слизня! HP врага: {enemy_hp}")
                        if enemy_hp <= 0:
                            enemy_alive = False
                            print("Слизень побежден!")
                    else:
                        # Если врага нет - просто идем
                        player_x, player_y = new_x, new_y
                        
            # После хода игрока (если он нажал клавишу движения) ходит враг
            if event.key in (pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d):
                enemy_turn()

    # --- ОТРИСОВКА ---
    screen.fill((20, 20, 20))
    
    # Рисуем карту
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            pixel_x = x * TILE_SIZE
            pixel_y = y * TILE_SIZE
            if level_map[y][x] == 1:
                pygame.draw.rect(screen, (100, 100, 100), (pixel_x, pixel_y, TILE_SIZE, TILE_SIZE))
                pygame.draw.rect(screen, (50, 50, 50), (pixel_x, pixel_y, TILE_SIZE, TILE_SIZE), 2)
            else:
                pygame.draw.rect(screen, (40, 40, 40), (pixel_x, pixel_y, TILE_SIZE, TILE_SIZE))
                pygame.draw.rect(screen, (60, 60, 60), (pixel_x, pixel_y, TILE_SIZE, TILE_SIZE), 1)

    # Рисуем врага (Красный квадрат), если он жив
    if enemy_alive:
        enemy_pixel_x = enemy_x * TILE_SIZE
        enemy_pixel_y = enemy_y * TILE_SIZE
        pygame.draw.rect(screen, (255, 50, 50), (enemy_pixel_x, enemy_pixel_y, TILE_SIZE, TILE_SIZE))

    # Рисуем игрока
    player_pixel_x = player_x * TILE_SIZE
    player_pixel_y = player_y * TILE_SIZE
    pygame.draw.rect(screen, (0, 255, 0), (player_pixel_x, player_pixel_y, TILE_SIZE, TILE_SIZE))

    # Рисуем интерфейс (HP игрока)
    hp_text = font.render(f"HP: {player_hp}", True, (255, 255, 255))
    screen.blit(hp_text, (10, 10)) # Выводим текст в левом верхнем углу

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()