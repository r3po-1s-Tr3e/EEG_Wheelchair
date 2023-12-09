import socket
import sys


def send_data(s,msg):


    
# Let's send data through UDP protocol
    # while True:
    s.sendto(msg.encode('utf-8'), ("192.168.1.170", 4444))
    print("\n\n 1. Client Sent : ", msg, "\n\n")
# close the socket
    s.close()