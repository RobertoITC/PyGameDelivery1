# enemy.py
import pygame

class Enemy:
    def __init__(self, x, y, sprite, speed=2, direction=1, chain_id=0, index_in_chain=0, behavior="normal", health=1):
        self.x = x
        self.y = y
        self.sprite = sprite
        self.image = pygame.image.load(sprite)
        self.health = health
        self.speed = speed
        self.direction = direction  # 1 = right, -1 = left
        self.chain_id = chain_id
        self.index_in_chain = index_in_chain
        self.behavior = behavior

    def move(self, screen_width, step_down=20):


        # Typical “centipede” movement: horizontal + bounce
        self.x += self.speed * self.direction

        # Bounce on edges
        if self.x < 0:
            self.x = 0
            self.direction *= -1
            self.y += step_down
        elif self.x + self.image.get_width() > screen_width:
            self.x = screen_width - self.image.get_width()
            self.direction *= -1
            self.y += step_down

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))