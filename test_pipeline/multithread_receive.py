import random
import time
from pylsl import StreamInlet, resolve_streams,resolve_stream
from scipy.io import savemat,loadmat
import numpy as np
import pdb
import keyboard
import threading
timeout = 62

print('HIHIHIHI')
timeout_start = time.time()

streams = resolve_stream('type', 'eeg')
inlet_e = StreamInlet(streams[0])
print('found eeg stream')
 
# time.sleep(5)
streams = resolve_stream('type', 'markers')
inlet_m = StreamInlet(streams[0])
print('found marker stream')
# prin'tfed('snfsk')


eeg = []
markers = []


def Extract(lst):
    return [item[0] for item in lst]
     
 
def get_eeg():
	
	while time.time() < timeout_start + timeout:

	    sample, timestamp = inlet_e.pull_sample()
	    # print(timestamp, sample)
	    eeg.append([timestamp,sample])
	    # if keyboard.is_pressed('q'):
	    # 	break 

 
def get_markers():

	while time.time() < timeout_start + timeout:

	    sample, timestamp = inlet_m.pull_sample()
	    # print(timestamp, sample)
	    markers.append([timestamp,sample])
	    # if keyboard.is_pressed('m'):
	    # 	break 
 
if __name__ =="__main__":
    # creating thread
    t1 = threading.Thread(target=get_eeg)
    t2 = threading.Thread(target=get_markers)
 
    # starting thread 1
    t1.start()
    # starting thread 2
    t2.start()
 
    # wait until thread 1 is completely executed
    t1.join()
    # wait until thread 2 is completely executed
    t2.join()
 
    # both threads completely executed
    print("Done!")




# # inlet_e = StreamInlet(streams[1])
print('---------------------')
p = np.array(eeg)
print(p.shape)
# print(eeg)
print('---------------------')
print(markers)

eeg_data = [item[1] for item in eeg]
eeg_data = np.array(eeg_data)
eeg_data = np.c_[ eeg_data, np.zeros(eeg_data.shape[0]) ] 
 
for i in range(len(markers)-1):
    eeg_timestamps = Extract(eeg)
    res = list(filter(lambda j: j > markers[i][0], eeg_timestamps))[0]
    res_m = eeg_timestamps.index(res)
    # print(res_m)
    eeg_data[res_m][-1] = markers[i][1][0]

 

mdic = {"eeg": eeg_data}
savemat("C:/Users/Vinay/OneDrive - IIT Kanpur/Documents/wheelchair/test_pipeline/data/matlab_matrix.mat", mdic)