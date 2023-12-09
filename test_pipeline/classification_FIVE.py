#!/usr/bin/env python
# coding: utf-8

# In[74]:


import scipy.io as sio
import numpy as np
import matplotlib.pyplot as plt
import sys
from udp_client_python import send_data
import pygame, random, os, sys
import time
import socket



filename = sys.argv[1]


letters=['A','B','C','D','E']

mat_contents = sio.loadmat('mat_files/'+filename+'.mat')
# d = mat_contents['ALLERP']['bindata'][0][0][3]
d = mat_contents['bindata'][3]

b=[]
for j in range(5):
  temp = []
  for i in range(400,550):
    temp.append(d[i][2*j]-d[i][2*j+1])
  b.append(temp)

###########peak_array############
peak_array = []
for i in range(5):
  peak_array.append(max(b[i]))

peak_array = np.array(peak_array)

res = peak_array.argsort()[-4:][::-1]
# res = peak_array.argsort()[:4]
print(res)
# print('peak_array',peak_array)

# letters = ['A','C','E','D','B']
for i in range(len(res)):
    print(letters[res[i]],end="  ")
print('\n')
###########avg_array###########

# avg_array = []
# for i in range(5):
#   avg_array.append(sum(b[i])/400) 
# # print('avg_array',avg_array)

# avg_array = np.array(avg_array)

# res = avg_array.argsort()[-4:][::-1]
# print(res)

# for i in range(len(res)):
#     print(letters[res[i]],end="  ")
# msg=letters[res[0]] + ', ' + letters[res[1]] + ', ' + letters[res[2]]
msg=letters[res[0]] 
# msg = 'B'
print(msg)
ip = "192.168.203.130"
port = 4444

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((ip, port))
    s.sendall(msg.encode('utf-8'))
    # data = s.recv(1024)

# print(f"Received {data!r}")


# s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
# # while True:
# s.sendto(msg.encode('utf-8'), (ip,port))
# print("\n\n 1. Client Sent : ", msg, "\n\n")
# # close the socket
# s.close()


pygame.init()
 

white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
pygame.init() #start pygame
info = pygame.display.Info()
SIZE = WIDTH, HEIGHT = info.current_w, info.current_h
print(WIDTH, HEIGHT)
# flags = pygame.DOUBLEBUF | pygame.FULLSCREEN
display_surface = pygame.display.set_mode(SIZE)
# background = pygame.Surface((screen.get_size()))
X = WIDTH
Y = HEIGHT
 
# display_surface = pygame.display.set_mode((X, Y))
 
# set the pygame window name
msg = 'Your goal is ' + letters[res[0]] + ', ' + letters[res[1]] + ', ' + letters[res[2]]
pygame.display.set_caption('Show Text')
font = pygame.font.Font('freesansbold.ttf', 32)
text = font.render(msg, True, green, blue)
textRect = text.get_rect()
textRect.center = (X // 2, Y // 2)
 
# infinite loop
while True:
 

    display_surface.fill(white)
    display_surface.blit(text, textRect)
    for event in pygame.event.get():
 
  
        if event.type == pygame.QUIT:
             pygame.quit()
             quit()
        # Draws the surface object to the screen.
        pygame.display.update()