import time
from pylsl import StreamInfo, StreamOutlet
import sys,os
import pygame, random, os, sys
import numpy as np      
# from psychopy import core, parallel



timeout = 32

# timeout_start = time.time()

 #### generate random array in blocks withoout consecutive repetitions
def generate_random_array(block_length, block_count):
    for blocks in range(0, block_count):
        nums = np.arange(block_length)
        np.random.shuffle(nums)
        try:
            if nums[0] == randoms_array [-1]:
                nums[0], nums[-1] = nums[-1], nums[0]
        except NameError:
            randoms_array = []
        randoms_array.extend(nums)
    return randoms_array
    
    
def offline():
    info = StreamInfo('Markers', 'ImageMarkers', 1, 0, 'string', 'myuidw43536')
    outlet = StreamOutlet(info)

    pygame.init() #start pygame
    info = pygame.display.Info()
    SIZE = WIDTH, HEIGHT = info.current_w, info.current_h
    print(WIDTH, HEIGHT)
    # flags = pygame.DOUBLEBUF | pygame.FULLSCREEN
    screen = pygame.display.set_mode(SIZE)
    background = pygame.Surface((screen.get_size()))
    # #specify screen and background sizes
    # screen = pygame.display.set_mode((400,300))
    screenrect = screen.get_rect()
    # background = pygame.Surface((screen.get_size()))
    backgroundrect = background.get_rect()
    background.fill((0,0,0)) # black
    background = background.convert()
    screen.blit(background, (0,0)) # clean whole screen

    clock = pygame.time.Clock()
    mainloop = True
    FPS = 2 # 2 FPS should give us epochs of 500 ms

    #specify the grid content
    grid = "ABCDE"
    
    r = generate_random_array(block_length=5, block_count=10)
    arr = ['0','1','2','3','4']



    columns  = len(grid)
    length = screenrect.width / columns
    y = screenrect.height
    vert = 3*y/8
    oldhighlight = 0

    numtrials = 0
 
    #we will use this function to write the letters
    def write(msg, colour=(30,144,255)):
        myfont = pygame.font.SysFont("None", 90)
        mytext = myfont.render(msg, True, colour)
        mytext = mytext.convert_alpha()
        return mytext

   
    #generate uncoloured frame
    def makeStandard():
        for x in range(columns):
            textsurface = write(grid[x])
            background.blit(textsurface, (length * x + length/4,vert ))
        screen.blit(background, (0,0))
        pygame.display.flip()


    #generate a coloured random coloured column or row
    def makeHighlighted(numtrials,oldhighlight=0):
        highlight = int(arr[r[numtrials]])
        newhighlight = highlight

        for x in range (columns):
            if x == highlight:
                textsurface = write(grid[x],(255,255,100))
                background.blit(textsurface, (length * x + length/4,vert))
            else:
                textsurface = write(grid[x])
                background.blit(textsurface, (length * x + length/4, vert))

        # core.wait(0.0001)
       
        return(newhighlight)

    #pygame uses a main loop to generate the interface
    while mainloop:
        milliseconds = clock.tick(FPS)  # milliseconds passed since last frame
        seconds = milliseconds / 1000.0 # seconds passed since last frame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainloop = False # pygame window closed by user
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    mainloop = False # user pressed ESC

        if numtrials == 50:
            pygame.quit()
            break

        else:
            makeStandard()
            oldhighlight = makeHighlighted( numtrials,oldhighlight)

            screen.blit(background, (0,0)) # clean whole screen
            pygame.display.flip()
            outlet.push_sample([str(oldhighlight+1)])

            print('--------------')
            print(str(oldhighlight+1))
            print('--------------')

            numtrials += 1





