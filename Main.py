import pygame
import Player
import Enemies
import Ball
import precode

pygame.init()
universal_speed = 8
screen_w = 1200
screen_h = 600
screen = pygame.display.set_mode((screen_w, screen_h))
user = Player.player(screen_w, screen_h)
ball1 = Ball.basic_ball(screen_w, screen_h, universal_speed)

num_of_enemies = 10
bots = []

for spacing, x in enumerate(range(num_of_enemies)):
    enemy = Enemies.basic_enemy(screen_w, screen_h, spacing * 110)
    bots.append(enemy)

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

    # Checking if the ball hit the user
    impulse_user = precode.intersect_rectangle_circle(user.pos, user.w, user.h, ball1.pos, ball1.r, ball1.dir)
    if impulse_user:
        ball1.dir = impulse_user * universal_speed

    # Checking if the ball hits an enemy
    for x in bots:
        ball1.dir = x.collision_test(screen, ball1.pos, ball1.r, ball1.dir, universal_speed)
        x.draw(screen)

    ball1.update()
    ball1.draw(screen)
    user.draw(screen)
    pygame.display.update()
