from pygame import Vector2
import pygame
import precode

class basic_enemy:
    def __init__(self, screen_w, screen_h, xpos, ypos, width):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.pos = Vector2(xpos, ypos)
        self.w = width
        self.h = 40

    def draw(self, surface):
        pygame.draw.rect(surface, (200, 200, 255), (self.pos.x, self.pos.y, self.w, self.h))


    def collision_test(self, ball_pos, ball_r, ball_dir, universal_speed):
        impulse = precode.intersect_rectangle_circle(self.pos, self.w, self.h, ball_pos, ball_r, ball_dir)
    
        if impulse:
            ball_dir = impulse * universal_speed
        return ball_dir
