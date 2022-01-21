from os import remove, system
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
pygame.font.init()

screen = pygame.display.set_mode((screen_w, screen_h))
pygame.display.set_caption('Atari Breakout, The Game, idk, or whatever, jerk')
logo = pygame.image.load('logo.png')
pygame.display.set_icon(logo)
my_font = pygame.font.SysFont('Times New Roman', 30)
loser_text = my_font.render("You're a loser, go cry to your mama", False, (255, 255, 255))

alpha_surface = pygame.Surface((screen_w, screen_h))
alpha_surface.set_alpha(40)
alpha_surface.fill((40, 40, 40))

# Sounds
mario = pygame.mixer.Sound('Mario.mp3')
rick = pygame.mixer.Sound('RickRoll.mp3')
somebody = pygame.mixer.Sound('Somebody.mp3')
ball_bounce = pygame.mixer.Sound('pop.mp3')
sang = pygame.mixer.Sound('sang.mp3')

# User, Enemies
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
    enemy_ypos = 100

    # Creating enemies
    for x in range(num_of_enemies):
        enemy_color = ((random.randint(0,255)), (random.randint(0,255)), (random.randint(0,255)))
        enemy_xpos = counter*distance_between_other_enemies
        enemy = Enemies.basic_enemy(screen_w, screen_h, enemy_xpos + enemy_spawn_shift, enemy_ypos, enemy_width, enemy_color)
        if enemy.pos.y + 50 < screen_h - enemy.line_of_death:
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

def dead():
    while ball1.dead:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ball1.dead = False
                running = False
                pygame.quit()

        screen.blit(loser_text, (screen_w/2, screen_h/2))
        pygame.display.update()

def game():
    # Checks if the user presses Right-key og the Left-key
    keys = pygame.key.get_pressed() 
    user.walk(keys, universal_speed)

    if precode.intersect_rectangle_circle(user.pos, user.w, user.h, ball1.pos, ball1.r, ball1.dir):
        ball_bounce.play()
        user.ball_hit(ball1, universal_speed)

    # Renderer
    ball1.update()
    ball1.draw(screen)
    user.draw(screen)

    if ball1.dead:
        dead()
        
    # Enemies Method Init
    if len(enemies) != 0:
        for x in enemies:
            hits_an_enemy = precode.intersect_rectangle_circle(x.pos, x.w, x.h, ball1.pos, ball1.r, ball1.dir)
            if hits_an_enemy:
                ball_bounce.play()
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
    
    #screen.blit(alpha_surface, (0, 0, screen_w, screen_h))
    pygame.display.update()

clock = pygame.time.Clock()
running = True
screen.fill((40,40,40))

sang.play()

while running:
    clock.tick(60)

    screen.fill((40,40,40))
    game()

    # Handling the events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()



