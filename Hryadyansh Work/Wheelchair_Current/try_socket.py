import socket

# Create a TCP/IP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the server's address and port
server_address = ('172.18.40.1', 12345)  # Use the IP address of the Linux server
client_socket.connect(server_address)

try:
    # Send data
    message = 'Hello, Linux Server!'
    client_socket.sendall(message.encode())

finally:
    # Clean up the connection
    client_socket.close()