import random
import pygame
from pygame import Vector2

class basic_ball:
    def __init__(self):
        self.pos = Vector2(470, 600)
        self.r = 10
        self.dir = Vector2(random.randint(-1, 1), -0.5)

    def draw(self, surface):
        pygame.draw.circle(surface, (255, 255, 255), self.pos, self.r)

    def update(self):
        if self.pos.x - self.r < 0:
            self.pos.x = self.r
            self.dir.x *= -1

        if self.pos.x + self.r > 1200:
            self.pos.x = 1200 - self.r
            self.dir.x *= -1

        if self.pos.y - self.r < 0:
            self.pos.y = self.r
            self.dir.y *= -1
        
        if self.pos.y + self.r > 800:
            self.pos.y = 800 - self.r
            self.dir.y *= -1
        
        self.pos += self.dir