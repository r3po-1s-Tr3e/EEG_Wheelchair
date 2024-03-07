import sys
from PYGAME_SPELLER_FIVE_6x6 import offline

alphabet = sys.argv[1]  # Receive the 'alphabet' variable from the batch file
trial = sys.argv[2]
name = sys.argv[3]
# alphabet = 'B'
# trial = '1'
# name = 'trial'
# Use the 'alphabet' variable in your code as needed

offline(alphabet,trial,name) 
# offline()