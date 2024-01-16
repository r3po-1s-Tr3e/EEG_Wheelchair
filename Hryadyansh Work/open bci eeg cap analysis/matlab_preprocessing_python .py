import mne
import numpy as np
import pyxdf
import bisect
import matplotlib.pyplot as plt

# Adjustable variables
low_cutoff = 0.1
high_cutoff = 15 
EPOCHS_TIMING = (-0.2, 0.8)

# Paths to your files   
data_file = r"C:\Users\hryad\Desktop\iitm\BCI Wheelchair\EEG_Wheelchair - Copy\10-12-Data\rishi_A.xdf"
# EVENTS_FILE = r"C:\Users\hryad\Desktop\iitm\BCI Wheelchair\EEG_Wheelchair - Copy\test_pipeline\events\foo_events.txt"


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
# Create an events array for MNE

if len(event_samples) == len(filtered_event_codes):
    events = np.column_stack((event_samples, np.zeros_like(event_samples), filtered_event_codes)).astype(int)
else:
    diff = len(event_samples) - len(filtered_event_codes)
    events = np.column_stack((event_samples[:-diff], np.zeros_like(event_samples[:-diff]), filtered_event_codes)).astype(int)

# events = np.column_stack((event_samples, np.zeros_like(event_samples), filtered_event_codes)).astype(int)
print()
print("EVENTS:")
print()
print(events)
print()
# Create epochs
epochs = mne.Epochs(raw, events, tmin=EPOCHS_TIMING[0], tmax=EPOCHS_TIMING[1], preload=True)
print(epochs)
# Average epochs to create ERP
#evoked = epochs.average()

print()
print("events: ", events)
print("event shape: ", events.shape)
print()
print(raw.times*sfreq)
print(raw.times.shape)
print(event_timestamps)
print(np.array(eeg_stream['time_stamps']).T)
print()
print("Difference between successive values of EEG array is: ", np.diff(np.array(eeg_stream['time_stamps']).T) )
print("Difference between successive values of MARKER array is: ", np.diff(event_timestamps) )
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

events = np.column_stack((nearest_indices[:-1], np.zeros_like(nearest_indices[:-1]), filtered_event_codes)).astype(int)
print()
print(events)
print()
print(raw.times)
print()
print((eeg_stream['time_stamps']))
print()
# Create epochs
epochs = mne.Epochs(raw, events, tmin=EPOCHS_TIMING[0], tmax=EPOCHS_TIMING[1], preload=True)
print(epochs)
# Average epochs to create ERP
evoked = epochs.average()
# Save the epochs to a FIF file
epochs_filename = r"C:\Users\hryad\Desktop\iitm\BCI Wheelchair\EEG_Wheelchair - Copy\test_pipeline\mat_files\rishi_A-epo.fif"
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



# Bootstrap average

# Function to calculate bootstrap average
def bootstrap_average(epochs, n_bootstrap=1000):
    bootstrap_avgs = []
    for _ in range(n_bootstrap):
        sample_indices = np.random.randint(0, len(epochs), len(epochs))
        sampled_epochs = epochs[sample_indices]
        bootstrap_avgs.append(sampled_epochs.average().data)
    return np.mean(bootstrap_avgs, axis=0)

# Calculate bootstrap averages for each class and their non-class counterparts
# bootstrap_avg_a = bootstrap_average(a_epoch)
# bootstrap_avg_non_a = bootstrap_average(non_a_target)
# bootstrap_avg_b = bootstrap_average(b_epoch)
# bootstrap_avg_non_b = bootstrap_average(non_b_target)
# bootstrap_avg_c = bootstrap_average(c_epoch)
# bootstrap_avg_non_c = bootstrap_average(non_c_target)
# bootstrap_avg_d = bootstrap_average(d_epoch)
# bootstrap_avg_non_d = bootstrap_average(non_d_target)
# bootstrap_avg_e = bootstrap_average(e_epoch)
# bootstrap_avg_non_e = bootstrap_average(non_e_target)





# Calculate averages for each class and their non-class counterparts
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


# Calculate bootstrap averages for each class and their non-class counterparts
# bootstrap_avg_a = bootstrap_average(a_epoch)
# bootstrap_avg_non_a = bootstrap_average(non_a_target)
# bootstrap_avg_b = bootstrap_average(b_epoch)
# bootstrap_avg_non_b = bootstrap_average(non_b_target)
# bootstrap_avg_c = bootstrap_average(c_epoch)
# bootstrap_avg_non_c = bootstrap_average(non_c_target)
# bootstrap_avg_d = bootstrap_average(d_epoch)
# bootstrap_avg_non_d = bootstrap_average(non_d_target)
# bootstrap_avg_e = bootstrap_average(e_epoch)
# bootstrap_avg_non_e = bootstrap_average(non_e_target)


# # Plotting of bootstrap average

# # Plotting of normal average
# plt.figure(figsize=(15, 15))

# # Plot for A vs Non-A
# plt.subplot(3, 2, 1)
# plt.plot(bootstrap_avg_a.times, bootstrap_avg_a.data[-3].T, color='blue', label='A')
# plt.plot(bootstrap_avg_non_a.times, bootstrap_avg_non_a.data[-3].T, color='orange', label='Non-A')
# plt.title('A vs Non-A')
# plt.legend()

# # Plot for B vs Non-B
# plt.subplot(3, 2, 2)
# plt.plot(bootstrap_avg_b.times, bootstrap_avg_b.data[-3].T, color='blue', label='B')
# plt.plot(bootstrap_avg_non_b.times, bootstrap_avg_non_b.data[-3].T, color='orange', label='Non-B')
# plt.title('B vs Non-B')
# plt.legend()

# # Plot for C vs Non-C
# plt.subplot(3, 2, 3)
# plt.plot(bootstrap_avg_c.times, bootstrap_avg_c.data[-3].T, color='blue', label='C')
# plt.plot(bootstrap_avg_non_c.times, bootstrap_avg_non_c.data[-3].T, color='orange', label='Non-C')
# plt.title('C vs Non-C')
# plt.legend()

# # Plot for D vs Non-D
# plt.subplot(3, 2, 4)
# plt.plot(bootstrap_avg_d.times, bootstrap_avg_d.data[-3].T, color='blue', label='D')
# plt.plot(bootstrap_avg_non_d.times, bootstrap_avg_non_d.data[-3].T, color='orange', label='Non-D')
# plt.title('D vs Non-D')
# plt.legend()

# # Plot for E vs Non-E
# plt.subplot(3, 2, 5)
# plt.plot(bootstrap_avg_e.times, bootstrap_avg_e.data[-3].T, color='blue', label='E')
# plt.plot(bootstrap_avg_non_e.times, bootstrap_avg_non_e.data[-3].T, color='orange', label='Non-E')
# plt.title('E vs Non-E')
# plt.legend()

# Adjust layout and display the plot
# plt.tight_layout()
# plt.show()


print(avg_a.data[-3].shape)

# Plotting of normal average
plt.figure(figsize=(15, 15))

# Plot for A vs Non-A
plt.subplot(3, 2, 1)
plt.plot(avg_a.times, avg_a.data[-3].T, color='blue', label='A')
plt.plot(avg_non_a.times, avg_non_a.data[-3].T, color='orange', label='Non-A')
plt.title('A vs Non-A')
plt.legend()

# Plot for B vs Non-B
plt.subplot(3, 2, 2)
plt.plot(avg_b.times, avg_b.data[-3].T, color='blue', label='B')
plt.plot(avg_non_b.times, avg_non_b.data[-3].T, color='orange', label='Non-B')
plt.title('B vs Non-B')
plt.legend()

# Plot for C vs Non-C
plt.subplot(3, 2, 3)
plt.plot(avg_c.times, avg_c.data[-3].T, color='blue', label='C')
plt.plot(avg_non_c.times, avg_non_c.data[-3].T, color='orange', label='Non-C')
plt.title('C vs Non-C')
plt.legend()

# Plot for D vs Non-D
plt.subplot(3, 2, 4)
plt.plot(avg_d.times, avg_d.data[-3].T, color='blue', label='D')
plt.plot(avg_non_d.times, avg_non_d.data[-3].T, color='orange', label='Non-D')
plt.title('D vs Non-D')
plt.legend()

# Plot for E vs Non-E
plt.subplot(3, 2, 5)
plt.plot(avg_e.times, avg_e.data[-3].T, color='blue', label='E')
plt.plot(avg_non_e.times, avg_non_e.data[-3].T, color='orange', label='Non-E')
plt.title('E vs Non-E')
plt.legend()

# Adjust layout and display the plot
plt.tight_layout()
plt.show()
