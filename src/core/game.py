import pygame
pygame.init()
import random
from src.core.config import Config
from src.entities.player import Player
from src.builder.director import EnemyDirector
from src.builder.enemy_builder import EnemyBuilder
from src.utils.collision import check_collision
from src.utils.obstacle import Obstacle

level = 1
font = pygame.font.SysFont(None, 36)


def spawn_centipede(level, enemies, director, builder):

    base_speed = 2 + (level - 1)
    chain_id = 1

    num_segments = 6
    start_x = 50
    start_y = 50

    # Spawn head
    head = director.construct_enemy(builder, "centipede_head")
    head.x = start_x
    head.y = start_y
    head.chain_id = chain_id
    head.index_in_chain = 0
    head.speed = base_speed
    enemies.append(head)

    for i in range(1, num_segments):
        body_segment = director.construct_enemy(builder, "centipede_body")
        body_segment.x = start_x + i * 50
        body_segment.y = start_y
        body_segment.chain_id = chain_id
        body_segment.index_in_chain = i
        body_segment.speed = base_speed
        enemies.append(body_segment)

def start_new_level(level, enemies, obstacles, player, director, builder):

    obstacles.clear()
    num_obstacles = 5 + (level - 1)
    new_obs = spawn_random_obstacles(num_obstacles, WIDTH, HEIGHT, player.y)
    obstacles.extend(new_obs)

    enemies.clear()

    spawn_centipede(level, enemies, director, builder)

def spawn_random_obstacles(num_obstacles, screen_width, screen_height, player_y):

    obstacles_list = []

    obs_width = 100
    obs_height = 20
    color = (200, 100, 50)

    for _ in range(num_obstacles):
        x = random.randint(0, screen_width - obs_width)

        max_y = max(0, player_y - obs_height - 20)
        y = random.randint(0, max_y)

        obstacle = Obstacle(x, y, obs_width, obs_height, color)
        obstacles_list.append(obstacle)

    return obstacles_list

# Configuration
config = Config()
WIDTH, HEIGHT = config.get('WIDTH'), config.get('HEIGHT')
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invader")

# Jugador
def select_player(player_type):
    if player_type == "speedy":
        return Player(WIDTH//2, HEIGHT-80, speed=12, health=2, bullet_cooldown=200)
    elif player_type == "tank":
        return Player(WIDTH//2, HEIGHT-80, speed=8, health=5, bullet_cooldown=400)
    else:
        return Player(WIDTH//2, HEIGHT-80,speed=3, health=5, bullet_cooldown=400)

chosen_type = "speedy"  # o "tank"
player = select_player(chosen_type)

score = 0

obstacles = spawn_random_obstacles(num_obstacles=5,
                                   screen_width=WIDTH,
                                   screen_height=HEIGHT,
                                   player_y=player.y)

# Enemigos con Builder

start_x = 50
start_y = 50
director = EnemyDirector()
builder = EnemyBuilder()

enemies = []

chain_id = 1
num_segments = 6

head = director.construct_enemy(builder, "centipede_head")
head.x = 50
head.y = 50
head.chain_id = chain_id
head.index_in_chain = 0
enemies.append(head)

for i in range(1, num_segments):
    body_segment = director.construct_enemy(builder, "centipede_body")
    body_segment.x = 50 + i * 50
    body_segment.y = 50
    body_segment.chain_id = chain_id
    body_segment.index_in_chain = i
    enemies.append(body_segment)
bullets = []
last_shot_time = 0
bullet_cooldown = 300

enemy_speed = 1
enemy_spawn_timer = 0

# En game.py, antes del loop principal


def split_chain(enemies, hit_enemy):
    """
    Removes 'hit_enemy' from the list, and any segments
    behind it become a new chain (if you want a new head).
    """
    old_chain_id = hit_enemy.chain_id
    hit_index = hit_enemy.index_in_chain
    hit_enemy.health -= 1
    if hit_enemy.health <= 0:
        enemies.remove(hit_enemy)






    behind_segments = [e for e in enemies
                       if e.chain_id == old_chain_id and e.index_in_chain > hit_index]

    if behind_segments:
        new_chain_id = max(e.chain_id for e in enemies) + 1  # or just random
        behind_segments_sorted = sorted(behind_segments, key=lambda e: e.index_in_chain)
        for i, seg in enumerate(behind_segments_sorted):
            seg.chain_id = new_chain_id
            seg.index_in_chain = i

        front_segments = [e for e in enemies
                          if e.chain_id == old_chain_id and e.index_in_chain < hit_index]
        front_segments_sorted = sorted(front_segments, key=lambda e: e.index_in_chain)
        for i, seg in enumerate(front_segments_sorted):
            seg.index_in_chain = i


def handle_bullet_collisions(enemies, bullets):
    for bullet in bullets[:]:
        bullet_rect = pygame.Rect(bullet.x, bullet.y, bullet.width, bullet.height)
        for enemy in enemies[:]:
            enemy_rect = pygame.Rect(enemy.x, enemy.y,
                                     enemy.image.get_width(), enemy.image.get_height())
            if bullet_rect.colliderect(enemy_rect):
                bullets.remove(bullet)
                split_chain(enemies, enemy)
                break


start_new_level(level, enemies, obstacles, player, director, builder)

running = True
while running:


    pygame.time.delay(30)
    screen.fill((0, 0, 0))


    text_surface = font.render(f"Level: {level}", True, (255, 255, 255))
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 40))  # Lo dibujas un poco más abajo que el nivel
    screen.blit(text_surface, (10, 10))


    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Controles
    keys = pygame.key.get_pressed()
    player.move(keys, WIDTH)
    current_time = pygame.time.get_ticks()


    if keys[pygame.K_SPACE] and (current_time - last_shot_time > bullet_cooldown):
        bullets.append(player.shoot())
        last_shot_time = current_time

    for bullet in bullets[:]:
        if bullet.y < 0:
            bullets.remove(bullet)

    for enemy in enemies[:]:
        if check_collision(enemy, player):
            running = False

    for bullet in bullets[:]:
        bullet.move()

        bullet_rect = pygame.Rect(bullet.x, bullet.y, bullet.width, bullet.height)

        for obs in obstacles:
            if bullet_rect.colliderect(obs.rect):
                bullets.remove(bullet)

                break

    for enemy in enemies:
        enemy.move(WIDTH)

        for obs in obstacles:
            enemy_rect = pygame.Rect(enemy.x, enemy.y,
                                     enemy.image.get_width(), enemy.image.get_height())
            if enemy_rect.colliderect(obs.rect):

                enemy.direction *= -1
                enemy.y += 20


    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if check_collision(bullet, enemy):
                handle_bullet_collisions(enemies, bullets)

                score += 10

                break

    if not enemies:
        level += 1
        start_new_level(level, enemies, obstacles, player, director, builder)



    '''enemy_spawn_timer += 1
    enemy_types = ["normal", "fast", "strong"]
    if enemy_spawn_timer > 30:  # Cada cierto tiempo puede ser 100 al principio
        random_enemy_type = random.choice(enemy_types)

        enemies.append(director.construct_enemy(builder, random_enemy_type))
        enemy_spawn_timer = 0'''

    enemy_spawn_timer += 0.1
    enemy_types = ["normal", "fast", "strong"]  # Agrega más si quieres

    if enemy_spawn_timer > 60:
        random_enemy_type = random.choice(enemy_types)
        new_enemy = director.construct_enemy(builder, random_enemy_type)
        new_enemy.x = random.randint(0, WIDTH - new_enemy.image.get_width())
        new_enemy.y = 0
        enemies.append(new_enemy)
        enemy_spawn_timer = 0

    player.draw(screen)

    for enemy in enemies:
        enemy.draw(screen)
    for bullet in bullets:
        bullet.draw(screen)
    for obs in obstacles:
        obs.draw(screen)


    pygame.display.update()


pygame.quit()




