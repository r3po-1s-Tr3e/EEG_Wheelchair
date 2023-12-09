#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import time
import sys,os
import pygame, random, os, sys
import numpy as np      
from psychopy import core, parallel

goal = 'D'
msg = 'The goal selected is '+goal
pygame.init() #start pygame

#specify screen and background sizes
screen = pygame.display.set_mode((400,300))
screenrect = screen.get_rect()
background = pygame.Surface((screen.get_size()))
backgroundrect = background.get_rect()
background.fill((0,0,0)) # black
background = background.convert()
screen.blit(background, (0,0)) # clean whole screen

clock = pygame.time.Clock()
mainloop = True
FPS = 2 # 2 FPS should give us epochs of 500 ms

x = screenrect.width
y = screenrect.height
vert = 3*y/8
hori = x/16

#we will use this function to write the letters
def write(msg, colour=(30,144,255),size=90):
    myfont = pygame.font.SysFont("None", size)
    mytext = myfont.render(msg, True, colour)
    mytext = mytext.convert_alpha()
    return mytext




textsurface = write(msg)
background.blit(textsurface, (hori,vert ))
screen.blit(background, (0,0))
pygame.display.flip()


core.wait(10.005)



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

 


