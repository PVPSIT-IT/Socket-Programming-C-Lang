import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 5678))
data = 'client1\n'  # 70 MB of data
data1=data.encode('utf-8')
assert sock.send(data1) == len(data1)  # True
