from pygame import Vector2
import pygame

class basic_enemy:
    dir_right = True
    color = (255, 50, 120)
    
    def __init__(self, screen_w, screen_h, xpos, ypos, width, height):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.pos = Vector2(xpos, ypos)
        self.w = width
        self.h = height
        self.health = 1
        self.xspeed = 0.5
        self.line_of_death = 200
        self.h_change = screen_h/50

    def update_screen_size(self, screen_w, screen_h):
        self.screen_w = screen_w
        self.screen_h = screen_h

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.pos.x, self.pos.y, self.w, self.h))
        #surface.blit(self.IMG, (self.pos.x + self.w/2 - self.IMG.get_width()/2, self.pos.y))
        pygame.draw.rect(surface, (255, 0, 0), (0, self.screen_h - self.line_of_death, self.screen_w, 10))

    def update(self):
        if self.dir_right:
            self.pos.x += self.xspeed
        else:
            self.pos.x -= self.xspeed

class harder_enemy(basic_enemy):
    color = (50, 255, 120)    
    def __init__(self, screen_w, screen_h, xpos, ypos, width, height):
        super().__init__(screen_w, screen_h, xpos, ypos, width, height)
        self.health = 2

class even_harder_enemy(basic_enemy):
    color = (120, 50, 255)
    def __init__(self, screen_w, screen_h, xpos, ypos, width, height):
        super().__init__(screen_w, screen_h, xpos, ypos, width, height)
        self.health = 3