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






def offline(alphabet):
    # Set up LSL stream information
    info = StreamInfo('Markers', 'ImageMarkers', 1, 0, 'string', 'myuidw43536')
    outlet = StreamOutlet(info)

    # Initialize Pygame
    pygame.init()
    
    # Get display information
    info = pygame.display.Info()
    SIZE = WIDTH, HEIGHT = info.current_w, info.current_h
    print(WIDTH, HEIGHT)
    
    # Create Pygame screen and background surfaces
    screen = pygame.display.set_mode(SIZE)
    background = pygame.Surface((screen.get_size()))
    screenrect = screen.get_rect()
    backgroundrect = background.get_rect()
    
    # Fill the background with black
    background.fill((0, 0, 0))  # Black
    background = background.convert()
    
    # Clean the whole screen with the background
    screen.blit(background, (0, 0))
    
    # Initialize Pygame clock
    clock = pygame.time.Clock()
    
    # Main loop control variable
    mainloop = True
    
    # Frames per second (FPS)
    FPS = 2  # 2 FPS should give us epochs of 500 ms
    
    # Countdown timer
    countdown_seconds = 3
    countdown_font = pygame.font.SysFont("None", 90)
    
    # Display countdown timer and message
    for i in range(countdown_seconds, 0, -1):
        screen.fill((0, 0, 0))  # Black background
        countdown_text = countdown_font.render(f"Count the occurrence of letter: {alphabet} in {i} seconds", True, (255, 255, 255))
        screen.blit(countdown_text, (WIDTH // 2 - countdown_text.get_width() // 2, HEIGHT // 2 - countdown_text.get_height() // 2))
        pygame.display.flip()
        pygame.time.delay(1000)  # Delay for one second
        screen.blit(background, (0, 0))  # Clean the screen with the background
        pygame.display.flip()
    
    # Specify the grid content
    grid = "ABCDE"
    
    # Generate a random array for highlighted columns
    r = generate_random_array(block_length=5, block_count=10)
    arr = ['0', '1', '2', '3', '4']
    
    # Define grid properties
    columns = len(grid)
    length = screenrect.width / columns
    y = screenrect.height
    vert = 3 * y / 8
    oldhighlight = 0
    
    # Number of trials counter
    numtrials = 0
    
    # Function to write letters on the screen
    def write(msg, colour=(30, 144, 255)):
        myfont = pygame.font.SysFont("None", 90)
        mytext = myfont.render(msg, True, colour)
        mytext = mytext.convert_alpha()
        return mytext
    
    # Function to generate an uncolored frame with the grid letters
    def makeStandard():
        for x in range(columns):
            textsurface = write(grid[x])
            background.blit(textsurface, (length * x + length / 4, vert))
        screen.blit(background, (0, 0))
        pygame.display.flip()
    
    # Function to generate a colored frame with a random colored column or row
    def makeHighlighted(numtrials, oldhighlight=0):
        highlight = int(arr[r[numtrials]])
        newhighlight = highlight
    
        for x in range(columns):
            if x == highlight:
                textsurface = write(grid[x], (255, 255, 100))
                background.blit(textsurface, (length * x + length / 4, vert))
            else:
                textsurface = write(grid[x])
                background.blit(textsurface, (length * x + length / 4, vert))
    
        return newhighlight
    
    # Main loop for the Pygame interface
    while mainloop:
        milliseconds = clock.tick(FPS)  # Milliseconds passed since the last frame
        seconds = milliseconds / 1000.0  # Seconds passed since the last frame
        
        # Check for Pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainloop = False  # Pygame window closed by the user
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    mainloop = False  # User pressed ESC
        
        # Check if the number of trials is reached
        if numtrials == 50:
            pygame.quit()
            break
        else:
            # Generate and display a standard frame
            makeStandard()
            
            # Generate and display a highlighted frame
            oldhighlight = makeHighlighted(numtrials, oldhighlight)
            
            # Clean the whole screen with the background
            screen.blit(background, (0, 0))
            pygame.display.flip()
            
            # Push LSL marker indicating the highlighted letter
            outlet.push_sample([str(oldhighlight + 1)])
    
            # Print information about the highlighted letter
            print('--------------')
            print(str(oldhighlight + 1))
            print('--------------')
    
            # Increment the trial counter
            numtrials += 1
