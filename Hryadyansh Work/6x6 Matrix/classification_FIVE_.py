#!/usr/bin/env python
# coding: utf-8

import mne
import numpy as np
import sys
import socket
import os
import pandas as pd

channel_no = -3      # Channel Names: ['Fp1', 'Fp2', 'Fz', 'C3', 'C4', 'Pz', 'O1', 'O2']
EPOCHS_TIMING = (-0.2, 0.8)
ar_start_time = 0.2
ar_end_time = 0.5
epoch_dict = {}
diff_dict = {}
epoch_avg_dict = {}
grid = [
    ['A', 'B', 'C', 'D', 'E', 'F'],
    ['G', 'H', 'I', 'J', 'K', 'L'],
    ['M', 'N', 'O', 'P', 'Q', 'R'],
    ['S', 'T', 'U', 'V', 'W', 'X'],
    ['Y', 'Z', '1', '2', '3', '4'],
    ['5', '6', '7', '8', '9', '0']
    ]

def area_classification(diff_dict):
    row_keys = range(1,7)
    col_keys = range(7,13)
    val_row = []
    for i in row_keys:
        val_row.append(diff_dict[str(i)])
    val_col = []
    for i in col_keys:
        val_col.append(diff_dict[str(i)])
    max_row = val_row.index(max(val_row))
    max_col = val_col.index(max(val_col))
    return grid[max_row][max_col]

def peak_picking(epoch_avg_dict):
    peak_dict = {}
    for i in range(1, 13):
        curr_key = str(i)
        peak_dict[curr_key] = np.max(epoch_avg_dict[curr_key].data[channel_no][list(epoch_avg_dict[curr_key].times).index(ar_start_time):list(epoch_avg_dict[curr_key].times).index(ar_end_time)]) - np.min(epoch_avg_dict[curr_key].data[channel_no][list(epoch_avg_dict[curr_key].times).index(EPOCHS_TIMING[0]):list(epoch_avg_dict[curr_key].times).index(ar_start_time)])
    row_keys = range(1,7)
    col_keys = range(7,13)
    val_row = []
    for i in row_keys:
        val_row.append(peak_dict[str(i)])
    val_col = []
    for i in col_keys:
        val_col.append(peak_dict[str(i)])
    max_row = val_row.index(max(val_row))
    max_col = val_col.index(max(val_col))   
    return grid[max_row][max_col]
    # return peak_dict

def get_epoch_files():
    folder_path = "Epoch Files"
    file_list = os.listdir(folder_path)
    return file_list

def classification_out(file_name):
    file_loc = "Epoch Files\\"+file_name
    epochs = mne.read_epochs(file_loc)
    print("file_name: ", file_name)
    for i in range(1, 13):
        curr_key = str(i)
        non_key = "non_" + curr_key
        epoch_dict[curr_key] = epochs[curr_key]
        epoch_dict[non_key] = epochs[epochs.events[:, 2] != i]

    for key in epoch_dict:
        epoch_avg_dict[key] = epoch_dict[key].average()

    for i in range(1, 13):
        curr_key = str(i)
        non_key = "non_" + curr_key
        diff_dict[curr_key] = np.mean(epoch_avg_dict[curr_key].data[channel_no][list(epoch_avg_dict[curr_key].times).index(ar_start_time):list(epoch_avg_dict[curr_key].times).index(ar_end_time)]) - np.mean(epoch_avg_dict[non_key].data[channel_no][list(epoch_avg_dict[non_key].times).index(ar_start_time):list(epoch_avg_dict[non_key].times).index(ar_end_time)])

    return [area_classification(diff_dict), peak_picking(epoch_avg_dict)]

file_list = get_epoch_files()

classification_list = []

for file_name in file_list:
    file_nm = file_name.split("_")
    for i in file_nm:
        check_char = i[0]
        if check_char.isdigit():
            index_nu = file_nm.index(i)
    true_lab = file_nm[index_nu-1]
    classification_list.append([file_name,true_lab,classification_out(file_name)[0], classification_out(file_name)[1]])  # structure of list: file_name, true_label, area_classification_output, peak_classification_output

columns = ["file_name", "true_label", "area_label", "peak_label"]

# Create DataFrame
df = pd.DataFrame(classification_list, columns=columns)

file_path = "classification_data.xlsx"

df.to_excel(file_path, index=False)

print("DataFrame saved to Excel file successfully.")