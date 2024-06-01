import time
from pylsl import StreamInfo, StreamOutlet
import sys,os
import pygame, random, os, sys
import numpy as np      


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

def write(msg, colour=(30,144,255)):
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


def makeHighlighted(numtrials, oldhighlight=0):
    highlight = int(r[numtrials])
    newhighlight = highlight

    if highlight < 6:
        for i in range(rows):
            for j in range(columns):
                if i == highlight:
                    textsurface = write(grid[i][j], (255, 255, 100))
                else:
                    textsurface = write(grid[i][j])
                background.blit(textsurface, (length * j + length/4, vert[i]))

    else:
        for j in range(columns):
            for i in range(rows):
                if j == highlight - 6:
                    textsurface = write(grid[i][j], (255, 255, 100))
                else:
                    textsurface = write(grid[i][j])
                background.blit(textsurface, (length * j + length/4, vert[i]))

    screen.blit(background, (0, 0))
    pygame.display.flip()

    return newhighlight



    # for i in range (rows):
    #     if i == highlight:
    #         textsurface = write(grid[x],(255,255,100))
    #         background.blit(textsurface, (length * x + length/4,vert))
    #     else:
    #         textsurface = write(grid[x])
    #         background.blit(textsurface, (length * x + length/4, vert))


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