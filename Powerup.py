import pygame
from pygame import Vector2

class Powerups:
    def __init__(self, screen_w, screen_h, enemy):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.pos = Vector2(enemy.pos.x + enemy.w/2, enemy.pos.y + enemy.h)
        self.speed = 4
        self.r = self.screen_w/150

    def draw(self, screen, IMG):
        screen.blit(IMG, (self.pos.x - self.r, self.pos.y - self.r))

    def update(self):
        self.pos.y += self.speed

class More_Balls(Powerups):
    def __init__(self, screen_w, screen_h, enemy_pos):
        super().__init__(screen_w, screen_h, enemy_pos)
        self.IMG = pygame.transform.smoothscale(pygame.image.load('Sprites/circle.png'), (self.r*2, self.r*2))

class Stronger_Ball(Powerups):
    def __init__(self, screen_w, screen_h, enemy_pos):
        super().__init__(screen_w, screen_h, enemy_pos)
        self.IMG = pygame.transform.smoothscale(pygame.image.load('Sprites/polygon.png'), (self.r*2, self.r*2))

class Ghost_Ball(Powerups):
    def __init__(self, screen_w, screen_h, enemy_pos):
        super().__init__(screen_w, screen_h, enemy_pos)
        self.IMG = pygame.transform.smoothscale(pygame.image.load('Sprites/triangle.png'), (self.r*2, self.r*2))