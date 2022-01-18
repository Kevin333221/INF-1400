from os import remove
import pygame
import Player
import Enemies
import Ball
import precode

screen_w = 1200
screen_h = 900

num_of_enemies = 1

pygame.init()

universal_speed = 8
screen = pygame.display.set_mode((screen_w, screen_h))
user = Player.player(screen_w, screen_h)
ball1 = Ball.basic_ball(screen_w, screen_h, universal_speed)
messuring_enemy = Enemies.basic_enemy(screen_w, screen_h, 0, 40, 100)

# Initalizing Enemy values
distance = 100
all_enemies_length = distance*num_of_enemies
enemy_ypos = 40

# Calculating the total width of x number of enemies on the screen
if all_enemies_length >= screen_w:
    while messuring_enemy.pos.x + messuring_enemy.w < screen_w:
        messuring_enemy.pos.x += messuring_enemy.w

enemy_spawn_shift = (screen_w - messuring_enemy.pos.x)/2

# Calculating the width of the enemies depending on the screen size
if messuring_enemy.w >= distance:
    messuring_enemy.w = distance - 10

bots = []
counter = 0
# Creating enemies
for x in enumerate(range(num_of_enemies)):
    enemy_xpos = counter*distance
    enemy = Enemies.basic_enemy(screen_w, screen_h, enemy_xpos + enemy_spawn_shift, enemy_ypos, messuring_enemy.w)
    bots.append(enemy)
    counter += 1
    if enemy.pos.x + enemy.w >= screen_w - 100:
        enemy_ypos += 50
        counter = 0

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