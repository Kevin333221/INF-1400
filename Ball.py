from asyncio import sleep
import random
import pygame
from pygame import Vector2

from Powerup import More_Balls , Stronger_Ball, Ghost_Ball

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

    def check_for_death(self):
        if self.pos.y - self.r > self.screen_h:
            return 1

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

        self.screen_w = screen_w
        self.screen_h = screen_h
        self.r = screen_w/100
        self.speed = int(screen_w/150)

    def moves(self):
        self.pos += self.dir
    
    def upgrade_ball(self, powerup_list):
        if len(powerup_list) != 0:
            for power in powerup_list:
                if type(power) == More_Balls:
                    print("Yes")
