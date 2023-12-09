#!/usr/bin/env python
# coding: utf-8

# In[2]:


import time
# from pylsl import StreamInfo, StreamOutlet
import sys,os
import pygame, random, os, sys
import numpy as np      
#we will borrow PsychoPy's parallel feature to record stimulus timings using the parallel port
from psychopy import core, parallel
#parallel.setPortAddress(61432) #61432 is the lab port address

# time.sleep(1)

# time.sleep(10)
# outlet.push_sample(['LSLStarted',str(111),str(111)])

# time.sleep(1)
timeout = 75

timeout_start = time.time()
# outlet.push_sample(['About to Start',str(999)])

 #### generate random array withoout consecutive repetitions
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
    # info = StreamInfo('Markers', 'ImageMarkers', 1, 0, 'string', 'myuidw43536')
    # outlet = StreamOutlet(info)

    pygame.init() #start pygame

    #specify screen and background sizes
    screen = pygame.display.set_mode((800,800))
    screenrect = screen.get_rect()
    background = pygame.Surface((screen.get_size()))
    backgroundrect = background.get_rect()
    background.fill((0,0,0)) # black
    background = background.convert()
    screen.blit(background, (0,0)) # clean whole screen

    clock = pygame.time.Clock()
    mainloop = True
    FPS = 2 # 2 FPS should give us epochs of 500 ms

    #specify the grid content
    grid = ["      ",
            "ABCDEF",
            "GHIJKL",
            "MNOPQR",
            "STUVWX",
            "YZ1234",
            "56789_"]
#     grid = ["ABCDEF",
#             "GHIJKL",
#             "MNOPQR",
#             "STUVWX",
#             "YZ1234",
#             "56789_"]

    phrase = "" #this is used to store the string at the bottom of the interface

    lines = len(grid)
    columns = len(grid[0])
    r = generate_random_array(block_length=12, block_count=10)
    arr = ['01','02','03','04','05','06','10','11','12','13','14','15']


    length = screenrect.width / columns
    height = screenrect.height / lines

    oldhighlight = 0

    numtrials = 0
#     targets = [[1,1],[3,5],[1,0],[2,2],[3,1],[4,0],[6,5]]
    targets=[[1,1]]
    targetcounter = 0

    waittime = 3000

    #we will use this function to write the letters
    def write(msg, colour=(30,144,255)):
        myfont = pygame.font.SysFont("None", 90)
        mytext = myfont.render(msg, True, colour)
        mytext = mytext.convert_alpha()
        return mytext

    #use this function to write the spelled phrase
    def writePhrase():
        for z in range(len(phrase)):
            textsurface = write(phrase[z], (255,255,255))
            background.blit(textsurface, (length * z + length/4, height * 5 + height/4))

    #generate uncoloured frame
    def makeStandard():
        for y in range(lines):
            for x in range(columns):
                textsurface = write(grid[y][x])
                background.blit(textsurface, (length * x + length/4, height * (y-1) + height/4))

        writePhrase()
        screen.blit(background, (0,0))
        pygame.display.flip()

   

    #this function makes a makes a target
    def makeTarget(target):
        for y in range(lines):
            for x in range(columns):
                if y == target[0] and x == target[1]:
                    textsurface = write(grid[y][x],(255,0,0))
                    background.blit(textsurface, (length * x + length/4, height * (y-1) + height/4))
                else:
                    textsurface = write(grid[y][x])
                    background.blit(textsurface, (length * x + length/4, height * (y-1) + height/4))
        writePhrase()

    #generate a coloured random coloured column or row
    def makeHighlighted(target, numtrials,oldhighlight=0):
        rowcol = int(arr[r[numtrials]][0])
        highlight = int(arr[r[numtrials]][1])

        newhighlight = highlight

        for y in range(lines):
            for x in range (columns):
                if rowcol == 0: #highlight a row
                    if y == highlight:
                        textsurface = write(grid[y][x],(255,255,100))
                        background.blit(textsurface, (length * x + length/4, height * (y-1) + height/4))
                    else:
                        textsurface = write(grid[y][x])
                        background.blit(textsurface, (length * x + length/4, height * (y-1) + height/4))
                else: #highlight a column
                    if x == highlight:
                        textsurface = write(grid[y][x],(255,255,100))
                        background.blit(textsurface, (length * x + length/4, height * (y-1) + height/4))
                    else:
                        textsurface = write(grid[y][x])
                        background.blit(textsurface, (length * x + length/4, height * (y-1) + height/4))

        writePhrase()

        #record on the parallel port; test to see if row is the same as target
        if rowcol == 0: #if it is a row
            if target[0] == highlight:
                #parallel.setData(2) #this is the target; record it in the parallel
#                 print(highlight)
#                 print(target)
#                 print(str(numtrials)," **target row")
                core.wait(0.005)
                #parallel.setData(0)
            else:
                #parallel.setData(1) #this is not the target
#                 print(highlight)
#                 print(target)
#                 print(str(numtrials),  " row")
                core.wait(0.005)
                #parallel.setData(0)
        else: #it is a column
            if target[1] == highlight:
                #parallel.setData(2) #this is the target; record it in the parallel
#                 print(highlight)
#                 print(target)
#                 print(str(numtrials)," **target column")
                core.wait(0.005)
                #parallel.setData(0)
            else:
                #parallel.setData(1) #this is not the target
#                 print(highlight)
#                 print(target)
#                 print(str(numtrials)," column")
                core.wait(0.005)
                #parallel.setData(0)

        return(newhighlight,rowcol)

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

        if time.time() > timeout_start + timeout:
            break
  
        if targetcounter < len(targets):
            if numtrials == 0:
                makeTarget(targets[targetcounter])
                screen.blit(background, (0,0)) #clean whole screen
                pygame.display.flip()
#                 outlet.push_sample(['New_letter',str(targetcounter),str(111)])

                pygame.time.wait(waittime)
                numtrials += 1
            elif numtrials == 120:
                targetcounter += 1
                numtrials = 0
            else:
                makeStandard()
                oldhighlight,rowcolumn = makeHighlighted(targets[targetcounter], numtrials,oldhighlight)

                screen.blit(background, (0,0)) # clean whole screen
                pygame.display.flip()
#                 outlet.push_sample(['Highlight',str(rowcolumn)+str(oldhighlight),str(111)])
                # outlet.push_sample([str(rowcolumn)+str(oldhighlight)])

                print('--------------')
                print(str(rowcolumn)+str(oldhighlight))
                print('--------------')

                numtrials += 1

        
    pygame.quit()

            

# #currently the scripts are written to be run as standalone
# #routines. We should change these to work in conjunction once we get
# # #the classifiers working sometime in the future.
if __name__=="__main__":
    offline()












