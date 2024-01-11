import mne
import numpy as np
import pyxdf
import bisect
import matplotlib.pyplot as plt

data_file = "VInay prabhu sample_old1.xdf"
streams, _ = pyxdf.load_xdf(data_file)

print(type(streams))
print()
print(len(streams))
print()

# for i in streams:
#     print(i.keys())
# print()
# for i in streams:
#     print(i['info']['name'][0])
#     print()

eeg_stream = streams[0]
first_timestamp = float(eeg_stream['footer']['info']['first_timestamp'][0])
print(eeg_stream.keys())
print()
print(eeg_stream['info'].keys())
print()

# for i in range(16):
#     print('Pos', i+1, '=', (eeg_stream['info']['desc'][0]['channels'][0]['channel'][i]['label'][0]))

time_offset = eeg_stream['footer']['info']['clock_offsets'][0]['offset'][0]['time']
eeg_time_stamps = np.array(eeg_stream['time_stamps']) # Length of this array is 20250
eeg_time_stamps_start_from_zero = eeg_time_stamps - first_timestamp 

Cz_series = eeg_stream['time_series'][:,8] # Length of this array is 20250
Pz_series = eeg_stream['time_series'][:,12] # Length of this array is 20250



# print(eeg_stream['footer']['info'].keys())
# print()
# print(first_timestamp)
# print(time_offset)

# for i in range(len(eeg_stream['footer']['info']['clock_offsets'][0]['offset'])):
#     print(eeg_stream['footer']['info']['clock_offsets'][0]['offset'][i]['time'])

print(np.diff(eeg_time_stamps))
print(np.mean(np.diff(eeg_time_stamps)))
print(np.std(np.diff(eeg_time_stamps)))
print(np.min(np.diff(eeg_time_stamps)))
print(np.max(np.diff(eeg_time_stamps)))

plt.subplot(1,2,1) 
plt.plot(eeg_time_stamps, Cz_series)
plt.xlabel('Time (s)')
plt.ylabel('Cz Amplitude')
plt.title('Cz vs Time')
plt.subplot(1,2,2)
plt.plot(eeg_time_stamps, Pz_series)
plt.xlabel('Time (s)')  
plt.ylabel('Pz Amplitude')
plt.title('Pz vs Time')
plt.show()
