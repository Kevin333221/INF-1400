from pygame import Vector2
import pygame

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
        self.IMG = pygame.transform.smoothscale(pygame.image.load('logo.png'), (50, 40))
        self.line_of_death = 150
        #self.color = ((random.randint(0,255)), (random.randint(0,255)), (random.randint(0,255)))

    def draw(self, surface):
        self.colorR = basic_enemy.color_picker(self.screen_w - self.pos.x, 0, self.screen_w, 0, 255)
        self.colorG = basic_enemy.color_picker(self.screen_h - self.pos.y, 0, self.screen_h - 20, 0, 255)
        pygame.draw.rect(surface, (self.colorR, self.colorG/2, self.colorG), (self.pos.x, self.pos.y, self.w, self.h))
        surface.blit(self.IMG, (self.pos.x, self.pos.y))
        pygame.draw.rect(surface, (255, 0, 0), (0, self.screen_h - self.line_of_death, self.screen_w, 10))

    def update(self):
        if self.dir_right:
            self.pos.x += self.xspeed
        else:
            self.pos.x -= self.xspeed

    def color_picker(value, left_min, left_max, right_min, right_max):
        return right_min + ((right_max - right_min) / (left_max - left_min)) * (value - left_min)
