from os import remove
import random
import pygame
import Player
import Enemies
import Ball
import precode

screen_w = 1400
screen_h = 900

num_of_enemies = 48
universal_speed = 8
distance_between_other_enemies = 110
enemy_color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))

pygame.init()

screen = pygame.display.set_mode((screen_w, screen_h))
pygame.display.set_caption('Atari Breakout, The Game, idk, or whatever, jerk')
logo = pygame.image.load('logo.png')
pygame.display.set_icon(logo)

user = Player.player(screen_w, screen_h)
ball1 = Ball.basic_ball(screen_w, screen_h, universal_speed)

def creating_enemies(num_of_enemies):
    counter = 0
    all_enemies_length = distance_between_other_enemies*num_of_enemies
    enemy_messuring_unit = 0
    enemy_width = 100

    # Calculating the total width of x number of enemies on the screen
    if all_enemies_length > screen_w:
        while enemy_messuring_unit + distance_between_other_enemies < screen_w:
            enemy_messuring_unit += distance_between_other_enemies
    else:
        while enemy_messuring_unit + distance_between_other_enemies < all_enemies_length:
            enemy_messuring_unit += distance_between_other_enemies

    # Calculating the width of the enemies depending on the screen size
    if enemy_width >= distance_between_other_enemies:
        enemy_width = distance_between_other_enemies - 10

    enemy_spawn_shift = (screen_w - enemy_messuring_unit)/2 + 5
    bots = []
    enemy_ypos = 40

    # Creating enemies
    for x in range(num_of_enemies):
        enemy_color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
        enemy_xpos = counter*distance_between_other_enemies
        enemy = Enemies.basic_enemy(screen_w, screen_h, enemy_xpos + enemy_spawn_shift, enemy_ypos, enemy_width, enemy_color)
        if enemy.pos.y + 50 < screen_h - 300:
            if enemy.pos.x + enemy.w < screen_w:
                counter += 1
            else:
                enemy.pos.x = enemy_spawn_shift
                enemy.pos.y += 50
                enemy_ypos += 50
                counter = 1
            bots.append(enemy)
        else:
            num_of_enemies -= 1

    return bots

enemies = creating_enemies(num_of_enemies)

clock = pygame.time.Clock()
running = True
while running:
    clock.tick(60)
    screen.fill((40,40,40))
    
    # Handling the events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

    # Checks if the user presses Right-key og the Left-key
    keys = pygame.key.get_pressed() 
    if keys[pygame.K_RIGHT] and user.pos.x + user.w < screen_w:
        user.walk(universal_speed)
    if keys[pygame.K_LEFT] and user.pos.x > 0:
        user.walk(-universal_speed)

    # Enemies init
    if len(enemies) != 0:
        for x in enemies:
            x.collision_test(ball1, universal_speed)
            if precode.intersect_rectangle_circle(x.pos, x.w, x.h, ball1.pos, ball1.r, ball1.dir):
                enemies.remove(x)
            else:    
                x.draw(screen)
        
    else:
        print("congatulton! YOU'VE WON!")
        pygame.quit()
        quit()

    # 'Renderer'
    user.ball_hit(ball1, universal_speed)
    ball1.update()
    ball1.draw(screen)
    user.draw(screen)
    pygame.display.update()

pygame.quit()