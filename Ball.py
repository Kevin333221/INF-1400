import random
import pygame
from pygame import Vector2

class basic_ball:
    def __init__(self, screen_w, screen_h, speed):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.pos = Vector2((screen_w - (3*self.screen_w)/5), screen_h - 200)
        self.r = 10
        self.dir = Vector2(random.randint(-speed, speed), -speed)

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
            print("Game Over")
            pygame.quit()
            quit()
        
        self.pos += self.dir
    
    def hit(self, enemy):
        
        pass