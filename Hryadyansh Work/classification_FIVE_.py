#!/usr/bin/env python
# coding: utf-8

import mne
import numpy as np
import sys
import socket
import pygame


epochs = mne.read_epochs(r"C:\Users\hryad\Desktop\iitm\BCI Wheelchair\EEG_Wheelchair - Copy\test_pipeline\mat_files\rishi_e2-epo.fif")

non_a_target = epochs['3','2','4','5']
a_epoch = epochs['1']

non_b_target = epochs['1','3','4','5']
b_epoch = epochs['2']



non_c_target = epochs['1','2','4','5']
c_epoch = epochs['3']

non_d_target = epochs['1','2','4','3']
d_epoch = epochs['4']

non_e_target = epochs['1','2','4','3']
e_epoch = epochs['5']

avg_a = a_epoch.average()
avg_non_a = non_a_target.average()
avg_b = b_epoch.average()
avg_non_b = non_b_target.average()
avg_c = c_epoch.average()
avg_non_c = non_c_target.average()
avg_d = d_epoch.average()
avg_non_d = non_d_target.average()
avg_e = e_epoch.average()
avg_non_e = non_e_target.average()


a_data = avg_a.data[-3][list(avg_a.times).index(0.2):list(avg_a.times).index(0.6)]
non_a_data = avg_non_a.data[-3][list(avg_non_a.times).index(0.2):list(avg_non_a.times).index(0.6)]
b_data = avg_b.data[-3][list(avg_b.times).index(0.2):list(avg_b.times).index(0.6)]
non_b_data = avg_non_b.data[-3][list(avg_non_b.times).index(0.2):list(avg_non_b.times).index(0.6)]
c_data = avg_c.data[-3][list(avg_c.times).index(0.2):list(avg_c.times).index(0.6)]
non_c_data = avg_non_c.data[-3][list(avg_non_c.times).index(0.2):list(avg_non_c.times).index(0.6)]
d_data = avg_d.data[-3][list(avg_d.times).index(0.2):list(avg_d.times).index(0.6)]
non_d_data = avg_non_d.data[-3][list(avg_non_d.times).index(0.2):list(avg_non_d.times).index(0.6)]
e_data = avg_e.data[-3][list(avg_e.times).index(0.2):list(avg_e.times).index(0.6)]
non_e_data = avg_non_e.data[-3][list(avg_non_e.times).index(0.2):list(avg_non_e.times).index(0.6)]

# print("A diff non A: ",np.mean(a_data)-np.mean(non_a_data))
# print("B diff non B: ",np.mean(b_data)-np.mean(non_b_data))
# print("C diff non C: ",np.mean(c_data)-np.mean(non_c_data))
# print("D diff non D: ",np.mean(d_data)-np.mean(non_d_data))
# print("E diff non E: ",np.mean(e_data)-np.mean(non_e_data))

a_diff_non_a = np.mean(a_data)-np.mean(non_a_data)
b_diff_non_b = np.mean(b_data)-np.mean(non_b_data)
c_diff_non_c = np.mean(c_data)-np.mean(non_c_data)
d_diff_non_d = np.mean(d_data)-np.mean(non_d_data)
e_diff_non_e = np.mean(e_data)-np.mean(non_e_data)

print("A diff non A: ",a_diff_non_a)
print("B diff non B: ",b_diff_non_b)
print("C diff non C: ",c_diff_non_c)
print("D diff non D: ",d_diff_non_d)
print("E diff non E: ",e_diff_non_e)

diff_dict = {'A':a_diff_non_a,'B':b_diff_non_b,'C':c_diff_non_c,'D':d_diff_non_d,'E':e_diff_non_e}

for i in diff_dict:
    if diff_dict[i] == max(diff_dict.values()):
        print("The letter is: ",i)
        

# # Define your letters and their corresponding event_ids here
# letters = ['A', 'B', 'C', 'D', 'E']
# event_ids = {letter: i+1 for i, letter in enumerate(letters)}

# # Get the filename from command line arguments
# filename = 'erp-ave'

# # Read the epochs from the .fif file
# # epochs= mne.read_epochs(r"C:\Users\hryad\Desktop\iitm\BCI Wheelchair\EEG_Wheelchair - Copy\test_pipeline\mat_files\rishi_A-epo.fif")
# # Load the epochs from the saved FIF file
# epochs = mne.read_epochs(r"C:\Users\hryad\Desktop\iitm\BCI Wheelchair\EEG_Wheelchair - Copy\test_pipeline\mat_files\rishi_A-epo.fif")



# # Initialize an empty list to hold peak values for each letter
# peak_array = []

# # Loop through each letter, extract the data for that condition,
# # and calculate the peak of the average response
# for letter in letters:
#     # Extract the data for the current letter
#     data = epochs[event_ids[letter]].get_data()
    
#     # Calculate the average response across epochs for each channel
#     avg_response = data.mean(axis=0)
    
#     # Find the peak of the average response
#     peak = avg_response.max()
#     peak_array.append(peak)

# # Convert the list to a NumPy array for further processing
# peak_array = np.array(peak_array)

# # Get the indices of the letters with the top responses
# top_indices = peak_array.argsort()[-4:][::-1]
# print(peak_array)
# # Print the letters with the top responses
# for i in top_indices:
#     print(letters[i], end="  ")
# print('\n')

# # Send the top response to a server via a socket
# msg = letters[top_indices[0]]
# ip = "192.168.203.130"
# port = 4444

# # Establish a socket connection and send the message
# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.connect((ip, port))
#     s.sendall(msg.encode('utf-8'))

# # Initialize Pygame for display
# pygame.init()
# info = pygame.display.Info()
# SIZE = WIDTH, HEIGHT = info.current_w, info.current_h
# display_surface = pygame.display.set_mode(SIZE)

# # Define text properties
# white = (255, 255, 255)
# green = (0, 255, 0)
# blue = (0, 0, 128)
# font = pygame.font.Font('freesansbold.ttf', 32)
# msg = f'Your goal is {", ".join(letters[i] for i in top_indices)}'
# text = font.render(msg, True, green, blue)
# textRect = text.get_rect()
# textRect.center = (WIDTH // 2, HEIGHT // 2)

# # Event loop to keep the display running
# while True:
#     display_surface.fill(white)
#     display_surface.blit(text, textRect)
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()
#     pygame.display.update()
