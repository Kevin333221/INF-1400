from os import remove, system
import random
from tracemalloc import start
from turtle import st
import pygame
import Player
import Enemies
import Ball
import precode
from pygame import Vector2

screen_w = 1400
screen_h = 800

num_of_enemies = 45
universal_speed = 6
distance_between_other_enemies = 100

# Pygame init
pygame.init()
pygame.mixer.init()
pygame.font.init()

# Screen init
screen = pygame.display.set_mode((screen_w, screen_h))
pygame.display.set_caption('Atari Breakout, The Game, idk, or whatever, jerk')
logo = pygame.image.load('Sprites/logo.png')
pygame.display.set_icon(logo)

# Sprites


# Fonts and texts
my_font_30 = pygame.font.SysFont('Times New Roman', 30)
my_font_60 = pygame.font.SysFont('Times New Roman', 60)
main_title = my_font_60.render("Welcome to this game!", False, (255, 255, 255))
main_start = my_font_60.render("Start", False, (255, 255, 255))

# Levels Background 
main_hub_BG = pygame.transform.smoothscale(pygame.image.load('Levels_BG/Main.jpg'), (screen_w, screen_h))
level1_BG = pygame.transform.smoothscale(pygame.image.load('Levels_BG/Level1.jpg'), (screen_w, screen_w))
level2_BG = pygame.transform.smoothscale(pygame.image.load('Levels_BG/level2.jpg'), (screen_w, screen_h))

# Sounds
mario = pygame.mixer.Sound('Sounds/Mario.mp3')
rick = pygame.mixer.Sound('Sounds/RickRoll.mp3')
ball_bounce = pygame.mixer.Sound('Sounds/pop.mp3')
sang = pygame.mixer.Sound('Sounds/sang.mp3')

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
    enemy_ypos = 40

    # Creating enemies
    for x in range(num_of_enemies):
        enemy_xpos = counter*distance_between_other_enemies
        enemy = Enemies.basic_enemy(screen_w, screen_h, enemy_xpos + enemy_spawn_shift, enemy_ypos, enemy_width, 0)
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

def check_for_quit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
    pygame.display.update()

def restart_level1(ball1, user):
    ball1.dead = False
    ball1.pos.x = screen_w/2
    ball1.pos.y = screen_h - 110
    ball1.dir = pygame.Vector2(random.randint(-universal_speed, universal_speed), -universal_speed)
    user.pos = Vector2((screen_w/2 - user.w/2), user.screen_h - 100)
    check_for_quit()

def dead():
    loser_text = my_font_60.render("Wanna play again?", False, (255, 255, 255))
    play_again = my_font_60.render("Oh no, you lost, maybe try again", False, (255, 255, 255))
    again_rect = pygame.Rect(screen_w/2 - 50, screen_h/2 - 52, 100, 45)

    while ball1.dead:  
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()
        screen.fill((40, 40, 40))
        screen.blit(loser_text, (screen_w/2 - loser_text.get_width()/2, screen_h/2))
        screen.blit(play_again, (screen_w/2 - play_again.get_width()/2, screen_h/3))

        if mouse_pos[0] > screen_w/2 - 50 and mouse_pos[0] < screen_w/2 - 50 + 100 and mouse_pos[1] > screen_h/2 - 52 and mouse_pos[1] < screen_h/2 - 52 + 45:
            pygame.draw.rect(screen, (0, 80, 80), again_rect)
            if mouse_clicked[0]:
                # Star over Again
                ball1.dead = False
        else:
            pygame.draw.rect(screen, (255, 80, 80), again_rect)
        check_for_quit()
    check_for_quit()

def level1():
    level1_start = False
    enemies = creating_enemies(num_of_enemies, 100)
    start_text = my_font_60.render("Start by pressing space", False, (255, 255, 255))
    winning_text = my_font_60.render("Congratulation, You Win!", False, (255, 255, 255))

    while level1_start == False:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    level1_start = True
        
        screen.blit(level1_BG, (0,0))
        
        # "Start by pressing enter" 
        screen.blit(start_text, (screen_w/2 - start_text.get_width()/2, screen_h/2))
        
        # Preview of player and ball
        ball1.draw(screen)
        user.draw(screen)

        while level1_start:
            screen.blit(level1_BG, (0,0))
            clock.tick(60)

            # Checks if the user presses Right-key og the Left-key
            keys = pygame.key.get_pressed()
            user.walk(keys, universal_speed)

            # Checks if the ball hits the player
            if precode.intersect_rectangle_circle(user.pos, user.w, user.h, ball1.pos, ball1.r, ball1.dir):
                ball_bounce.play()
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
                screen.fill((40, 40, 40))
                screen.blit(winning_text, (screen_w/2 - winning_text.get_width()/2, screen_h/2))
                ball1.dir.x = 0
                ball1.dir.y = 0
            
            # Checks if the ball is out of bottom of the screen
            if ball1.dead:
                enemies.clear()
                dead()
                restart_level1(ball1, user)
                enemies = creating_enemies(num_of_enemies, 100)
                level1_start = False

            check_for_quit()
        check_for_quit()

def exit_menu():
    pass

clock = pygame.time.Clock()
running = True
level1_init = False
alpha_screen = pygame.Surface((main_title.get_width(), screen_h), pygame.SRCALPHA)

# Game Loop
while running:
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()
    clock.tick(60)

    screen.blit(main_hub_BG, (0,0))
    screen.blit(main_title, (screen_w/2 - main_title.get_width()/2, screen_h/6))
    
    screen.blit(main_start, (screen_w/2 - main_start.get_width()/2, screen_h/3))
    pygame.draw.rect(alpha_screen, (0,0,0,155), (screen_w/2 - main_title.get_width()/2, screen_h/3, main_title.get_width(), main_start.get_height()), 21)

    # Lines
    pygame.draw.line(screen, (0,0,0), (screen_w/2, 0), (screen_w/2, screen_h))
    pygame.draw.line(screen, (0,0,0), (0, screen_h/2), (screen_w, screen_h/2))


    #pygame.draw.rect(screen, (0,0,0), (screen_w/2 - 200, screen_h/3, 400, 75))

    if mouse_pressed[0]:
        level1_init = True

    # Init levels
    if level1_init:
        level1()

    check_for_quit()
