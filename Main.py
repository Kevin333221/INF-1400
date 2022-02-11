from math import sqrt
from os import remove
import random
import sys
import pygame
import Player
import Enemies
import Ball
from Powerup import More_Balls, Stronger_Ball, Ghost_Ball
import precode
from pygame import K_ESCAPE, Vector2

screen_w = 1200
screen_h = 600

clock_tick = 60

# Pygame init
pygame.init()
pygame.mixer.init()
pygame.font.init()
pygame.display.init()

pygame.mixer.set_num_channels(8)

# Screen init
screen = pygame.display.set_mode((screen_w, screen_h))
pygame.display.set_caption('Atari Breakout, The Game, idk, or whatever, jerk')
logo = pygame.image.load('Sprites/logo.png')
pygame.display.set_icon(logo)

# Fonts and texts
my_font_60 = pygame.font.SysFont('Times New Roman', 60)
my_font_30 = pygame.font.SysFont('Times New Roman', 30)
main_title = my_font_60.render("Welcome to Breakout!", False, (255, 255, 255))
main_start = my_font_60.render("Start", False, (255, 255, 255))
main_levels = my_font_60.render("Levels", False, (255, 255, 255))
main_options = my_font_60.render("Options", False, (255, 255, 255))
main_exit = my_font_60.render("Exit", False, (255, 255, 255))

# Levels Background 
main_hub_BG = pygame.transform.smoothscale(pygame.image.load('Levels_BG/Main.jpg'), (screen_w, screen_h))

# Sounds
level_sounds = pygame.mixer.Channel(1)
rick = pygame.mixer.Sound('Sounds/RickRoll.mp3')
rick.set_volume(0.1)
main_song = pygame.mixer.Sound('Sounds/main_song.mp3')
level1_song = pygame.mixer.Sound('Sounds/Level1.mp3')
level2_song = pygame.mixer.Sound('Sounds/Level2.mp3')
level3_song = pygame.mixer.Sound('Sounds/Level3.mp3')
level4_song = pygame.mixer.Sound('Sounds/Level4.mp3')
level5_song = pygame.mixer.Sound('Sounds/Level5.mp3')
ball_bounce = pygame.mixer.Sound('Sounds/pop.mp3')
click = pygame.mixer.Sound('Sounds/click.mp3')

# Just a helping function that does the same as the "map()" function from C++
def map(value, left_min, left_max, right_min, right_max):
    return right_min + ((right_max - right_min) / (left_max - left_min)) * (value - left_min)

# As the name suggests, here is where the "enemies_create" algorithm is 
def enemies_create(array_with_enemies):
    global running

    counter = 0
    enemy_width = 110

    # Finds the total length that the "enemies" span across the screen
    all_enemies_length = enemy_width*len(array_with_enemies)

    enemy_messuring_unit = 0

    scale = screen_w/14
    enemy_width = scale
    enemy_height = screen_h/14

    # Calculating the total width of x number of enemies on the screen
    if all_enemies_length > screen_w:
        while enemy_messuring_unit + enemy_width < screen_w:
            enemy_messuring_unit += enemy_width
    else:
        while enemy_messuring_unit + enemy_width < all_enemies_length:
            enemy_messuring_unit += enemy_width

    enemy_spawn_shift = scale
    bots = []
    enemy_ypos = 40
    
    for x in array_with_enemies:
        enemy_xpos = counter*enemy_width
        if x == 0:
            if enemy_xpos + enemy_width + scale < screen_w:
                counter += 1
            else:
                enemy_xpos = enemy_spawn_shift
                enemy_ypos += enemy_height + 10
                counter = 1
        elif x == 1:
            enemy = Enemies.basic_enemy(screen_w, screen_h, enemy_xpos + enemy_spawn_shift, enemy_ypos, enemy_width - 10, enemy_height, 0)
            if enemy.pos.y + 50 < screen_h - enemy.line_of_death:
                if enemy.pos.x + enemy.w + scale < screen_w:
                    counter += 1
                else:
                    enemy.pos.x = enemy_spawn_shift
                    enemy.pos.y += enemy_height + 10
                    enemy_ypos += enemy_height + 10
                    counter = 1  
            colorR = map(screen_w - enemy.pos.x, 0, screen_w, 0, 255)
            colorG = map(screen_h - enemy.pos.y, 0, screen_h - 20, 0, 255)
            enemy.color = (colorR, colorG/2, colorG)
            bots.append(enemy)
        elif x == 2:
            enemy = Enemies.harder_enemy(screen_w, screen_h, enemy_xpos + enemy_spawn_shift, enemy_ypos, enemy_width - 10, enemy_height, 0)
            if enemy.pos.y + 50 < screen_h - enemy.line_of_death:
                if enemy.pos.x + enemy.w + scale < screen_w:
                    counter += 1
                else:
                    enemy.pos.x = enemy_spawn_shift
                    enemy.pos.y += enemy_height + 10
                    enemy_ypos += enemy_height + 10
                    counter = 1    
            colorR = map(screen_w - enemy.pos.x, 0, screen_w, 0, 255)
            colorG = map(screen_h - enemy.pos.y, 0, screen_h - 20, 0, 255)
            enemy.color = (colorR, colorG/3, colorG/2)
            bots.append(enemy)
        else:
            print("Invalid ID")
            running = False
            pygame.quit()
            sys.exit()
    return bots
 
# As the name suggests again, here is where i restart a level
def restart_level(ball1, user):
    global running

    dead()

    ball1.dead = False
    ball1.pos.x = screen_w/2
    ball1.pos.y = screen_h - 110 
    object_speed = int(screen_h/120)
    ball1.dir = pygame.Vector2(random.randint(-object_speed, object_speed), -object_speed)
    user.pos = Vector2((screen_w/2 - user.w/2), user.screen_h - 100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                exit_menu()

def dead():
    global running

    loser_text = my_font_60.render("Wanna play again?", False, (255, 255, 255))
    play_again = my_font_60.render("Oh no, you lost, maybe try again", False, (255, 255, 255))
    again_rect = pygame.Rect(screen_w/2 - 50, screen_h/2 - 52, 100, 45)

    dead = True

    while dead:  
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()
        screen.fill((40, 40, 40))
        screen.blit(loser_text, (screen_w/2 - loser_text.get_width()/2, screen_h/2))
        screen.blit(play_again, (screen_w/2 - play_again.get_width()/2, screen_h/3))

        if mouse_pos[0] > screen_w/2 - 50 and mouse_pos[0] < screen_w/2 - 50 + 100 and mouse_pos[1] > screen_h/2 - 52 and mouse_pos[1] < screen_h/2 - 52 + 45:
            pygame.draw.rect(screen, (0, 80, 80), again_rect)
            if mouse_clicked[0]:
                # Star over Again
                dead = False
        else:
            pygame.draw.rect(screen, (255, 80, 80), again_rect)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    exit_menu()
        pygame.display.update()
    
def winning_screen():
    global running

    winning_text = my_font_60.render("Congratulation, You Win!", False, (255, 255, 255))
    screen.fill((40, 40, 40))
    screen.blit(winning_text, (screen_w/2 - winning_text.get_width()/2, screen_h/4))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                exit_menu()
    pygame.display.update()

# Here is where i check if the ball hits an enemy and also drawing them
def enemies_mechanics(enemies, ball, powerups_list):
    
    more_balls_powerup_odds = 10
    stronger_ball_powerup_odds = 2
    ghost_ball_powerup_odds = 1

    for x in enemies:
        if x != 0:
            hits_an_enemy = precode.intersect_rectangle_circle(x.pos, x.w, x.h, ball.pos, ball.r, ball.dir)
            if hits_an_enemy and x.health == 1:

                # Maybe a powerup will spawn
                dice = random.randint(0, 10)
                if more_balls_powerup_odds >= dice:
                    MB_powerup = More_Balls(screen_w, screen_h, x)
                    powerups_list.append(MB_powerup)
                if stronger_ball_powerup_odds >= dice:
                    SB_powerup = Stronger_Ball(screen_w, screen_h, x)
                    powerups_list.append(SB_powerup)
                if ghost_ball_powerup_odds >= dice:
                    GB_powerup = Ghost_Ball(screen_w, screen_h, x)
                    powerups_list.append(GB_powerup)

                ball_bounce.play()
                ball.dir = hits_an_enemy * ball.speed
                enemies.remove(x)
            elif hits_an_enemy and x.health == 2:
                ball_bounce.play()
                ball.dir = hits_an_enemy * ball.speed
                colorR = map(screen_w - x.pos.x, 0, screen_w, 0, 255)
                colorG = map(screen_h - x.pos.y, 0, screen_h - 20, 0, 255)
                x.color = (colorR, colorG/2, colorG)
                x.health -= 1
            else:
                if x.pos.x + x.w >= x.screen_w:
                    Enemies.basic_enemy.dir_right = False
                    for y in enemies:
                        y.pos.y += y.h_change
                if x.pos.x <= 0:
                    Enemies.basic_enemy.dir_right = True                
                    for y in enemies:
                        y.pos.y += y.h_change

            x.update()
            x.draw(screen)

            if x.pos.y + 5 >= screen_h - x.line_of_death:
                ball.dead = True
                
    for power in powerups_list:
        power.draw(screen, power.IMG)
        power.update()

        if power.pos.y > screen_h:
            powerups_list.remove(power)

# The level creation
def init_level_of_your_choice(background, title, music, arr_of_enemies, nextlevel):

    global clock_tick
    global running
    global level_sounds
    
    level_sounds.play(music) 

    level_BG = pygame.transform.smoothscale(pygame.image.load(background), (screen_w, screen_w))
    start_text = my_font_60.render("Start by pressing space, Use your arrow keys", False, (255, 255, 255))
    level_title = my_font_60.render(title, False, (255, 255, 255))

    clock.tick(clock_tick)
    
    user = Player.player(screen_w, screen_h)
    ball1 = Ball.basic_ball(screen_w, screen_h)
    enemies = enemies_create(arr_of_enemies)

    level_init = True
    while level_init:
        clock.tick(clock_tick)

        # Checking if the screensize has changed
        if enemies[0].screen_w != screen_w:
            enemies.clear()
            enemies = enemies_create(arr_of_enemies)

        level_BG = pygame.transform.smoothscale(pygame.image.load(background), (screen_w, screen_w))

        user.update_screen_size(screen_w, screen_h)
        ball1.update(screen_w, screen_h)
        
        level_start = False
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    level_start = True
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    exit_menu()

        pygame.display.update()
        
        screen.blit(level_BG, (0,0))
        screen.blit(level_title, (screen_w/2 - level_title.get_width()/2, 10))

        # "Start by pressing enter" 
        screen.blit(start_text, (screen_w/2 - start_text.get_width()/2, screen_h/2))
        
        # Preview of player and ball
        ball1.draw(screen)
        user.draw(screen)
        
        powerups_list = []

        while level_start: 
            clock.tick(clock_tick)
            screen.blit(level_BG, (0,0))

            if level_sounds.get_busy() == False:
                level_sounds.play(music)
            
            # Renderer
            ball1.update(screen_w, screen_h)
            ball1.moves()
            ball1.draw(screen)
            user.update(screen_w, ball1)
            user.draw(screen)

            # Enemies Method Init
            if len(enemies) != 0:
                enemies_mechanics(enemies, ball1, powerups_list)
            else:
                # When Winnning
                level_init = False
                level_start = False
                next_level(nextlevel)

            # Checks if the ball is out of bottom of the screen
            if ball1.dead:
                enemies.clear()
                restart_level(ball1, user)
                enemies = enemies_create(arr_of_enemies)
                level_start = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        level_start = False
                        exit_menu()
            pygame.display.update()  
        pygame.display.update()
    pygame.display.update()

# Keeps track of what level is playing next
def next_level(x):
    if x == 1:
        level1_BG = ('Levels_BG/Level1.jpg')
        level1_title = ("Level 1 - The Beginning")
        init_level_of_your_choice(level1_BG, level1_title, level1_song, [1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1], 2)
    
    elif x == 2:
        level2_BG = ('Levels_BG/Level2.jpg')
        level2_title = ("Level 2 - Double Up")
        init_level_of_your_choice(level2_BG, level2_title, level2_song, [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
                                                                         1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 3)
    elif x == 3:
        level3_BG = ('Levels_BG/Level3.jpg')
        level3_title = ("Level 3 - It's getting harder")
        init_level_of_your_choice(level3_BG, level3_title, level3_song, [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                                                                         1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 4)
    elif x == 4:
        level4_BG = ('Levels_BG/Level4.jpg')
        level4_title = ("Level 4 - Why so strange?")
        init_level_of_your_choice(level4_BG, level4_title, level4_song, [0, 1, 0, 1, 0, 2, 2, 0, 1, 0, 1, 0,
                                                                         1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1], 5)
    elif x == 5:
        level5_BG = ('Levels_BG/Level5.jpg')
        level5_title = ("Level 5 - Stygging")
        init_level_of_your_choice(level5_BG, level5_title, level5_song, [1, 1, 0, 0, 2, 0, 0, 2, 0, 0, 1, 1,
                                                                         0, 0, 1, 1, 0, 2, 2, 0, 1, 1, 0, 0,
                                                                         0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0], 0)                                                                    
                                                                        
    else:
        winning_screen()

# The exit menu by pressing espace
def exit_menu():
    global running

    resume_text = my_font_30.render("Resume", False, (255, 255, 255))
    options_text = my_font_30.render("Options", False, (255, 255, 255))
    rick_text = my_font_30.render("Free Money", False, (255, 255, 255))
    back_text = my_font_30.render("Back To Main", False, (255, 255, 255))
    exit_text = my_font_30.render("Exit", False, (255, 255, 255))

    runs = True
    while runs:
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        block_height = (screen_h/2 - 60)/4

        pygame.draw.rect(screen, (70, 70, 70),    (screen_w/3, screen_h/4, screen_w/3, screen_h/2 + block_height))
        pygame.draw.rect(screen, (255, 255, 255), (screen_w/3, screen_h/4, screen_w/3, screen_h/2 + block_height), 2)

        pygame.draw.rect(screen, (40, 40, 40), (screen_w/3 + 20, screen_h/4 + 20, screen_w/3 - 40, screen_h/2 - 40 + block_height))
        pygame.draw.rect(screen, ( 0,  0,  0), (screen_w/3 + 20, screen_h/4 + 20, screen_w/3 - 40, screen_h/2 - 40 + block_height) , 2)
        
        # Resume Block
        pygame.draw.rect(screen, (70,  70, 70), (screen_w/3 + 40, screen_h/4 + 40,  screen_w/3 - 80, block_height - 20))
        screen.blit(resume_text, (screen_w/3 + 40 + (screen_w/3 - 80)/2 - resume_text.get_width()/2, screen_h/4 + 40 + block_height/2 - 20 - resume_text.get_height()/4))
        if mouse_pos[0] > screen_w/3 + 40 and mouse_pos[0] < screen_w/3 + 40 + screen_w/3 - 80 and mouse_pos[1] > screen_h/4 + 40 and mouse_pos[1] < screen_h/4 + 40 + block_height - 20:
            pygame.draw.rect(screen, (60, 255, 255), (screen_w/3 + 40, screen_h/4 + 40, screen_w/3 - 80, block_height - 20), 2)
            if mouse_pressed[0]:
                click.play()
                runs = False
                pygame.mouse.set_pos(screen_w/2, screen_h/4)
        else:
            pygame.draw.rect(screen, (100, 100, 100), (screen_w/3 + 40, screen_h/4 + 40,  screen_w/3 - 80, block_height - 20), 2)
        
        # Options Block
        pygame.draw.rect(screen, (70,  70, 70),   (screen_w/3 + 40, screen_h/4 + 40 + block_height,  screen_w/3 - 80, block_height - 20))
        screen.blit(options_text, (screen_w/3 + 40 + (screen_w/3 - 80)/2 - options_text.get_width()/2, screen_h/4 + 40 + block_height/2 - 20 - options_text.get_height()/4 + block_height))
        if mouse_pos[0] > screen_w/3 + 40 and mouse_pos[0] < screen_w/3 + 40 + screen_w/3 - 80 and mouse_pos[1] > screen_h/4 + 40 + block_height and mouse_pos[1] < screen_h/4 + 40 + block_height*2 - 20:
            pygame.draw.rect(screen, (60, 255, 255), (screen_w/3 + 40, screen_h/4 + 40 + block_height,  screen_w/3 - 80, block_height - 20), 2)
            if mouse_pressed[0]:
                click.play()
                pygame.mouse.set_pos(screen_w/2, screen_h/4)
                options()
                runs = False
        else:
            pygame.draw.rect(screen, (100, 100, 100), (screen_w/3 + 40, screen_h/4 + 40 + block_height,  screen_w/3 - 80, block_height - 20), 2)

        # Rick Block
        pygame.draw.rect(screen, (70,  70, 70),   (screen_w/3 + 40, screen_h/4 + 40 + block_height*2,  screen_w/3 - 80, block_height - 20))
        screen.blit(rick_text, (screen_w/3 + 40 + (screen_w/3 - 80)/2 - rick_text.get_width()/2, screen_h/4 + 40 + block_height/2 - 20 - rick_text.get_height()/4 + block_height*2))
        if mouse_pos[0] > screen_w/3 + 40 and mouse_pos[0] < screen_w/3 + 40 + screen_w/3 - 80 and mouse_pos[1] > screen_h/4 + 40 + block_height*2 and mouse_pos[1] < screen_h/4 + 40 + block_height*3 - 20:
            pygame.draw.rect(screen, (60, 255, 255), (screen_w/3 + 40, screen_h/4 + 40 + block_height*2,  screen_w/3 - 80, block_height - 20), 2)
            if mouse_pressed[0]:
                if rick.play():
                    pass
                else:
                    rick.play()
        else:
            pygame.draw.rect(screen, (100, 100, 100), (screen_w/3 + 40, screen_h/4 + 40 + block_height*2,  screen_w/3 - 80, block_height - 20), 2)

        # Back Block
        pygame.draw.rect(screen, (70,  70, 70),   (screen_w/3 + 40, screen_h/4 + 40 + block_height*3,  screen_w/3 - 80, block_height - 20))
        screen.blit(back_text, (screen_w/3 + 40 + (screen_w/3 - 80)/2 - back_text.get_width()/2, screen_h/4 + 40 + block_height/2 - 20 - back_text.get_height()/4 + block_height*3))
        if mouse_pos[0] > screen_w/3 + 40 and mouse_pos[0] < screen_w/3 + 40 + screen_w/3 - 80 and mouse_pos[1] > screen_h/4 + 40 + block_height*3 and mouse_pos[1] < screen_h/4 + 40 + block_height*4 - 20:
            pygame.draw.rect(screen, (60, 255, 255), (screen_w/3 + 40, screen_h/4 + 40 + block_height*3,  screen_w/3 - 80, block_height - 20), 2)
            if mouse_pressed[0]:
                runs = False

        else:
            pygame.draw.rect(screen, (100, 100, 100), (screen_w/3 + 40, screen_h/4 + 40 + block_height*3,  screen_w/3 - 80, block_height - 20), 2)

        # Exit Block
        pygame.draw.rect(screen, (70,  70, 70),   (screen_w/3 + 40, screen_h/4 + 40 + block_height*4,  screen_w/3 - 80, block_height - 20))
        screen.blit(exit_text, (screen_w/3 + 40 + (screen_w/3 - 80)/2 - exit_text.get_width()/2, screen_h/4 + 40 + block_height/2 - 20 - exit_text.get_height()/4 + block_height*4))
        if mouse_pos[0] > screen_w/3 + 40 and mouse_pos[0] < screen_w/3 + 40 + screen_w/3 - 80 and mouse_pos[1] > screen_h/4 + 40 + block_height*4 and mouse_pos[1] < screen_h/4 + 40 + block_height*5 - 20:
            pygame.draw.rect(screen, (60, 255, 255), (screen_w/3 + 40, screen_h/4 + 40 + block_height*4,  screen_w/3 - 80, block_height - 20), 2)
            if mouse_pressed[0]:
                runs = False
                running = False
                pygame.quit()
                sys.exit()
        else:
            pygame.draw.rect(screen, (100, 100, 100), (screen_w/3 + 40, screen_h/4 + 40 + block_height*4,  screen_w/3 - 80, block_height - 20), 2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
        pygame.display.update()

# The options menu
def options():
    options_screen_size = my_font_30.render("Change screen size: ", False, (255, 255, 255))
    size_800x600 = my_font_30.render("800x600", False, (255, 255, 255))
    size_1200x800 = my_font_30.render("1200x800", False, (255, 255, 255))
    size_1600x800 = my_font_30.render("1600x800", False, (255, 255, 255))
    size_1600x1000 = my_font_30.render("1600x1000", False, (255, 255, 255))
    size_fullscreen = my_font_30.render('Fullscreen', False, (255, 255, 255))
    
    audio_title = my_font_30.render("Master Volume", False, (255, 255, 255))

    global running
    global screen_w
    global screen_h
    global clock_tick
    
    options_init = True
    
    screen_size = False

    node_chosen = False
    node_x = ((screen_w/2 + 20) + (screen_w/2 + main_title.get_width()/2 - 10 - 20))/2
    
    while options_init:
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        screen.fill((40, 40, 40))

        # Options Title
        screen.blit(main_options, (screen_w/2 - main_options.get_width()/2, screen_h/6))

        # Screen size picker
        base_unit = pygame.Rect(screen_w/2 - main_title.get_width()/2, screen_h/3, main_title.get_width(), main_start.get_height())
        base_unit_height = main_start.get_height()
        pygame.draw.rect(screen, (50, 80, 80), base_unit)
        screen.blit(options_screen_size, (screen_w/2 - main_title.get_width()/2 + 10, screen_h/3 + options_screen_size.get_height()/2))
        pygame.draw.rect(screen, (255, 255, 255), base_unit, 3)

        # Back Button
        if mouse_pos[0] > 50 and mouse_pos[0] < 100 and mouse_pos[1] > 50 and mouse_pos[1] < 100:
             pygame.draw.rect(screen, (255, 80, 80), (50, 50, 50, 50))
             if mouse_pressed[0]:
                click.play()
                options_init = False
                pygame.display.update()
        else:
            pygame.draw.rect(screen, (50, 80, 80), (50, 50, 50, 50))
        pygame.draw.rect(screen, (255, 255, 255), (50, 50, 50, 50) , 2)
        pygame.draw.line(screen, (255, 255, 255), (60, 60), (90, 90), 3)
        pygame.draw.line(screen, (255, 255, 255), (60, 90), (90, 60), 3)

        # Audio Picker
        base_unit.y += base_unit_height
        pygame.draw.rect(screen, (50, 80, 80), base_unit)
        screen.blit(audio_title, (base_unit.x + 10, base_unit.y + audio_title.get_height()/2))
        pygame.draw.rect(screen, (255, 255, 255), base_unit, 3)

        node_y = base_unit.y + base_unit_height/2
        
        # Master Volume Bar
        pygame.draw.line(screen, (255, 255, 255), (screen_w/2 + 20, base_unit.y + base_unit_height/2), (screen_w/2 + main_title.get_width()/2 - 10 - 20, base_unit.y + base_unit_height/2), 4)
        if (sqrt(((mouse_pos[0] - node_x)**2) + ((mouse_pos[1] - node_y)**2)) < 10) or node_chosen:
            pygame.draw.circle(screen, (60, 255, 255), (node_x, node_y), 10)
            if mouse_pressed[0]:
                node_chosen = True
                if mouse_pos[0] > screen_w/2 + 20 and mouse_pos[0] < screen_w/2 + main_title.get_width()/2 - 10 - 20:
                    node_x = mouse_pos[0]
                    node_y = mouse_pos[1]
                    level1_song.set_volume(map((node_x - screen_w/2 + 20), 41, 268, 0, 1))
                    level2_song.set_volume(map((node_x - screen_w/2 + 20), 41, 268, 0, 1))
                    level3_song.set_volume(map((node_x - screen_w/2 + 20), 41, 268, 0, 1))
                    level4_song.set_volume(map((node_x - screen_w/2 + 20), 41, 268, 0, 1))
                    level5_song.set_volume(map((node_x - screen_w/2 + 20), 41, 268, 0, 1))
                    main_song.set_volume(map((node_x - screen_w/2 + 20), 41, 268, 0, 1))
                    rick.set_volume(map((node_x - screen_w/2 + 20), 41, 268, 0, 1))
            else:
                node_chosen = False
        else:
            pygame.draw.circle(screen, (200, 200, 200), (node_x, node_y), 10)
            node_chosen = False

        # Screen Size Picker
        if ((mouse_pos[0] > screen_w/2 and mouse_pos[0] < screen_w/2 + main_title.get_width()/2 - 10 and mouse_pos[1] > screen_h/3 + 10 and mouse_pos[1] < screen_h/3 + main_start.get_height() - 10) or screen_size) and node_chosen != True:
            if mouse_pos[0] > screen_w/2 and mouse_pos[0] < screen_w/2 + main_title.get_width()/2 - 10 and mouse_pos[1] > screen_h/3 + 10 and mouse_pos[1] < screen_h/3 + main_start.get_height()*5:
                screen_size = True
            else:
                screen_size = False
            pygame.draw.rect(screen, (50, 80, 80),    (screen_w/2, screen_h/3 + 10, main_title.get_width()/2 - 10, main_start.get_height()*5))
            pygame.draw.rect(screen, (255, 255, 255), (screen_w/2, screen_h/3 + 10, main_title.get_width()/2 - 10, main_start.get_height()*5), 2)
    
            # 800x600 Button
            if mouse_pos[0] > screen_w/2 and mouse_pos[0] < screen_w/2 + main_title.get_width()/2 - 10 and mouse_pos[1] > screen_h/3 + 10 and mouse_pos[1] < screen_h/3 + main_start.get_height() + 10:
                rect_800x600 = pygame.Rect(screen_w/2, screen_h/3 + 10, main_title.get_width()/2 - 10, main_start.get_height() + 2)
                pygame.draw.rect(screen, (60, 255, 255), rect_800x600, 2)
                if mouse_pressed[0]:
                    click.play()
                    screen_w = 800
                    screen_h = 600
                    pygame.display.set_mode((screen_w, screen_h))
                    pygame.mouse.set_pos(screen_w/2, screen_h/4)
                    node_x = ((screen_w/2 + 20) + (screen_w/2 + main_title.get_width()/2 - 10 - 20))/2
                    
            screen.blit(size_800x600, ((screen_w/2 +  (main_title.get_width()/2 - 10)/2 - size_800x600.get_width()/2), screen_h/3 + 10 + size_800x600.get_height()/2))

            # 1200x800 Button
            if mouse_pos[0] > screen_w/2 and mouse_pos[0] < screen_w/2 + main_title.get_width()/2 - 10 and mouse_pos[1] > screen_h/3 + 10 + main_start.get_height() and mouse_pos[1] < screen_h/3 + main_start.get_height()*2 + 10:
                rect_1200x800 = pygame.Rect(screen_w/2, screen_h/3 + 10 + main_start.get_height(), main_title.get_width()/2 - 10, main_start.get_height() + 2)
                pygame.draw.rect(screen, (60, 255, 255), rect_1200x800, 2)
                if mouse_pressed[0]:
                    click.play()
                    screen_w = 1200
                    screen_h = 800
                    pygame.display.set_mode((screen_w, screen_h))
                    pygame.mouse.set_pos(screen_w/2, screen_h/4)
                    node_x = ((screen_w/2 + 20) + (screen_w/2 + main_title.get_width()/2 - 10 - 20))/2
            screen.blit(size_1200x800, ((screen_w/2 +  (main_title.get_width()/2 - 10)/2 - size_1200x800.get_width()/2), screen_h/3 + 10 + size_1200x800.get_height()/2 + main_start.get_height()))
            
            # 1600x800 Button
            if mouse_pos[0] > screen_w/2 and mouse_pos[0] < screen_w/2 + main_title.get_width()/2 - 10 and mouse_pos[1] > screen_h/3 + 10 + main_start.get_height()*2 and mouse_pos[1] < screen_h/3 + main_start.get_height()*3 + 10:
                rect_1600x800 = pygame.Rect(screen_w/2, screen_h/3 + 10 + main_start.get_height()*2, main_title.get_width()/2 - 10, main_start.get_height() + 2)
                pygame.draw.rect(screen, (60, 255, 255), rect_1600x800, 2)
                if mouse_pressed[0]:
                    click.play()
                    screen_w = 1600
                    screen_h = 800
                    pygame.display.set_mode((screen_w, screen_h))
                    pygame.mouse.set_pos(screen_w/2, screen_h/4)
                    node_x = ((screen_w/2 + 20) + (screen_w/2 + main_title.get_width()/2 - 10 - 20))/2
            screen.blit(size_1600x800, ((screen_w/2 +  (main_title.get_width()/2 - 10)/2 - size_1600x800.get_width()/2), screen_h/3 + 10 + size_1600x800.get_height()/2 + main_start.get_height()*2))

            # 1600x1000 Button
            if mouse_pos[0] > screen_w/2 and mouse_pos[0] < screen_w/2 + main_title.get_width()/2 - 10 and mouse_pos[1] > screen_h/3 + 10 + main_start.get_height()*3 and mouse_pos[1] < screen_h/3 + main_start.get_height()*4 + 10:
                rect_1600x1000 = pygame.Rect(screen_w/2, screen_h/3 + 10 + main_start.get_height()*3, main_title.get_width()/2 - 10, main_start.get_height())
                pygame.draw.rect(screen, (60, 255, 255), rect_1600x1000, 2)
                if mouse_pressed[0]:
                    click.play()
                    screen_w = 1600
                    screen_h = 1000
                    pygame.display.set_mode((screen_w, screen_h))
                    pygame.mouse.set_pos(screen_w/2, screen_h/4)
                    node_x = ((screen_w/2 + 20) + (screen_w/2 + main_title.get_width()/2 - 10 - 20))/2
            screen.blit(size_1600x1000, ((screen_w/2 +  (main_title.get_width()/2 - 10)/2 - size_1600x1000.get_width()/2), screen_h/3 + 10 + size_1600x1000.get_height()/2 + main_start.get_height()*3))

            # Fullscreen Button
            if mouse_pos[0] > screen_w/2 and mouse_pos[0] < screen_w/2 + main_title.get_width()/2 - 10 and mouse_pos[1] > screen_h/3 + 10 + main_start.get_height()*4 and mouse_pos[1] < screen_h/3 + main_start.get_height()*5 + 10:
                rect_fullscreen = pygame.Rect(screen_w/2, screen_h/3 + 10 + main_start.get_height()*4, main_title.get_width()/2 - 10, main_start.get_height())
                pygame.draw.rect(screen, (60, 255, 255), rect_fullscreen, 2)
                if mouse_pressed[0]:
                    click.play()
                    pygame.display.set_mode((0,0), pygame.FULLSCREEN)
                    size = pygame.display.get_window_size()
                    screen_w = size[0]
                    screen_h = size[1]
                    pygame.mouse.set_pos(screen_w/2, screen_h/4)
                    node_x = ((screen_w/2 + 20) + (screen_w/2 + main_title.get_width()/2 - 10 - 20))/2
            screen.blit(size_fullscreen, ((screen_w/2 +  (main_title.get_width()/2 - 10)/2 - size_fullscreen.get_width()/2), screen_h/3 + 10 + size_fullscreen.get_height()/2 + main_start.get_height()*4))
        else:
            pygame.draw.rect(screen, (50, 80, 80), (screen_w/2, screen_h/3 + 10, main_title.get_width()/2 - 10, main_start.get_height() - 20))
            pygame.draw.rect(screen, (255, 255, 255), (screen_w/2, screen_h/3 + 10, main_title.get_width()/2 - 10, main_start.get_height() - 20), 2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    exit_menu()
        pygame.display.update()  

# Displaying the different levels
def levels():
    global running

    scale_w = screen_w/3 - 20 - 20
    levels_level1 = pygame.transform.smoothscale(pygame.image.load('Levels_BG/Levels_Level1.png'), (screen_w/5, screen_h/5))
    levels_level2 = pygame.transform.smoothscale(pygame.image.load('Levels_BG/Levels_Level2.png'), (screen_w/5, screen_h/5))

    levels_level1_text = my_font_30.render("Level 1", False, (255, 255, 255))
    levels_level2_text = my_font_30.render("Level 2", False, (255, 255, 255))

    levels_init = True
    while levels_init:
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        screen.fill((40, 40, 40))

        shift = 40

        # Level Images
        screen.blit(levels_level1, (shift + scale_w*0, shift))
        screen.blit(levels_level2, (shift + scale_w*1, shift))

        # Level Texts
        screen.blit(levels_level1_text, (shift + scale_w*0 + levels_level1.get_width()/2 - levels_level1_text.get_width()/2, levels_level1.get_height() + shift))
        screen.blit(levels_level2_text, (shift + scale_w*1 + levels_level2.get_width()/2 - levels_level2_text.get_width()/2, levels_level2.get_height() + shift))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    levels_init = False
                    exit_menu()
        pygame.display.update()

# The buttons in "main hub"
def buttons():

    global running
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()

    # Start Button
    if mouse_pos[0] > screen_w/2 - main_title.get_width()/2 and mouse_pos[0] < screen_w/2 - main_title.get_width()/2 + main_title.get_width() and mouse_pos[1] > screen_h/3 and mouse_pos[1] < screen_h/3 + main_start.get_height():
        pygame.draw.rect(screen, (255, 80, 80), (screen_w/2 - main_title.get_width()/2, screen_h/3, main_title.get_width(), main_start.get_height()))
        if mouse_pressed[0]:
            click.play()
            next_level(1)
    else:
        pygame.draw.rect(screen, (50, 80, 80), (screen_w/2 - main_title.get_width()/2, screen_h/3, main_title.get_width(), main_start.get_height()))
    screen.blit(main_start, (screen_w/2 - main_start.get_width()/2, screen_h/3))
    pygame.draw.rect(screen, (255, 255, 255), (screen_w/2 - main_title.get_width()/2, screen_h/3, main_title.get_width(), main_start.get_height()), 3)
     
    # Levels Button
    if mouse_pos[0] > screen_w/2 - main_title.get_width()/2 and mouse_pos[0] < screen_w/2 - main_title.get_width()/2 + main_title.get_width() and mouse_pos[1] > screen_h/3 + 100 and mouse_pos[1] < screen_h/3 + 100 + main_start.get_height():
        pygame.draw.rect(screen, (255, 80, 80), (screen_w/2 - main_title.get_width()/2, screen_h/3 + 100, main_title.get_width(), main_start.get_height()))
        if mouse_pressed[0]:
            click.play()
            levels()
    else:
        pygame.draw.rect(screen, (50, 80, 80), (screen_w/2 - main_title.get_width()/2, screen_h/3 + 100, main_title.get_width(), main_start.get_height()))
    screen.blit(main_levels, (screen_w/2 - main_levels.get_width()/2, screen_h/3 + 100))
    pygame.draw.rect(screen, (255, 255, 255), (screen_w/2 - main_title.get_width()/2, screen_h/3 + 100, main_title.get_width(), main_start.get_height()), 3)

    # Option Button
    if mouse_pos[0] > screen_w/2 - main_title.get_width()/2 and mouse_pos[0] < screen_w/2 - main_title.get_width()/2 + main_title.get_width() and mouse_pos[1] > screen_h/3 + 200 and mouse_pos[1] < screen_h/3 + 200 + main_start.get_height():
        pygame.draw.rect(screen, (255, 80, 80), (screen_w/2 - main_title.get_width()/2, screen_h/3 + 200, main_title.get_width(), main_start.get_height()))    
        if mouse_pressed[0]:
            click.play()
            options()
    else:
        pygame.draw.rect(screen, (50, 80, 80), (screen_w/2 - main_title.get_width()/2, screen_h/3 + 200, main_title.get_width(), main_start.get_height()))
    screen.blit(main_options, (screen_w/2 - main_options.get_width()/2, screen_h/3 + 200))
    pygame.draw.rect(screen, (255, 255, 255), (screen_w/2 - main_title.get_width()/2, screen_h/3 + 200, main_title.get_width(), main_start.get_height()), 3)

    # Exit Button
    if mouse_pos[0] > screen_w/2 - main_title.get_width()/2 and mouse_pos[0] < screen_w/2 - main_title.get_width()/2 + main_title.get_width() and mouse_pos[1] > screen_h/3 + 300 and mouse_pos[1] < screen_h/3 + 300 + main_start.get_height():
        pygame.draw.rect(screen, (255, 80, 80), (screen_w/2 - main_title.get_width()/2, screen_h/3 + 300, main_title.get_width(), main_start.get_height()))
        if mouse_pressed[0]:
            click.play()
            running = False
            pygame.quit()
            sys.exit()
    else:
        pygame.draw.rect(screen, (50, 80, 80), (screen_w/2 - main_title.get_width()/2, screen_h/3 + 300, main_title.get_width(), main_start.get_height()))
    screen.blit(main_exit, (screen_w/2 - main_exit.get_width()/2, screen_h/3 + 300))
    pygame.draw.rect(screen, (255, 255, 255), (screen_w/2 - main_title.get_width()/2, screen_h/3 + 300, main_title.get_width(), main_start.get_height()), 3)
    pygame.display.update()

# Main Loop
def main():

    global main_hub_BG
    global main_title
    global running

    clock.tick(clock_tick)

    main_hub_BG = pygame.transform.smoothscale(main_hub_BG, (screen_w, screen_h))
    screen.blit(main_hub_BG, (0,0))
    screen.blit(main_title, (screen_w/2 - main_title.get_width()/2, screen_h/6))

    buttons()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                exit_menu()  
    pygame.display.update()

clock = pygame.time.Clock()
running = True
click.set_volume(0.5)

# Game Loop
while running:
    main()