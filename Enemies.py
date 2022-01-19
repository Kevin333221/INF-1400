from pygame import Vector2
import pygame
import precode
import random

class basic_enemy:
    def __init__(self, screen_w, screen_h, xpos, ypos, width, color):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.pos = Vector2(xpos, ypos)
        self.w = width
        self.h = 40
        self.color = color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.pos.x, self.pos.y, self.w, self.h))

    def create_enemies(self, surface, num_enemies):
        distance_between_other_enemies = 110
        all_enemies_length = distance_between_other_enemies*num_enemies
        
        # Calculating the width of the enemies depending on the screen size
        if self.w >= distance_between_other_enemies:
            self.w = distance_between_other_enemies - 10

        # Calculating the total width of x number of enemies on the screen
        if all_enemies_length > self.screen_w:
            while self.pos.x + distance_between_other_enemies < self.screen_w:
                self.pos.x += distance_between_other_enemies
        else:   
            while self.pos.x + distance_between_other_enemies < all_enemies_length:
                self.pos.x += distance_between_other_enemies

        enemy_xpos = 0
        enemy_ypos = 0
        enemy_shift_spawn = (self.screen_w - self.pos.x)/2 + 5
        counter = 0
        for x in range(num_enemies):
            enemy_color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
            enemy_xpos = counter*distance_between_other_enemies
            enemy = basic_enemy(self.screen_w, self.screen_h, enemy_shift_spawn, enemy_ypos, self.w, self.color)
            if enemy.pos.y + 50 < self.screen_h - 300:
                if enemy.pos.x + enemy.w <self.screen_w:
                    counter += 1
            else:
                enemy.pos.x = enemy_shift_spawn
                enemy.pos.y += 50
                enemy_ypos += 50
                counter = 1
        else:
            num_enemies -= 1
    def collision_test(self, ball_pos, ball_r, ball_dir, universal_speed):
        impulse = precode.intersect_rectangle_circle(self.pos, self.w, self.h, ball_pos, ball_r, ball_dir)
    
        if impulse:
            ball_dir = impulse * universal_speed
        return ball_dir
