from pygame import Vector2
import pygame
import precode
import Ball

class basic_enemy:
    def __init__(self, screen_w, screen_h, xpos, ypos, width, color):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.pos = Vector2(xpos, ypos)
        self.w = width
        self.h = 40
        self.color = color
        self.dir_right = True

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.pos.x, self.pos.y, self.w, self.h))

    def collision_test(self, ball: Ball.basic_ball, universal_speed):
        impulse = precode.intersect_rectangle_circle(self.pos, self.w, self.h, ball.pos, ball.r, ball.dir)
    
        if impulse:
            ball.dir = impulse * universal_speed
    
    def update(self, surface):
        if self.pos.x + self.w >= self.screen_w: 
            self.pos.x = self.screen_w - self.w 
            self.dir_right = False
            self.pos.y += 50

        if self.pos.x <= 0:
            self.pos.x = 0
            self.dir_right = True
            self.pos.y += 50

        if self.dir_right == True:
            self.pos.x += 1
        elif self.dir_right == False:
            self.pos.x -= 1