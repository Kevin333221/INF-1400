from pygame import Vector2
import pygame
from Ball import basic_ball
import precode

pygame.mixer.init()

class player:
    def __init__(self, screen_w, screen_h):
        self.w = screen_w/8
        self.h = 15
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.pos = Vector2((screen_w/2 - self.w/2), self.screen_h - 100)
        self.speed = int(self.screen_w/150)
        self.ball_bounce = pygame.mixer.Sound('Sounds/pop.mp3')

    def update_screen_size(self, screen_w, screen_h):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.w = screen_w/8
        self.pos = Vector2((screen_w/2 - self.w/2), self.screen_h - 100)     

    def update(self, screen_w, balls):
        keys = pygame.key.get_pressed()
        self.speed = int(screen_w/130)

        if keys[pygame.K_RIGHT] and self.pos.x + self.w < self.screen_w:
            self.xspeed = self.speed
            self.pos.x += self.xspeed
        if keys[pygame.K_LEFT] and self.pos.x > 0:
            self.xspeed = self.speed
            self.pos.x -= self.xspeed

        # Checks if the ball hits the player
        for ball in balls:
            hit = precode.intersect_rectangle_circle(self.pos, self.w, self.h, ball.pos, ball.r, ball.dir)
            if hit:
                self.ball_bounce.play()
                where_it_hits = (((self.pos.x + self.w/2) - ball.pos.x)/(self.w/2))
                amount_of_force = self.speed * where_it_hits
                if ball.dir.y < self.speed:
                    ball.dir.y = self.speed
                ball.dir.y = -ball.dir.y
                if ball.pos.x <= self.pos.x + self.w/2:
                    ball.dir.x += -amount_of_force
                else:
                    ball.dir.x += abs(amount_of_force)

    def draw(self, surface):
        itself = pygame.Rect(self.pos.x, self.pos.y, self.w, self.h)
        pygame.draw.rect(surface, (180, 0, 0), itself)