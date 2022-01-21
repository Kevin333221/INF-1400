from os import remove
import random
import pygame
import Player
import Enemies
import Ball
import precode

screen_w = 1000
screen_h = 600

num_of_enemies = 45
universal_speed = 6
distance_between_other_enemies = 100

enemy_color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((screen_w, screen_h))
pygame.display.set_caption('Atari Breakout, The Game, idk, or whatever, jerk')
logo = pygame.image.load('logo.png')
pygame.display.set_icon(logo)
mario = pygame.mixer.Sound('Mario.mp3')
rick = pygame.mixer.Sound('RickRoll.mp3')
somebody = pygame.mixer.Sound('Somebody.mp3')

user = Player.player(screen_w, screen_h)
ball1 = Ball.basic_ball(screen_w, screen_h, universal_speed)

def creating_enemies(num_of_enemies, enemy_width):
    counter = 0
    all_enemies_length = distance_between_other_enemies*num_of_enemies
    enemy_messuring_unit = 0

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
enemies = creating_enemies(num_of_enemies, 100)

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
    user.walk(keys, universal_speed)

    if precode.intersect_rectangle_circle(user.pos, user.w, user.h, ball1.pos, ball1.r, ball1.dir):
        user.ball_hit(ball1, universal_speed)

    # Renderer
    ball1.update()
    ball1.draw(screen)
    user.draw(screen)
        
    # Enemies Method Init
    if len(enemies) != 0:
        for x in enemies:
            hits_an_enemy = precode.intersect_rectangle_circle(x.pos, x.w, x.h, ball1.pos, ball1.r, ball1.dir)
            if hits_an_enemy:
                ball1.dir = hits_an_enemy * ball1.speed
                enemies.remove(x)
            else:
                if x.pos.x + x.w >= x.screen_w:
                    Enemies.basic_enemy.dir_right = False
                    for y in enemies:
                        y.pos.y += 5
                if x.pos.x <= 0:
                    Enemies.basic_enemy.dir_right = True                
                    for y in enemies:
                        y.pos.y += 5
                x.update()
                x.draw(screen)

    else:
        print("Congatulton! YU WÅN!")
        pygame.quit()
        quit()
        
    if ball1.dead == True:
        print("You've lost")
        pygame.quit()
        quit()
    
    
    pygame.display.update()



