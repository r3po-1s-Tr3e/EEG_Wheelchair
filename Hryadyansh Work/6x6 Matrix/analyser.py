import mne
import numpy as np
import pyxdf
import bisect
import matplotlib.pyplot as plt

low_cutoff = 0.1
high_cutoff = 15 
EPOCHS_TIMING = (-0.2, 0.8)
channel_no = -3     # Channel Names: ['Fp1', 'Fp2', 'Fz', 'C3', 'C4', 'Pz', 'O1', 'O2']
file_name = 'Daksh_B_1'
data_file = "LabRecorder\\" + file_name + ".xdf"
streams, _ = pyxdf.load_xdf(data_file)

# for i in streams:
#     print(i['info']['name'][0])           # Marker stream is streams[0], EEG stream is streams[1]
#     print()

eeg_stream = streams[1]
ch_names = []
for i in range(len(eeg_stream['info']['desc'][0]['channels'][0]['channel'])):
    ch_names.append(eeg_stream['info']['desc'][0]['channels'][0]['channel'][i]['label'][0])

sfreq = float(eeg_stream['info']['nominal_srate'][0])
info = mne.create_info(ch_names=ch_names, sfreq=sfreq, ch_types='eeg')
data = np.array(eeg_stream['time_series']).T
raw = mne.io.RawArray(data, info)
raw.filter(low_cutoff, high_cutoff, fir_design='firwin')

# Read events and create epochs
marker_stream = streams[0]
event_codes = [int(event[0]) if event[0] else 0 for event in marker_stream['time_series']] # Using zero as a placeholder
event_timestamps = marker_stream['time_stamps']
event_samples = (event_timestamps) 
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
# Create epochs
epochs = mne.Epochs(raw, events, tmin=EPOCHS_TIMING[0], tmax=EPOCHS_TIMING[1], preload=True)
print(epochs)
# Average epochs to create ERP
#evoked = epochs.average()

print()
print("events: ", events)
# print("event shape: ", events.shape)
# print()
# print(raw.times*sfreq)
# print(raw.times.shape)
# print(event_timestamps)
# print(np.array(eeg_stream['time_stamps']).T)
# print()
# print("Difference between successive values of EEG array is: ", np.diff(np.array(eeg_stream['time_stamps']).T) )
# print("Difference between successive values of MARKER array is: ", np.diff(event_timestamps) )
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
# print("Nearest indices in list A for elements in list B:")
# print(nearest_indices)

if len(nearest_indices) == len(filtered_event_codes):
    events = np.column_stack((nearest_indices, np.zeros_like(nearest_indices), filtered_event_codes)).astype(int)
else:
    diff = len(nearest_indices) - len(filtered_event_codes)
    events = np.column_stack((nearest_indices[:-diff], np.zeros_like(nearest_indices[:-diff]), filtered_event_codes)).astype(int)
# print(events)

# events = np.column_stack((nearest_indices[:-1], np.zeros_like(nearest_indices[:-1]), filtered_event_codes)).astype(int)
# Create epochs
epochs = mne.Epochs(raw, events, tmin=EPOCHS_TIMING[0], tmax=EPOCHS_TIMING[1], preload=True, event_repeated='merge')
# epochs = mne.Epochs(raw, events, tmin=EPOCHS_TIMING[0], tmax=EPOCHS_TIMING[1], preload=True, event_repeated='merge')
print(epochs)
epochs_filename = "Epoch Files\\" + file_name + "_epochs-epo.fif"
# epochs.save(epochs_filename)


epoch_dict = {}
for i in range(1, 13):
    curr_key = str(i)
    non_key = "non_" + curr_key
    epoch_dict[curr_key] = epochs[curr_key]
    epoch_dict[non_key] = epochs[epochs.events[:, 2] != i]

epoch_avg_dict = {}
for key in epoch_dict:
    epoch_avg_dict[key] = epoch_dict[key].average()

print("sfreq: ", sfreq)

print("Epoch val:", np.vstack((epoch_dict['1'].get_data()[:,3:6], epoch_dict['2'].get_data()[:,3:6])).shape)
# print("Epoch val:", np.vstack((epoch_dict['1'].get_data()[:,3:7], epoch_dict['2'].get_data()[:,3:7])))

print(epoch_dict['1'].get_data().shape[0])

# Plotting of normal average
plt.figure(figsize=(15, 15))

# Plot for 1 vs Non-1
plt.subplot(3, 2, 1)
plt.plot(epoch_avg_dict['1'].times, epoch_avg_dict['1'].data[channel_no].T, color='blue', label='A')
plt.plot(epoch_avg_dict['non_1'].times, epoch_avg_dict['non_1'].data[channel_no].T, color='orange', label='Non-A')
plt.title('1 vs Non-1')
plt.legend()

# Plot for 2 vs Non-2
plt.subplot(3, 2, 2)
plt.plot(epoch_avg_dict['2'].times, epoch_avg_dict['2'].data[channel_no].T, color='blue', label='B')
plt.plot(epoch_avg_dict['non_2'].times, epoch_avg_dict['non_2'].data[channel_no].T, color='orange', label='Non-B')
plt.title('2 vs Non-2')
plt.legend()

# Plot for 3 vs Non-3
plt.subplot(3, 2, 3)
plt.plot(epoch_avg_dict['3'].times, epoch_avg_dict['3'].data[channel_no].T, color='blue', label='C')
plt.plot(epoch_avg_dict['non_3'].times, epoch_avg_dict['non_3'].data[channel_no].T, color='orange', label='Non-C')
plt.title('3 vs Non-3')
plt.legend()

# Plot for 4 vs Non-4
plt.subplot(3, 2, 4)
plt.plot(epoch_avg_dict['4'].times, epoch_avg_dict['4'].data[channel_no].T, color='blue', label='D')
plt.plot(epoch_avg_dict['non_4'].times, epoch_avg_dict['non_4'].data[channel_no].T, color='orange', label='Non-D')
plt.title('4 vs Non-4')
plt.legend()

# Plot for 5 vs Non-5
plt.subplot(3, 2, 5)
plt.plot(epoch_avg_dict['5'].times, epoch_avg_dict['5'].data[channel_no].T, color='blue', label='E')
plt.plot(epoch_avg_dict['non_5'].times, epoch_avg_dict['non_5'].data[channel_no].T, color='orange', label='Non-E')
plt.title('5 vs Non-5')
plt.legend()

# Plot for 6 vs Non-6
plt.subplot(3, 2, 6)
plt.plot(epoch_avg_dict['6'].times, epoch_avg_dict['6'].data[channel_no].T, color='blue', label='E')
plt.plot(epoch_avg_dict['non_6'].times, epoch_avg_dict['non_6'].data[channel_no].T, color='orange', label='Non-E')
plt.title('6 vs Non-6')
plt.legend()

# Adjust layout and display the plot
plt.tight_layout()
plt.show()


# Plotting of normal average
plt.figure(figsize=(15, 15))

# Plot for 7 vs Non-7
plt.subplot(3, 2, 1)
plt.plot(epoch_avg_dict['7'].times, epoch_avg_dict['7'].data[channel_no].T, color='blue', label='F')
plt.plot(epoch_avg_dict['non_7'].times, epoch_avg_dict['non_7'].data[channel_no].T, color='orange', label='Non-F')
plt.title('7 vs Non-7')
plt.legend()

# Plot for 8 vs Non-8
plt.subplot(3, 2, 2)
plt.plot(epoch_avg_dict['8'].times, epoch_avg_dict['8'].data[channel_no].T, color='blue', label='G')
plt.plot(epoch_avg_dict['non_8'].times, epoch_avg_dict['non_8'].data[channel_no].T, color='orange', label='Non-G')
plt.title('8 vs Non-8')
plt.legend()

# Plot for 9 vs Non-9
plt.subplot(3, 2, 3)
plt.plot(epoch_avg_dict['9'].times, epoch_avg_dict['9'].data[channel_no].T, color='blue', label='H')
plt.plot(epoch_avg_dict['non_9'].times, epoch_avg_dict['non_9'].data[channel_no].T, color='orange', label='Non-H')
plt.title('9 vs Non-9')
plt.legend()

# Plot for 10 vs Non-10
plt.subplot(3, 2, 4)
plt.plot(epoch_avg_dict['10'].times, epoch_avg_dict['10'].data[channel_no].T, color='blue', label='I')
plt.plot(epoch_avg_dict['non_10'].times, epoch_avg_dict['non_10'].data[channel_no].T, color='orange', label='Non-I')
plt.title('10 vs Non-10')
plt.legend()

# Plot for 11 vs Non-11
plt.subplot(3, 2, 5)
plt.plot(epoch_avg_dict['11'].times, epoch_avg_dict['11'].data[channel_no].T, color='blue', label='J')
plt.plot(epoch_avg_dict['non_11'].times, epoch_avg_dict['non_11'].data[channel_no].T, color='orange', label='Non-J')
plt.title('11 vs Non-11')
plt.legend()

# Plot for 12 vs Non-12
plt.subplot(3, 2, 6)
plt.plot(epoch_avg_dict['12'].times, epoch_avg_dict['12'].data[channel_no].T, color='blue', label='K')
plt.plot(epoch_avg_dict['non_12'].times, epoch_avg_dict['non_12'].data[channel_no].T, color='orange', label='Non-K')
plt.title('12 vs Non-12')
plt.legend()

# Adjust layout and display the plot
plt.tight_layout()
plt.show()