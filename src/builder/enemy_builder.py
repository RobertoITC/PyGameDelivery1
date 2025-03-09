# enemy_builder.py
import pygame
from src.entities.enemy import Enemy

class EnemyBuilder:
    def __init__(self):
        self.reset()

    def reset(self):
        # Crea un enemigo por defecto (valores genéricos)
        self.enemy = Enemy(0, 0, "../assets/images/enemy.png", speed=2)
        self.enemy.is_head = False  # Atributo para diferenciar

    def set_sprite(self, sprite_path):
        self.enemy.sprite = sprite_path
        self.enemy.image = pygame.image.load(sprite_path)

    def set_speed(self, speed):
        self.enemy.speed = speed

    def set_is_head(self, is_head):
        self.enemy.is_head = is_head

    def set_position(self, x, y):
        self.enemy.x = x
        self.enemy.y = y

    def set_behavior(self, behavior):
        self.enemy.behavior = behavior

    def set_health(self, health):
        self.enemy.health = health

    def set_bullet_cooldown(self, bullet_cooldown):
        self.enemy.bullet_cooldown = bullet_cooldown

    def get_enemy(self):
        # Devuelve la instancia creada
        enemy = self.enemy
        # Resetea para la siguiente construcción
        self.reset()
        return enemy