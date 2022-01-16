from pygame import Vector2
import pygame

class basic_enemy:
    def __init__(self):
        self.pos = Vector2(400, 100)
        self.w = 100
        self.h = 30

    def draw(self, surface):
        pygame.draw.rect(surface, (200, 200, 255), (self.pos.x, self.pos.y, self.w, self.h))
