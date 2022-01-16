from pygame import Vector2
import pygame

class player:
    def __init__(self):
        self.pos = Vector2(430, 700)
        self.w = 200
        self.h = 15

    def walk(self, direction):
        self.xspeed = direction
        self.pos.x += self.xspeed

    def draw(self, surface):
        itself = pygame.Rect(self.pos.x, self.pos.y, self.w, self.h)
        pygame.draw.rect(surface, (180, 0, 0), itself)