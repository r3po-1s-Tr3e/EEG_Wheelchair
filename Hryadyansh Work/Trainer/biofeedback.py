import sys
import mne
import numpy as np
import pyxdf
import bisect
import pygame
import sys
import matplotlib.pyplot as plt

# Adjustable variables
low_cutoff = 0.1
high_cutoff = 15 
EPOCHS_TIMING = (-0.2, 0.8)

name = sys.argv[1]
alphabet = sys.argv[2]
trial = sys.argv[3]

# name = 'sanat'
# alphabet = 'C'
# trial = '2'

# Paths to your files   
data_file = f"LabRecorder/{name}_{alphabet}_{trial}.xdf"

# Load the XDF file
streams, _ = pyxdf.load_xdf(data_file)
eeg_stream = streams[1]
ch_names = []
for i in range(len(eeg_stream['info']['desc'][0]['channels'][0]['channel'])):
    ch_names.append(eeg_stream['info']['desc'][0]['channels'][0]['channel'][i]['label'][0])

sfreq = float(eeg_stream['info']['nominal_srate'][0])
info = mne.create_info(ch_names=ch_names, sfreq=sfreq, ch_types='eeg')
data = np.array(eeg_stream['time_series']).T
print("eeg stream keys:", eeg_stream.keys())
raw = mne.io.RawArray(data, info)

# Setting montage
ch_coordinates = {
    'Fp1': [-37, 5, 55],
    'Fp2': [37, 5, 55],
    'Fz': [0, 5, 90],
    'C3': [-45, 5, 20],
    'C4': [45, 5, 20],
    'Pz': [0, -30, 20],  
    'O1': [-20, -100, 5],   
    'O2': [20, -100, 5]   
}
ch_positions = np.array([ch_coordinates[name] for name in ch_names])

montage = mne.channels.make_dig_montage(ch_coordinates, coord_frame='head')
raw.set_montage(montage=montage)

# Apply the bandpass filter
raw.filter(low_cutoff, high_cutoff, fir_design='firwin')

# Read events and create epochs
marker_stream = streams[0]
event_codes = [int(event[0]) if event[0] else 0 for event in marker_stream['time_series']] # Using zero as a placeholder
event_timestamps = marker_stream['time_stamps']
event_samples = (event_timestamps ) 
#event_samples = ((event_timestamps ) - event_timestamps[0]*sfreq).astype(int)
# Filter out '0' placeholders from the events
valid_events_mask = [event != 0 for event in event_codes]
filtered_event_codes = [event for event, mask in zip(event_codes, valid_events_mask) if mask]
filtered_event_timestamps = [timestamp for timestamp, mask in zip(marker_stream['time_stamps'], valid_events_mask) if mask]
#event_samples = ((np.array(filtered_event_timestamps) ) - event_timestamps[0] ).astype(int)
event_samples = (np.array(filtered_event_timestamps)*sfreq ).astype(int)


# Save the ERP data, adjust the filename and path as needed
def find_nearest_index(sorted_list, target):
    index = bisect.bisect_left(sorted_list, target)
    if index == 0:
        return 0
    if index == len(sorted_list):
        return len(sorted_list) - 1
    before = sorted_list[index - 1]
    after = sorted_list[index]
    if after - target < target - before:
        return index
    else:
        return index - 1
    
nearest_indices = [find_nearest_index(list(np.array(eeg_stream['time_stamps']).T), element) for element in event_timestamps]
print("Nearest indices in list A for elements in list B:")
print(nearest_indices)

if len(nearest_indices) == len(filtered_event_codes):
    events = np.column_stack((nearest_indices, np.zeros_like(nearest_indices), filtered_event_codes)).astype(int)
else:
    diff = len(nearest_indices) - len(filtered_event_codes)
    events = np.column_stack((nearest_indices[:-diff], np.zeros_like(nearest_indices[:-diff]), filtered_event_codes)).astype(int)
# print(events)
# events = np.column_stack((nearest_indices[:-1], np.zeros_like(nearest_indices[:-1]), filtered_event_codes)).astype(int)

# Create epochs
epochs = mne.Epochs(raw, events, tmin=EPOCHS_TIMING[0], tmax=EPOCHS_TIMING[1], preload=True)
print(epochs)
# Average epochs to create ERP

# Save the epochs to a FIF file
epochs_filename = f"Epoch Files/{name}_{alphabet}_{trial}-epo.fif"
epochs.save(epochs_filename, overwrite=True)

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
        predicted_letter = i
        print("The letter is: ",i)

if predicted_letter == alphabet:
    Pygame_print_1 = 'Our systems show that you indeed focused on the letter ' + alphabet + ' during the trial.'
    Pygame_print_2 = 'Well done!'
else:
    Pygame_print_1 = 'Our systems show that you did not focus on the letter ' + alphabet + ' during the trial.' 
    Pygame_print_2 = 'Please try again.'
# Initialize Pygame
pygame.init()

# Set the screen size
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Set the colors
black = (0, 0, 0)
white = (255, 255, 255)

# Set the font
yellow = (255, 255, 0)  # Define the "yellow" color

font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

# Set the text
text = font.render(Pygame_print_1, True, yellow)
text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
text_2 = font.render(Pygame_print_2, True, yellow)
text_rect_2 = text.get_rect(center=(screen_width // 2, screen_height // 2))

# Set the "Press Enter to Continue" text
continue_text = small_font.render("Press Enter to Continue", True, white)
continue_text_rect = continue_text.get_rect(center=(screen_width // 2, screen_height // 2 + 50))
# Set the screen size
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# ...

# Main loop
running = True
while running:
    # Fill the screen with black color
    screen.fill(black)

    # Draw the text on the screen
    screen.blit(text, text_rect)
    screen.blit(text_2, text_rect_2)
    screen.blit(continue_text, continue_text_rect)

    # Update the display
    pygame.display.flip()

    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                running = False

# Quit Pygame
pygame.quit()
sys.exit()


