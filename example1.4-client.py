'''
For this example, run two processes of the server and make both of them listen
on different ports.

Usage:

    python example1-server.py 1234
    python example1-server.py 5678
'''

import errno
import select
import socket
import time


def other_task():
    i = 0
    while i < 5:
        i += 1
        print(i)
        time.sleep(0.02)
        yield


def send_data_task(port, data):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', port))
    sock.setblocking(0)
    data = (data + 'helloworld')
    #encode('utf-8'))
    data1=data.encode('utf-8')
    print("Bytes to send: ", len(data1))
    total_sent = 0
    while len(data1):
        try:
            sent = sock.send(data1)
            total_sent += sent
            data = data1[sent:]
            print("Sending data")
        except socket.error as e:
            if e.errno != errno.EAGAIN:
                raise e
            yield ('w', sock)

    print("Bytes sent:", total_sent)


if __name__ == '__main__':
    tasks = [
        other_task(),
        #send_data_task(port=1234, data='india'),
        send_data_task(port=5678, data='bar'),
    ]

    fds = dict(w={}, r={})
    while len(tasks) or len(fds['w']) or len(fds['r']):
        new_tasks = []
        for task in tasks:
            try:
                resp = next(task)
                try:
                    iter(resp)
                    fds[resp[0]][resp[1]] = task
                except TypeError:
                    # this task has to be done since not dependent on any fd
                    new_tasks.append(task)
            except StopIteration:
                # function completed
                pass

        if len(fds['w'].keys()) or len(fds['r'].keys()):
            readable, writeable, exceptional = select.select(
                fds['r'].keys(), fds['w'].keys(), [], 0)
            for readable_sock in readable:
                new_tasks.append(fds['r'][fd])
                del fds['r'][fd]
            for fd in writeable:
                new_tasks.append(fds['w'][fd])
                del fds['w'][fd]
            # ignore exceptional for now

        tasks = new_tasks
