import pygame
import sys
import random

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
font = pygame.font.SysFont("Arial", 20)
big_font = pygame.font.SysFont("Arial", 40)

game_state = "MENU"
player_char = ""
player_color = (0, 255, 0)

# Функция для отрисовки полоски здоровья
def draw_hp_bar(surface, x, y, current_hp, max_hp):
    bar_width = TILE_SIZE
    bar_height = 6
    # Позиция над объектом
    bar_x = x * TILE_SIZE
    bar_y = y * TILE_SIZE - 10 
    
    # Задний фон (красный - пустое здоровье)
    pygame.draw.rect(surface, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))
    
    # Текущее здоровье (зеленое)
    hp_ratio = max(0, current_hp / max_hp) # Защита от отрицательного значения
    pygame.draw.rect(surface, (0, 255, 0), (bar_x, bar_y, bar_width * hp_ratio, bar_height))
    
    # Рамка для красоты
    pygame.draw.rect(surface, (0, 0, 0), (bar_x, bar_y, bar_width, bar_height), 1)

def generate_map():
    level_map = []
    for y in range(GRID_HEIGHT):
        row = []
        for x in range(GRID_WIDTH):
            if x == 0 or x == GRID_WIDTH - 1 or y == 0 or y == GRID_HEIGHT - 1:
                row.append(1) 
            else:
                if random.random() < 0.15:
                    row.append(1)
                else:
                    row.append(0)
        level_map.append(row)
    return level_map

running = True
while running:
    
    # МЕНЮ
    if game_state == "MENU":
        screen.fill((20, 20, 20))
        title = big_font.render("Выбери своего героя", True, (255, 255, 255))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))
        
        text1 = font.render("1 - Паук (Быстрый, 50 HP, Урон 20)", True, (255, 50, 50))
        text2 = font.render("2 - Гарри (Маг, 70 HP, Урон 30)", True, (150, 50, 255))
        text3 = font.render("3 - Ты сам (Танк, 120 HP, Урон 15)", True, (0, 255, 0))
        
        screen.blit(text1, (WIDTH//2 - text1.get_width()//2, 250))
        screen.blit(text2, (WIDTH//2 - text2.get_width()//2, 300))
        screen.blit(text3, (WIDTH//2 - text3.get_width()//2, 350))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    player_char, player_color = "Паук", (255, 50, 50)
                    player_hp, player_max_hp, player_atk = 50, 50, 20
                elif event.key == pygame.K_2:
                    player_char, player_color = "Гарри", (150, 50, 255)
                    player_hp, player_max_hp, player_atk = 70, 70, 30
                elif event.key == pygame.K_3:
                    player_char, player_color = "Я сам", (0, 255, 0)
                    player_hp, player_max_hp, player_atk = 120, 120, 15
                else:
                    continue 
                
                level_map = generate_map()
                player_x, player_y = 10, 7
                level_map[player_y][player_x] = 0
                
                enemy_x, enemy_y = 5, 5
                level_map[enemy_y][enemy_x] = 0
                enemy_hp = 50
                enemy_max_hp = 50 # Добавили максимальное HP для врага
                enemy_alive = True
                
                potion_x, potion_y = 15, 10
                potion_alive = True
                level_map[potion_y][potion_x] = 0
                
                buff_x, buff_y = 3, 12
                buff_alive = True
                level_map[buff_y][buff_x] = 0

                sword_x, sword_y = 16, 3
                sword_alive = True
                level_map[sword_y][sword_x] = 0
                
                player_speed_boost = 0
                has_sword = False 
                game_state = "PLAYING"

    # ИГРА
    elif game_state == "PLAYING":
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            
            if event.type == pygame.KEYDOWN:
                new_x, new_y = player_x, player_y
                player_moved = False
                
                if event.key == pygame.K_w: new_y -= 1; player_moved = True
                elif event.key == pygame.K_s: new_y += 1; player_moved = True
                elif event.key == pygame.K_a: new_x -= 1; player_moved = True
                elif event.key == pygame.K_d: new_x += 1; player_moved = True
                elif event.key == pygame.K_ESCAPE: running = False
                
                if 0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT:
                    if level_map[new_y][new_x] == 0:
                        if enemy_alive and new_x == enemy_x and new_y == enemy_y:
                            enemy_hp -= player_atk
                            if enemy_hp <= 0: enemy_alive = False
                        else:
                            player_x, player_y = new_x, new_y
                            
                            if potion_alive and player_x == potion_x and player_y == potion_y:
                                player_hp += 30
                                if player_hp > player_max_hp: player_hp = player_max_hp
                                potion_alive = False
                            
                            if buff_alive and player_x == buff_x and player_y == buff_y:
                                player_speed_boost = 3
                                buff_alive = False

                            if sword_alive and player_x == sword_x and player_y == sword_y:
                                has_sword = True
                                player_atk += 25 
                                sword_alive = False
                            
                if player_moved:
                    if player_speed_boost > 0:
                        player_speed_boost -= 1 
                    else:
                        if enemy_alive:
                            dx = player_x - enemy_x
                            dy = player_y - enemy_y
                            if abs(dx) + abs(dy) == 1: 
                                player_hp -= 10
                            else: 
                                step_x, step_y = 0, 0
                                if dx > 0: step_x = 1
                                elif dx < 0: step_x = -1
                                elif dy > 0: step_y = 1
                                elif dy < 0: step_y = -1
                                if level_map[enemy_y + step_y][enemy_x + step_x] == 0:
                                    enemy_x += step_x
                                    enemy_y += step_y

        # ОТРИСОВКА
        screen.fill((20, 20, 20))
        
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

        if potion_alive:
            pygame.draw.rect(screen, (0, 150, 255), (potion_x * TILE_SIZE, potion_y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        if buff_alive:
            pygame.draw.rect(screen, (255, 255, 0), (buff_x * TILE_SIZE, buff_y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        if sword_alive:
            pygame.draw.rect(screen, (220, 220, 220), (sword_x * TILE_SIZE, sword_y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            
        # Отрисовка Врага и его HP
        if enemy_alive:
            pygame.draw.rect(screen, (255, 50, 50), (enemy_x * TILE_SIZE, enemy_y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            draw_hp_bar(screen, enemy_x, enemy_y, enemy_hp, enemy_max_hp) # Рисуем полоску врага

        # Отрисовка Игрока и его HP
        pygame.draw.rect(screen, player_color, (player_x * TILE_SIZE, player_y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        draw_hp_bar(screen, player_x, player_y, player_hp, player_max_hp) # Рисуем полоску игрока

        # Интерфейс (оставили только урон и бонусы)
        info_text = font.render(f"Урон: {player_atk}", True, (255, 255, 255))
        screen.blit(info_text, (10, 10))
        
        if has_sword:
            sword_text = font.render("В руках: Меч (+25)", True, (220, 220, 220))
            screen.blit(sword_text, (10, 35))

        if player_speed_boost > 0:
            speed_text = font.render(f"Speed Boost: {player_speed_boost}", True, (255, 255, 0))
            screen.blit(speed_text, (10, 60))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()