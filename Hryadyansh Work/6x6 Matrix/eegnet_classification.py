#!/usr/bin/env python
# coding: utf-8

import mne
import numpy as np
import pandas as pd
from ALL_model import EEGNet_ELU
from torch.autograd import Variable
from dataloader import read_bci_data
import pandas as pd
import torch
import statistics
import os

# file_name = "abhishek_mantri_H_2.xdf_epochs-epo.fif"
file_name = "ayush_sawarn_F_1.xdf_epochs-epo.fif"

file_loc = "Epoch Files\\"+file_name
epochs = mne.read_epochs(file_loc)
print("file_name: ", file_name)
epoch_dict = {}
for i in range(1, 13):
    curr_key = str(i)
    non_key = "non_" + curr_key
    epoch_dict[curr_key] = epochs[curr_key]
    epoch_dict[non_key] = epochs[epochs.events[:, 2] != i]

model = EEGNet_ELU(2)
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print("Device: ", device)
filepath= "trained_models\\EEGNet_abhishek_mantri_checkpoint_ELU.rar"
model.load_state_dict(torch.load(filepath, map_location=device))

def predict_single_sample(data_row, model, device):
    model.eval()  # Set the model to evaluation mode
    with torch.no_grad():
        data_row = data_row.astype("float32")  # Convert data to float32
        data_row = torch.from_numpy(data_row)  # Convert to PyTorch tensor
        data_row = data_row.to(device)  # Move data to the specified device (CPU or GPU)
        model = model.to(device)
        # Forward pass to get predictions
        output = model(data_row)
        predicted_label = torch.argmax(output, dim=1).item()  # Get the predicted label
        
        return predicted_label

epoch_output = {}

for i in range(1,13):
    epoch_output[str(i)] = []
    for j in range(epoch_dict[str(i)].get_data().shape[0]):
        current_dat = epoch_dict[str(i)].get_data()[j:j+1,3:6]
        current_data = np.expand_dims(current_dat, axis=1)
        # print("Predicted label: ", predict_single_sample(current_data, model, device))
        epoch_output[str(i)].append(predict_single_sample(current_data, model, device))
    mode_epoch = statistics.mode(epoch_output[str(i)])
    score_epoch = np.sum(epoch_output[str(i)])
    epoch_output[str(i)] = score_epoch

print((epoch_output))