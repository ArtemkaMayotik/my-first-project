import pygame
import sys
import random

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
name_font = pygame.font.SysFont("Arial", 14, bold=True)

try:
    player_img = pygame.image.load("player.png").convert_alpha()
    player_img = pygame.transform.scale(player_img, (TILE_SIZE * 2, TILE_SIZE * 2))
    has_player_img = True
except Exception as e:
    has_player_img = False

try:
    slime_img = pygame.image.load("slime.png").convert_alpha()
    slime_img = pygame.transform.scale(slime_img, (TILE_SIZE * 2, TILE_SIZE * 2))
    has_slime_img = True
except Exception as e:
    has_slime_img = False

try:
    rat_img = pygame.image.load("rat.png").convert_alpha()
    rat_img = pygame.transform.scale(rat_img, (TILE_SIZE * 2, TILE_SIZE * 2))
    has_rat_img = True
except Exception as e:
    has_rat_img = False

game_state = "MENU"
player_char = ""
player_color = (0, 255, 0)
portal_alive = False
enemy_type = "slime"

def draw_hp_bar(surface, x, y, current_hp, max_hp):
    bar_width = TILE_SIZE
    bar_height = 6
    bar_x = x * TILE_SIZE
    bar_y = y * TILE_SIZE - 15
    pygame.draw.rect(surface, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))
    hp_ratio = max(0, current_hp / max_hp) 
    pygame.draw.rect(surface, (0, 255, 0), (bar_x, bar_y, bar_width * hp_ratio, bar_height))
    pygame.draw.rect(surface, (0, 0, 0), (bar_x, bar_y, bar_width, bar_height), 1)

def draw_eyes(surface, x, y, target_x, target_y):
    cx = x * TILE_SIZE + TILE_SIZE // 2
    cy = y * TILE_SIZE + TILE_SIZE // 2
    dx = 1 if target_x > x else (-1 if target_x < x else 0)
    dy = 1 if target_y > y else (-1 if target_y < y else 0)
    pygame.draw.circle(surface, (255, 255, 255), (cx - 8, cy - 5), 5)
    pygame.draw.circle(surface, (255, 255, 255), (cx + 8, cy - 5), 5)
    pygame.draw.circle(surface, (0, 0, 0), (cx - 8 + dx*2, cy - 5 + dy*2), 2)
    pygame.draw.circle(surface, (0, 0, 0), (cx + 8 + dx*2, cy - 5 + dy*2), 2)

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

def setup_level():
    global level_map, player_x, player_y, enemy_x, enemy_y, enemy_hp, enemy_max_hp, enemy_alive, enemy_stunned, enemy_atk, enemy_speed, enemy_color, enemy_type
    global potion_x, potion_y, potion_alive, buff_x, buff_y, buff_alive, sword_x, sword_y, sword_alive
    global barrels, spikes, portal_alive, chest_x, chest_y, chest_alive
    
    level_map = generate_map()
    player_x, player_y = 10, 7
    level_map[player_y][player_x] = 0
    
    enemy_type = random.choice(["slime", "rat"])
    if enemy_type == "slime":
        enemy_hp, enemy_max_hp = 50, 50
        enemy_atk = 10
        enemy_speed = 1
        enemy_color = (255, 50, 50)
    else:
        enemy_hp, enemy_max_hp = 30, 30
        enemy_atk = 5
        enemy_speed = 2
        enemy_color = (160, 82, 45)

    enemy_x, enemy_y = 5, 5
    level_map[enemy_y][enemy_x] = 0
    enemy_alive = True
    enemy_stunned = 0
    
    potion_x, potion_y = 15, 10
    potion_alive = True
    level_map[potion_y][potion_x] = 0
    
    buff_x, buff_y = 3, 12
    buff_alive = True
    level_map[buff_y][buff_x] = 0

    sword_x, sword_y = 16, 3
    sword_alive = True
    level_map[sword_y][sword_x] = 0
    
    barrels = []
    for _ in range(10):
        bx, by = random.randint(1, GRID_WIDTH-2), random.randint(1, GRID_HEIGHT-2)
        if level_map[by][bx] == 0 and (bx, by) != (player_x, player_y) and (bx, by) != (enemy_x, enemy_y):
            barrels.append([bx, by])
            
    spikes = []
    for _ in range(10):
        sx, sy = random.randint(1, GRID_WIDTH-2), random.randint(1, GRID_HEIGHT-2)
        if level_map[sy][sx] == 0 and (sx, sy) != (player_x, player_y) and (sx, sy) != (enemy_x, enemy_y) and [sx, sy] not in barrels:
            spikes.append([sx, sy])

    chest_x, chest_y = random.randint(1, GRID_WIDTH-2), random.randint(1, GRID_HEIGHT-2)
    if level_map[chest_y][chest_x] == 0 and (chest_x, chest_y) != (player_x, player_y) and (chest_x, chest_y) != (enemy_x, enemy_y) and [chest_x, chest_y] not in barrels and [chest_x, chest_y] not in spikes:
        chest_alive = True
    else:
        chest_alive = False
            
    portal_alive = False

running = True
while running:
    if game_state == "MENU":
        screen.fill((20, 20, 20))
        title = big_font.render("Выбери своего героя", True, (255, 255, 255))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))
        
        text1 = font.render("1 - Паук (Space: Паутина)", True, (200, 0, 0))
        text2 = font.render("2 - Гарри (Space: Оглушение)", True, (150, 50, 255))
        text3 = font.render("3 - Ты сам (Лечение за убийство)", True, (0, 255, 0))
        
        screen.blit(text1, (WIDTH//2 - text1.get_width()//2, 250))
        screen.blit(text2, (WIDTH//2 - text2.get_width()//2, 300))
        screen.blit(text3, (WIDTH//2 - text3.get_width()//2, 350))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    player_char, player_color = "Паук", (200, 0, 0)
                    player_hp, player_max_hp, player_atk = 50, 50, 20
                elif event.key == pygame.K_2:
                    player_char, player_color = "Гарри", (150, 50, 255)
                    player_hp, player_max_hp, player_atk = 70, 70, 30
                elif event.key == pygame.K_3:
                    player_char, player_color = "Я сам", (0, 255, 0)
                    player_hp, player_max_hp, player_atk = 120, 120, 15
                else:
                    continue 
                
                inventory_potions = 0
                player_speed_boost = 0
                has_sword = False 
                setup_level()
                game_state = "PLAYING"

    elif game_state == "PLAYING":
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            
            if event.type == pygame.KEYDOWN:
                new_x, new_y = player_x, player_y
                player_moved = False
                enemy_attacked = False
                
                if event.key == pygame.K_w: new_y -= 1; player_moved = True
                elif event.key == pygame.K_s: new_y += 1; player_moved = True
                elif event.key == pygame.K_a: new_x -= 1; player_moved = True
                elif event.key == pygame.K_d: new_x += 1; player_moved = True
                elif event.key == pygame.K_ESCAPE: running = False
                
                elif event.key == pygame.K_e:
                    if inventory_potions > 0 and player_hp < player_max_hp:
                        inventory_potions -= 1
                        player_hp += 30
                        if player_hp > player_max_hp: player_hp = player_max_hp
                        player_moved = True
                
                elif event.key == pygame.K_SPACE and enemy_alive:
                    dist = abs(player_x - enemy_x) + abs(player_y - enemy_y)
                    
                    if player_char == "Паук" and dist == 2:
                        enemy_hp -= player_atk
                        enemy_attacked = True
                        if enemy_hp <= 0: 
                            enemy_alive = False
                            portal_alive = True
                            portal_x, portal_y = enemy_x, enemy_y
                            
                    elif player_char == "Гарри" and dist == 2:
                        enemy_stunned = 1
                        enemy_attacked = True
                
                if 0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT:
                    if level_map[new_y][new_x] == 0:
                        if [new_x, new_y] in barrels:
                            barrels.remove([new_x, new_y])
                            if random.random() < 0.5:
                                inventory_potions += 1
                            player_moved = True
                            
                        elif enemy_alive and new_x == enemy_x and new_y == enemy_y:
                            enemy_hp -= player_atk
                            enemy_attacked = True
                            if enemy_hp <= 0: 
                                enemy_alive = False
                                portal_alive = True
                                portal_x, portal_y = enemy_x, enemy_y
                                if player_char == "Я сам":
                                    player_hp += 20
                                    if player_hp > player_max_hp: player_hp = player_max_hp
                        else:
                            player_x, player_y = new_x, new_y
                            
                            if portal_alive and player_x == portal_x and player_y == portal_y:
                                setup_level()
                            else:
                                if [player_x, player_y] in spikes:
                                    player_hp -= 15
                                
                                if potion_alive and player_x == potion_x and player_y == potion_y:
                                    inventory_potions += 1
                                    potion_alive = False
                                
                                if buff_alive and player_x == buff_x and player_y == buff_y:
                                    player_speed_boost = 3
                                    buff_alive = False

                                if sword_alive and player_x == sword_x and player_y == sword_y:
                                    has_sword = True
                                    player_atk += 25 
                                    sword_alive = False
                                    
                                if chest_alive and player_x == chest_x and player_y == chest_y:
                                    player_max_hp += 20
                                    player_hp += 20
                                    chest_alive = False
                            
                if player_moved or enemy_attacked:
                    if player_speed_boost > 0:
                        player_speed_boost -= 1 
                    else:
                        if enemy_alive:
                            if enemy_stunned > 0:
                                enemy_stunned -= 1
                            else:
                                for _ in range(enemy_speed):
                                    dx = player_x - enemy_x
                                    dy = player_y - enemy_y
                                    if abs(dx) + abs(dy) == 1: 
                                        player_hp -= enemy_atk
                                        break
                                    else: 
                                        step_x, step_y = 0, 0
                                        if dx > 0: step_x = 1
                                        elif dx < 0: step_x = -1
                                        elif dy > 0: step_y = 1
                                        elif dy < 0: step_y = -1
                                        if level_map[enemy_y + step_y][enemy_x + step_x] == 0:
                                            enemy_x += step_x
                                            enemy_y += step_y
                                        
                if player_hp <= 0:
                    game_state = "GAME_OVER"

        screen.fill((20, 20, 20))
        
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                pixel_x = x * TILE_SIZE
                pixel_y = y * TILE_SIZE
                if level_map[y][x] == 1:
                    shade = (x * 7 + y * 13) % 10 - 5
                    wall_col = (60 + shade, 60 + shade, 70 + shade)
                    pygame.draw.rect(screen, wall_col, (pixel_x, pixel_y, TILE_SIZE, TILE_SIZE))
                    pygame.draw.line(screen, (40, 40, 50), (pixel_x, pixel_y + 20), (pixel_x + TILE_SIZE, pixel_y + 20), 2)
                    pygame.draw.line(screen, (40, 40, 50), (pixel_x + 20, pixel_y), (pixel_x + 20, pixel_y + 20), 2)
                    pygame.draw.line(screen, (40, 40, 50), (pixel_x + 10, pixel_y + 20), (pixel_x + 10, pixel_y + TILE_SIZE), 2)
                    pygame.draw.line(screen, (40, 40, 50), (pixel_x + 30, pixel_y + 20), (pixel_x + 30, pixel_y + TILE_SIZE), 2)
                    pygame.draw.rect(screen, (30, 30, 40), (pixel_x, pixel_y, TILE_SIZE, TILE_SIZE), 1)
                else:
                    floor_color = (25, 25, 30) if (x + y) % 2 == 0 else (30, 30, 35)
                    pygame.draw.rect(screen, floor_color, (pixel_x, pixel_y, TILE_SIZE, TILE_SIZE))
                    
                    shadow_col = (15, 15, 20)
                    if y > 0 and level_map[y-1][x] == 1:
                        pygame.draw.rect(screen, shadow_col, (pixel_x, pixel_y, TILE_SIZE, 8))
                    if y < GRID_HEIGHT - 1 and level_map[y+1][x] == 1:
                        pygame.draw.rect(screen, shadow_col, (pixel_x, pixel_y + TILE_SIZE - 8, TILE_SIZE, 8))
                    if x > 0 and level_map[y][x-1] == 1:
                        pygame.draw.rect(screen, shadow_col, (pixel_x, pixel_y, 8, TILE_SIZE))
                    if x < GRID_WIDTH - 1 and level_map[y][x+1] == 1:
                        pygame.draw.rect(screen, shadow_col, (pixel_x + TILE_SIZE - 8, pixel_y, 8, TILE_SIZE))
                        
                    if (x * 3 + y * 7) % 11 == 0:
                        pygame.draw.line(screen, (20, 20, 25), (pixel_x + 10, pixel_y + 10), (pixel_x + 20, pixel_y + 30), 1)

        for sx, sy in spikes:
            pygame.draw.rect(screen, (60, 60, 60), (sx * TILE_SIZE, sy * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            pygame.draw.polygon(screen, (200, 200, 200), [(sx*TILE_SIZE+5, sy*TILE_SIZE+35), (sx*TILE_SIZE+15, sy*TILE_SIZE+15), (sx*TILE_SIZE+25, sy*TILE_SIZE+35)])
            pygame.draw.polygon(screen, (200, 200, 200), [(sx*TILE_SIZE+15, sy*TILE_SIZE+35), (sx*TILE_SIZE+25, sy*TILE_SIZE+15), (sx*TILE_SIZE+35, sy*TILE_SIZE+35)])

        for bx, by in barrels:
            pygame.draw.ellipse(screen, (10, 10, 15), (bx * TILE_SIZE + 5, by * TILE_SIZE + 25, 30, 10))
            pygame.draw.rect(screen, (139, 69, 19), (bx * TILE_SIZE, by * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            pygame.draw.rect(screen, (80, 40, 10), (bx * TILE_SIZE, by * TILE_SIZE, TILE_SIZE, TILE_SIZE), 2)

        if chest_alive:
            pygame.draw.ellipse(screen, (10, 10, 15), (chest_x * TILE_SIZE + 5, chest_y * TILE_SIZE + 25, 30, 10))
            pygame.draw.rect(screen, (255, 215, 0), (chest_x * TILE_SIZE, chest_y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            pygame.draw.rect(screen, (139, 69, 19), (chest_x * TILE_SIZE + 15, chest_y * TILE_SIZE + 15, 10, 10))

        if potion_alive:
            pygame.draw.rect(screen, (0, 150, 255), (potion_x * TILE_SIZE, potion_y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        if buff_alive:
            pygame.draw.rect(screen, (255, 255, 0), (buff_x * TILE_SIZE, buff_y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        if sword_alive:
            pygame.draw.rect(screen, (220, 220, 220), (sword_x * TILE_SIZE, sword_y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            
        if portal_alive:
            pygame.draw.rect(screen, (200, 0, 255), (portal_x * TILE_SIZE, portal_y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            
        if enemy_alive:
            pygame.draw.ellipse(screen, (10, 10, 15), (enemy_x * TILE_SIZE + 5, enemy_y * TILE_SIZE + 25, 30, 10))
            
            if enemy_type == "slime" and has_slime_img:
                screen.blit(slime_img, (enemy_x * TILE_SIZE - TILE_SIZE // 2, enemy_y * TILE_SIZE - TILE_SIZE // 2))
            elif enemy_type == "rat" and has_rat_img:
                screen.blit(rat_img, (enemy_x * TILE_SIZE - TILE_SIZE // 2, enemy_y * TILE_SIZE - TILE_SIZE // 2))
            else:
                pygame.draw.rect(screen, enemy_color, (enemy_x * TILE_SIZE, enemy_y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                draw_eyes(screen, enemy_x, enemy_y, player_x, player_y)
                
            draw_hp_bar(screen, enemy_x, enemy_y, enemy_hp, enemy_max_hp)
            
            if enemy_stunned > 0:
                pygame.draw.circle(screen, (255, 255, 0), (enemy_x * TILE_SIZE + 20, enemy_y * TILE_SIZE - 20), 5)

        pygame.draw.ellipse(screen, (10, 10, 15), (player_x * TILE_SIZE + 5, player_y * TILE_SIZE + 25, 30, 10))
        
        if has_player_img:
            screen.blit(player_img, (player_x * TILE_SIZE - TILE_SIZE // 2, player_y * TILE_SIZE - TILE_SIZE // 2))
        else:
            pygame.draw.rect(screen, player_color, (player_x * TILE_SIZE, player_y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            draw_eyes(screen, player_x, player_y, enemy_x, enemy_y)
            
        draw_hp_bar(screen, player_x, player_y, player_hp, player_max_hp)
        
        name_text = name_font.render(player_char, True, (255, 255, 255))
        screen.blit(name_text, (player_x * TILE_SIZE + TILE_SIZE//2 - name_text.get_width()//2, player_y * TILE_SIZE - 30))

        info_text = font.render(f"Урон: {player_atk} | Зелья (E): {inventory_potions}", True, (255, 255, 255))
        screen.blit(info_text, (10, 10))
        
        if has_sword:
            sword_text = font.render("В руках: Меч (+25)", True, (220, 220, 220))
            screen.blit(sword_text, (10, 35))

        if player_speed_boost > 0:
            speed_text = font.render(f"Speed Boost: {player_speed_boost}", True, (255, 255, 0))
            screen.blit(speed_text, (10, 60))
            
        hint = font.render("Space - способность | E - выпить зелье", True, (150, 150, 150))
        screen.blit(hint, (10, HEIGHT - 30))
        
    elif game_state == "GAME_OVER":
        screen.fill((50, 0, 0))
        go_text = big_font.render("ВЫ ПОГИБЛИ", True, (255, 0, 0))
        screen.blit(go_text, (WIDTH//2 - go_text.get_width()//2, HEIGHT//2 - 50))
        
        restart_text = font.render("Нажмите R, чтобы начать заново", True, (255, 255, 255))
        screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 20))

        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game_state = "MENU"

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()