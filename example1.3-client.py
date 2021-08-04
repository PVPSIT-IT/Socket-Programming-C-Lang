import errno
import select
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost',5678))
sock.setblocking(0)

data = 'foobar\n'
data_size = len(data)
data1=data.encode('utf-8')
print('Bytes to send: ', len(data1))

total_sent = 0
while len(data1):
    try:
        sent = sock.send(data1)
        total_sent += sent
        data = data1[sent:]
        print('Sending data')
    except socket.error as e:
        if e.errno != errno.EAGAIN:
            raise e
        print('Blocking with', len(data), 'remaining')
        select.select([], [sock], [])  # This blocks until

assert total_sent == data_size  # True
