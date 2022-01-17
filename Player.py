from pygame import Vector2
import pygame

class player:
    def __init__(self, screen_w, screen_h):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.pos = Vector2((screen_w - (3*self.screen_w)/5), self.screen_h - 100)
        self.w = 200
        self.h = 15

    def walk(self, direction):
        self.xspeed = direction
        self.pos.x += self.xspeed

    def draw(self, surface):
        itself = pygame.Rect(self.pos.x, self.pos.y, self.w, self.h)
        pygame.draw.rect(surface, (180, 0, 0), itself)