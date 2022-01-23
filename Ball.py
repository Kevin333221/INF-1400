from asyncio import sleep
import random
import pygame
from pygame import Vector2
import pygame

class basic_ball:
    def __init__(self, screen_w, screen_h, speed):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.pos = pygame.Vector2(screen_w/2, screen_h - 110)
        self.r = 10
        self.dir = pygame.Vector2(random.randint(-speed, speed), -speed)
        self.dead = False
        self.speed = speed

    def draw(self, surface):
        pygame.draw.circle(surface, (255, 255, 255), self.pos, self.r)

    def update(self):
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

        self.pos += self.dir