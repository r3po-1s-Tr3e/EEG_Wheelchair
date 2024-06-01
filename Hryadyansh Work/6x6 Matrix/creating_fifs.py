import mne
import numpy as np
import pyxdf
import bisect

def save_epoch(file_name):
    low_cutoff = 0.1
    high_cutoff = 15 
    EPOCHS_TIMING = (-0.2, 0.8)
    channel_no = -3  # Channel Names: ['Fp1', 'Fp2', 'Fz', 'C3', 'C4', 'Pz', 'O1', 'O2']
    data_file = "LabRecorder\\" + file_name 
    
    streams, _ = pyxdf.load_xdf(data_file)
    
    eeg_stream = streams[1]
    ch_names = []
    for i in range(len(eeg_stream['info']['desc'][0]['channels'][0]['channel'])):
        ch_names.append(eeg_stream['info']['desc'][0]['channels'][0]['channel'][i]['label'][0])
    
    sfreq = float(eeg_stream['info']['nominal_srate'][0])
    info = mne.create_info(ch_names=ch_names, sfreq=sfreq, ch_types='eeg')
    data = np.array(eeg_stream['time_series']).T
    raw = mne.io.RawArray(data, info)
    raw.filter(low_cutoff, high_cutoff, fir_design='firwin')
    
    marker_stream = streams[0]
    event_codes = [int(event[0]) if event[0] else 0 for event in marker_stream['time_series']]
    event_timestamps = marker_stream['time_stamps']
    event_samples = (event_timestamps)
    
    valid_events_mask = [event != 0 for event in event_codes]
    filtered_event_codes = [event for event, mask in zip(event_codes, valid_events_mask) if mask]
    filtered_event_timestamps = [timestamp for timestamp, mask in zip(marker_stream['time_stamps'], valid_events_mask) if mask]
    event_samples = (np.array(filtered_event_timestamps) * sfreq).astype(int)
    
    if len(event_samples) == len(filtered_event_codes):
        events = np.column_stack((event_samples, np.zeros_like(event_samples), filtered_event_codes)).astype(int)
    else:
        diff = len(event_samples) - len(filtered_event_codes)
        events = np.column_stack((event_samples[:-diff], np.zeros_like(event_samples[:-diff]), filtered_event_codes)).astype(int)
    
    nearest_indices = [find_nearest_index(list(np.array(eeg_stream['time_stamps']).T), element) for element in event_timestamps]
    
    if len(nearest_indices) == len(filtered_event_codes):
        events = np.column_stack((nearest_indices, np.zeros_like(nearest_indices), filtered_event_codes)).astype(int)
    else:
        diff = len(nearest_indices) - len(filtered_event_codes)
        events = np.column_stack((nearest_indices[:-diff], np.zeros_like(nearest_indices[:-diff]), filtered_event_codes)).astype(int)
    
    epochs = mne.Epochs(raw, events, tmin=EPOCHS_TIMING[0], tmax=EPOCHS_TIMING[1], preload=True, event_repeated='drop')
    epochs_filename = "Epoch Files\\" + file_name + "_epochs-epo.fif"
    epochs.save(epochs_filename)

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

file_list = [
    "vikky_G_1.xdf",
    "vikky_G_2.xdf",
    "vikky_H_1.xdf",
    "vikky_H_2.xdf",
    "vikky_P_1.xdf",
    "vikky_P_2.xdf",
    "vikky_V_1.xdf",
    "vikky_V_2.xdf",
    "vikky_Y_1.xdf",
    "vikky_Y_2.xdf"
]

for file_name in file_list:
    save_epoch(file_name)
    print(file_name + " done")
