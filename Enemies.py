from pygame import Vector2
import pygame
import precode
import Ball

class basic_enemy:
    dir_right = True

    def __init__(self, screen_w, screen_h, xpos, ypos, width, color):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.pos = Vector2(xpos, ypos)
        self.w = width
        self.h = 40
        self.color = color
        self.xspeed = 0.5

    def draw(self, surface):
        #self.color = abs(self.screen_h - self.pos.y)
        pygame.draw.rect(surface, self.color, (self.pos.x, self.pos.y, self.w, self.h))

    def update(self):
        if self.dir_right:
            self.pos.x += self.xspeed
        else:
            self.pos.x -= self.xspeed

    def color_picker(value, left_min, left_max, right_min, right_max):
        pass