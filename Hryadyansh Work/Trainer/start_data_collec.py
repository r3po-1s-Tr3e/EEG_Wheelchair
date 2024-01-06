import subprocess
import time
batch_file_path = "get_data_batch.bat"

print("Enter only subjects first name, dont use any whitespaces")
time.sleep(0.5)
print("One trial contains one xdf file of each alphabet")
time.sleep(0.5)
print('Example of order of trial: A C B E D')
time.sleep(0.5)
name = input("Enter subjects first name, dont use any whitespaces: ")
n = input("Enter number of trials: ")
order = input("Enter order of alphabet in each trial: ")
order = order.split()

for i in range(int(n)):
    print("Trial: ", i+1)
    for alphabet in order:
        print("Count the occurance of alphabet: ", alphabet)
        subprocess.call([batch_file_path, name, alphabet], shell=True)
        print("Alphabet: ", alphabet, " done")
