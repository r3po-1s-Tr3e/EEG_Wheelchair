import subprocess
import time
import random
batch_file_path = "get_data_batch.bat"

print("One iteration contains one xdf file of each alphabet")
time.sleep(0.5)
print("Enter only subjects first name, dont use any whitespaces")
time.sleep(0.5)

name = input("Enter subjects first name, dont use any whitespaces: ")
n = 20

set_1 = ['H','V','G','Y','F']
set_2 = ['B','G','1','P','Y']
order = []
for i in range(2):
    set_1_r = set_1.copy()
    random.shuffle(set_1_r)
    order.extend(set_1_r)

for i in range(2):
    set_2_r = set_2.copy()
    random.shuffle(set_2_r)
    order.extend(set_2_r)

done_alpha = []

for ite in range(int(n)):
    print("Iteration: ", ite+1)
    for i in range(len(order)):
        alphabet = order[i]
        if alphabet in done_alpha:
            trial_no = "2"
        else:
            trial_no = "1"
        print("Count the occurance of alphabet: ", alphabet)
        time.sleep(2.5)
        subprocess.call([batch_file_path, name, alphabet, trial_no], shell=True)
        print("Alphabet: ", alphabet, " done")
        done_alpha.append(alphabet)
        time.sleep(0.5)
        print("Press Enter to continue")
        input()