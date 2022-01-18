from os import remove
import pygame
import Player
import Enemies
import Ball
import precode

screen_w = 700
screen_h = 900

num_of_enemies = 30
universal_speed = 8
distance_between_other_enemies = 110

pygame.init()

screen = pygame.display.set_mode((screen_w, screen_h))
pygame.display.set_caption('Atari Breakout, The Game, idk, or whatever, jerk')
logo = pygame.image.load('logo.png')
pygame.display.set_icon(logo)

user = Player.player(screen_w, screen_h)
ball1 = Ball.basic_ball(screen_w, screen_h, universal_speed)
messuring_enemy = Enemies.basic_enemy(screen_w, screen_h, 0, 40, 100)

# Initalizing Enemy values
all_enemies_length = distance_between_other_enemies*num_of_enemies

# Calculating the total width of x number of enemies on the screen
if all_enemies_length > screen_w:
    while messuring_enemy.pos.x + messuring_enemy.w < screen_w:
        messuring_enemy.pos.x += messuring_enemy.w
    messuring_enemy.pos.x -= messuring_enemy.w
else:
    while messuring_enemy.pos.x + messuring_enemy.w < all_enemies_length:
        messuring_enemy.pos.x += messuring_enemy.w
    messuring_enemy.pos.x -= messuring_enemy.w

# Calculating the width of the enemies depending on the screen size
if messuring_enemy.w >= distance_between_other_enemies:
    messuring_enemy.w = distance_between_other_enemies - 10

enemy_spawn_shift = (screen_w - messuring_enemy.pos.x - messuring_enemy.w)/2

bots = []
counter = 0
enemy_ypos = 40
# Creating enemies
for x in enumerate(range(num_of_enemies)):
    enemy_xpos = counter*distance_between_other_enemies
    enemy = Enemies.basic_enemy(screen_w, screen_h, enemy_xpos + enemy_spawn_shift, enemy_ypos, messuring_enemy.w)
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
            exit()

    # Checks if the user presses Right-key og the Left-key
    keys = pygame.key.get_pressed() 
    if keys[pygame.K_RIGHT] and user.pos.x + user.w < screen_w:
        user.walk(universal_speed)
    if keys[pygame.K_LEFT] and user.pos.x > 0:
        user.walk(-universal_speed)

    # Checking if the ball hit the user
    impulse_user = precode.intersect_rectangle_circle(user.pos, user.w, user.h, ball1.pos, ball1.r, ball1.dir)
    if impulse_user:
        ball1.dir = impulse_user * universal_speed

    # Checking if the ball hits an enemy
    if len(bots) != 0:
        for x in bots:
            ball1.dir = x.collision_test(ball1.pos, ball1.r, ball1.dir, universal_speed)
            if precode.intersect_rectangle_circle(x.pos, x.w, x.h, ball1.pos, ball1.r, ball1.dir):
                bots.remove(x)
            x.draw(screen)
    else:
        print("CONGRATULATION! YOU'VE WON!")
        pygame.quit()
        quit()

    # 'Renderer'
    ball1.update()
    ball1.draw(screen)
    user.draw(screen)
    pygame.display.update()

pygame.quit()