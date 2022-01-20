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
        self.xspeed = 0.7

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.pos.x, self.pos.y, self.w, self.h))

    def collision_test(self, ball: Ball.basic_ball, universal_speed):
        impulse = precode.intersect_rectangle_circle(self.pos, self.w, self.h, ball.pos, ball.r, ball.dir)
    
        if impulse:
            ball.dir = impulse * universal_speed
    
    def update(self):
        if self.dir_right:
            self.pos.x += self.xspeed
        else:
            self.pos.x -= self.xspeed
