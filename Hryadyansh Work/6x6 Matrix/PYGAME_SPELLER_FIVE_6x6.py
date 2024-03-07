from pylsl import StreamInfo, StreamOutlet
import sys,os
import pygame, random, os, sys
import numpy as np      
import time
# from psychopy import core, parallel

# def_col = (30, 144, 255)  # Default color 
def_col = (128, 128, 128)  # Default color 
ill_col = (255, 255, 100)  # Illumination color 

timeout = 50

# timeout_start = time.time()

 #### generate random array in blocks withoout consecutive repetitions
def generate_random_array(block_length, block_count):
    randoms_array = []
    i = 0
    for blocks in range(0, block_count):
        nums = np.arange(block_length)
        np.random.shuffle(nums)
        if i%2 == 0:
            nums = nums
        else:
            nums = nums + 6
        randoms_array.extend(nums)
        i += 1
    return randoms_array
    
    
def offline(alphabet):
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
    FPS = 10  # Change the FPS to 10 for 100 ms highlight and 400 ms no illumination

    countdown_seconds = 5
    countdown_font = pygame.font.SysFont("None", 90)
    instruction_font = pygame.font.SysFont("None", 50)

    # Display countdown timer and message
    for i in range(countdown_seconds, 0, -1):
        screen.fill((0, 0, 0))  # Black background


        # Countdown timer
        countdown_text = countdown_font.render(f"Count the occurrence of letter: {alphabet} in {i} seconds",
                                               True, (255, 255, 255))
        screen.blit(countdown_text, (WIDTH // 2 - countdown_text.get_width() // 2,
                                     HEIGHT // 2 - countdown_text.get_height() // 2 - 30))

        # Instruction line
        instruction_text = instruction_font.render('Press "D" when you see, alphabet ' + alphabet,
                                                   True, (255, 255, 255))
        screen.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2,
                                       HEIGHT // 2 + instruction_text.get_height()))

        pygame.display.flip()
        pygame.time.delay(1000)  # Delay for one second
        screen.blit(background, (0, 0))  # Clean the screen with the background
        pygame.display.flip()


    #specify the grid content
    grid = [
    ['A', 'B', 'C', 'D', 'E', 'F'],
    ['G', 'H', 'I', 'J', 'K', 'L'],
    ['M', 'N', 'O', 'P', 'Q', 'R'],
    ['S', 'T', 'U', 'V', 'W', 'X'],
    ['Y', 'Z', '1', '2', '3', '4'],
    ['5', '6', '7', '8', '9', '0']
    ]

    
    r = generate_random_array(block_length=6, block_count=10)


    columns  = len(grid[0])
    rows = len(grid[1])
    length = screenrect.width / columns
    y = screenrect.height
    vert = []
    for i in  range(rows):
        vert.append(round(y/7*(i+1)))
    oldhighlight = 0

    numtrials = 0
 
    #we will use this function to write the letters
    def write(msg, colour=def_col):
        myfont = pygame.font.SysFont("None", 90)
        mytext = myfont.render(msg, True, colour)
        mytext = mytext.convert_alpha()
        return mytext

   
    #generate uncoloured frame
    def makeStandard():
        for j in range(columns):
            for i in range(rows):
                textsurface = write(grid[i][j])
                background.blit(textsurface, (length * j + length/4,vert[i]))
                screen.blit(background, (0,0))
                pygame.display.flip()


    #generate a coloured random coloured column or row
    # def makeHighlighted(numtrials,oldhighlight=0):
    #     highlight = int(r[numtrials])
    #     newhighlight = highlight

    #     for x in range (columns):
    #         if x == highlight:
    #             textsurface = write(grid[x],(255,255,100))
    #             background.blit(textsurface, (length * x + length/4,vert))
    #         else:
    #             textsurface = write(grid[x])
    #             background.blit(textsurface, (length * x + length/4, vert))

    #     # core.wait(0.0001)
       
    #     return(newhighlight)
    
    def makeHighlighted(numtrials, oldhighlight=0):
        highlight = int(r[numtrials])
        newhighlight = highlight

        if highlight < 6:
            for i in range(rows):
                for j in range(columns):
                    if i == highlight:
                        textsurface = write(grid[i][j], ill_col)
                    else:
                        textsurface = write(grid[i][j])
                    background.blit(textsurface, (length * j + length/4, vert[i]))
                
        else:
            for j in range(columns):
                for i in range(rows):
                    if j == highlight - 6:
                        textsurface = write(grid[i][j], ill_col)
                    else:
                        textsurface = write(grid[i][j])
                    background.blit(textsurface, (length * j + length/4, vert[i]))

        screen.blit(background, (0, 0))
        pygame.display.flip()

        time.sleep(0.1)  # Illumination period of 100 ms

        makeStandard()  # No illumination for 400 ms

        screen.blit(background, (0, 0))
        pygame.display.flip()

        time.sleep(0.4)  # No illumination period of 400 ms

        return newhighlight

    #pygame uses a main loop to generate the interface
    makeStandard()  # Display the matrix with default color
    screen.blit(background, (0, 0))
    pygame.display.flip()
    time.sleep(2)  # 2 second window with no illumination
    while mainloop:

        milliseconds = clock.tick(FPS)  # milliseconds passed since last frame
        seconds = milliseconds / 1000.0 # seconds passed since last frame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainloop = False # pygame window closed by user
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    mainloop = False # user pressed ESC

        if numtrials == 60:
            pygame.quit()
            break

        else:
            makeStandard()
            oldhighlight = makeHighlighted(numtrials,oldhighlight)

            screen.blit(background, (0,0)) # clean whole screen
            pygame.display.flip()
            outlet.push_sample([str(oldhighlight+1)])

            print('--------------')
            print(str(oldhighlight+1))
            print('--------------')

            numtrials += 1

            if (numtrials)%6 == 0:
                time.sleep(1)  # Change the delay to 0.4 seconds for no illumination

        