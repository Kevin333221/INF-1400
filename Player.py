from pygame import Vector2
import pygame
import precode

class player:
    def __init__(self, screen_w, screen_h):
        self.w = 200
        self.h = 15
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.pos = Vector2((screen_w/2 - self.w/2), self.screen_h - 100)
        self.IMG = pygame.transform.smoothscale(pygame.image.load('player.png'),(200, 50))
        

    def walk(self, direction):
        self.xspeed = direction
        self.pos.x += self.xspeed

    def ball_hit(self, ball_pos, ball_r, ball_dir, universal_speed):
        impulse_user = precode.intersect_rectangle_circle(self.pos, self.w, self.h, ball_pos, ball_r, ball_dir)
        if impulse_user:
            ball_dir = impulse_user * universal_speed
        return ball_dir

    def draw(self, surface):
        itself = pygame.Rect(self.pos.x, self.pos.y, self.w, self.h)
        pygame.draw.rect(surface, (180, 0, 0), itself)
        #surface.blit(self.IMG, (self.pos.x, self.pos.y))