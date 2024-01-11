import mne
import numpy as np
import pyxdf
import bisect
import matplotlib.pyplot as plt

data_file = "DPI.xdf"
streams, _ = pyxdf.load_xdf(data_file)

eeg_stream = streams[3]
sfreq = float(eeg_stream['info']['nominal_srate'][0])

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

marker_stream = streams[1]
print()
print(marker_stream['info'].keys())
print()
print((marker_stream['time_series']))
print()
print('EEG time stamps:')
print(eeg_stream['time_stamps'])
print()
print('Marker time stamps:')
print((marker_stream['time_stamps']))
