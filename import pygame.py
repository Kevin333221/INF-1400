import pygame

pygame.init()
pygame.font.init()

screen_w = 1400
screen_h = 800

screen = pygame.display.set_mode((screen_w, screen_h))

myfont = pygame.font.SysFont('Times New Roman', 60)
mytext = myfont.render("This is a text", False, (255, 255, 255))

def myfunc():
    # Her skjønner ikke python ha 'runs' er self om jeg har definert den i line 25
    while runs:

        screen.blit(mytext, (screen_w/2, screen_h/2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runs = False
    pygame.display.update()

runs = True
running = True

while running:

    myfunc()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    pygame.display.update()
    