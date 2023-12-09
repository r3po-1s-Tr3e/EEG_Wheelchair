import socket

ip = "192.168.203.130"
# ip = "127.0.0.1"
port = 4444

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((ip, port))
    s.sendall(b"Hello, world")
    data = s.recv(1024)

print(f"Received {data!r}")