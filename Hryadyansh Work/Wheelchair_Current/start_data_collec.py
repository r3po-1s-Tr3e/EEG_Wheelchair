import subprocess
import time
from datetime import datetime

batch_file_path = "get_data_batch.bat"

# name = str(round(time.time()))
name = "rishi_A"
# print("Press enter  to continue")
# input()
subprocess.call([batch_file_path, name], shell=True)
