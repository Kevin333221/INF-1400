import pygame
import Player
import Enemies
import Ball
import precode

pygame.init()
screen_w = 1200
screen_h = 800
screen = pygame.display.set_mode((screen_w, screen_h))
user = Player.player()
enemy1 = Enemies.basic_enemy()
ball1 = Ball.basic_ball()

running = True
while running:
    screen.fill((40,40,40))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT]:
        user.walk(0.7)
    if keys[pygame.K_LEFT]:
        user.walk(-0.7)

    impulse_enemy1 = precode.intersect_rectangle_circle(enemy1.pos, enemy1.w, enemy1.h, ball1.pos, ball1.r, ball1.dir)
    impulse_user = precode.intersect_rectangle_circle(user.pos, user.w, user.h, ball1.pos, ball1.r, ball1.dir)

    if impulse_enemy1:
        ball1.dir = impulse_enemy1
    
    if impulse_user:
        ball1.dir = impulse_user

    ball1.update()
    ball1.draw(screen)
    enemy1.draw(screen)
    user.draw(screen)
    pygame.display.update()
