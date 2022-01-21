import imp
from pygame import Vector2
import random
import pygame
import precode

class player:
    def __init__(self, screen_w, screen_h):
        self.w = 200
        self.h = 15
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.pos = Vector2((screen_w/2 - self.w/2), self.screen_h - 100)
        self.IMG = pygame.transform.smoothscale(pygame.image.load('player.png'),(self.w, 50))
        

    def walk(self, keys, direction):
        if keys[pygame.K_RIGHT] and self.pos.x + self.w < self.screen_w:
            self.xspeed = direction
            self.pos.x += self.xspeed
        if keys[pygame.K_LEFT] and self.pos.x > 0:
            self.xspeed = direction
            self.pos.x -= self.xspeed

    def ball_hit(self, ball, speed):
        where_it_hits = ((self.pos.x + self.w/2) - ball.pos.x)/(self.w/2)
        amount_of_force = speed * where_it_hits
        if ball.dir.y < speed:
            ball.dir.y = speed
        ball.dir.y = -ball.dir.y
        if ball.pos.x <= self.pos.x + self.w/2:
            ball.dir.x += -amount_of_force
        else:
             ball.dir.x += abs(amount_of_force)


    def draw(self, surface):
        itself = pygame.Rect(self.pos.x, self.pos.y, self.w, self.h)
        pygame.draw.rect(surface, (180, 0, 0), itself)
        #surface.blit(self.IMG, (self.pos.x, self.pos.y))