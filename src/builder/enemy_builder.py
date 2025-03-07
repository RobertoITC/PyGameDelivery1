import random
import pygame
from src.entities.enemy import Enemy


class EnemyBuilder:
    def __init__(self):
        self.reset()

    def reset(self):
        self.enemy = Enemy(0, 0, "../assets/images/enemy.png")

    def set_position(self):
        self.enemy.x = random.randint(50, 750)
        self.enemy.y = random.randint(50, 200)

    def set_sprite(self, sprite_path):
        self.enemy.sprite = sprite_path
        self.enemy.image = pygame.image.load(sprite_path)

    def set_speed(self, speed):
        self.enemy.speed = speed

    def get_enemy(self):
        enemy = self.enemy
        self.reset()
        return enemy
