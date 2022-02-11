from asyncio import sleep
import random
import pygame
from pygame import Vector2

pygame.mixer.init()

class basic_ball:
    def __init__(self, screen_w, screen_h):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.pos = pygame.Vector2(screen_w/2, self.screen_h - 140)
        self.r = screen_w/100
        self.speed = int(screen_w/150)
        self.dir = pygame.Vector2(random.randint(-self.speed, self.speed), -self.speed)
        self.dead = False
        self.speed = self.speed

    def draw(self, surface):
        pygame.draw.circle(surface, (255, 255, 255), self.pos, self.r)

    def update(self, screen_w, screen_h):
        if self.pos.x - self.r < 0:
            self.pos.x = self.r
            self.dir.x *= -1

        if self.pos.x + self.r > self.screen_w:
            self.pos.x = self.screen_w - self.r
            self.dir.x *= -1

        if self.pos.y - self.r < 0:
            self.pos.y = self.r
            self.dir.y *= -1
        
        if self.pos.y - self.r > self.screen_h:
            self.dead = True

        self.screen_w = screen_w
        self.screen_h = screen_h
        self.r = screen_w/100
        self.speed = int(screen_w/150)

        self.pos += self.dir