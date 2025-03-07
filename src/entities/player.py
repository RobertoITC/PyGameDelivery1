import pygame
from entities.bullet import Bullet


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 5
        self.sprite_path = pygame.image.load("../assets/images/player.png")

    def shoot(self):
        return Bullet(self.x + 20, self.y)

    def move(self, keys, width):
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < width - 50:
            self.x += self.speed

    def draw(self, screen):
        screen.blit(self.sprite_path, (self.x, self.y))
