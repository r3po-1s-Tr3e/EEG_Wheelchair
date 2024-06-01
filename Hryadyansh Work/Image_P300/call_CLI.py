import sys
import subprocess
batch_file_path = "get_from_CLI.bat"
name = sys.argv[1]


subprocess.call([batch_file_path, name], shell=True)