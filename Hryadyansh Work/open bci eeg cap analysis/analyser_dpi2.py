import mne
import numpy as np
import pyxdf
import bisect
import matplotlib.pyplot as plt

data_file = "DPI2.xdf"
streams, _ = pyxdf.load_xdf(data_file)
low_cutoff = 0.1
high_cutoff = 15 
EPOCHS_TIMING = (0, 1.2)

for i  in range(len(streams)):
    print(streams[i]['info']['name'][0])

print()

eeg_stream = streams[2]
sfreq = float(eeg_stream['info']['nominal_srate'][0])
ch_names = []
for i in range(len(eeg_stream['info']['desc'][0]['channels'][0]['channel'])):
    ch_names.append(eeg_stream['info']['desc'][0]['channels'][0]['channel'][i]['label'][0])
info = mne.create_info(ch_names=ch_names, sfreq=sfreq, ch_types='eeg')
data = np.array(eeg_stream['time_series']).T
raw = mne.io.RawArray(data, info)
raw.filter(low_cutoff, high_cutoff, fir_design='firwin')

first_timestamp = float(eeg_stream['footer']['info']['first_timestamp'][0])
eeg_time_stamps = np.array(eeg_stream['time_stamps']) 
eeg_time_stamps_start_from_zero = eeg_time_stamps - first_timestamp 

Cz_series = eeg_stream['time_series'][:,8] 
Pz_series = eeg_stream['time_series'][:,12] 

# plt.subplot(1,2,1) 
# plt.plot(eeg_time_stamps_start_from_zero, Cz_series)
# plt.xlabel('Time (s)')
# plt.ylabel('Cz Amplitude')
# plt.title('Cz vs Time')
# plt.subplot(1,2,2)
# plt.plot(eeg_time_stamps_start_from_zero, Pz_series)
# plt.xlabel('Time (s)')  
# plt.ylabel('Pz Amplitude')
# plt.title('Pz vs Time')
# plt.show()

marker_stream = streams[3]
# print()
# print(marker_stream['info'].keys())
# print()
# print((marker_stream['time_series']))
# print()
# print('EEG time stamps:')
# print(eeg_stream['time_stamps'])
# print()
# print('Marker time stamps:')
# print((marker_stream['time_stamps']))

marker_time_samples = marker_stream['time_stamps']
marker_time_series = [i[0] for i in marker_stream['time_series']]
# print(marker_time_series)
masked_marker_time_series = []
for i in marker_time_series:
    if i == 'X':
        masked_marker_time_series.append(0)
    elif i == 'I':
        masked_marker_time_series.append(2)
    elif i == 'T':
        masked_marker_time_series.append(1)
# print()
# print(masked_marker_time_series)

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
    
nearest_indices = [find_nearest_index(list(np.array(eeg_stream['time_stamps']).T), element) for element in marker_time_samples]

if len(nearest_indices) == len(masked_marker_time_series):
    events = np.column_stack((nearest_indices, np.zeros_like(nearest_indices), masked_marker_time_series)).astype(int)
else:
    diff = len(nearest_indices) - len(masked_marker_time_series)
    events = np.column_stack((nearest_indices[:-diff], np.zeros_like(nearest_indices[:-diff]), masked_marker_time_series)).astype(int)
# print(events)
# print(events.shape)

events_filtered = events.copy()
events_filtered = events_filtered[events_filtered[:, 2] != 0]

print(events_filtered)
print(events_filtered.shape)

print(eeg_time_stamps)

epochs = mne.Epochs(raw, events_filtered, tmin=EPOCHS_TIMING[0], tmax=EPOCHS_TIMING[1], baseline=(0, 0), preload=True)
print(epochs)
evoked = epochs.average()

T_epoch = epochs['1']
I_epoch = epochs['2']

avg_T = T_epoch.average()
avg_I = I_epoch.average()


plt.plot(avg_T.times, avg_T.data[0])
plt.plot(avg_I.times, avg_I.data[0])
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.title('T and I ERP')
plt.legend(['I', 'T'])
plt.show()