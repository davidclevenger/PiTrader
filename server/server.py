import socket
from _thread import *
import threading

print_lock = threading.Lock()

def threaded(c):
    data = None
    #c.setblocking(0)
    while True:
        #print("oy")
        try:
            data = c.recv(1024)
            data = data[::-1]
            c.send(data)
            c.send('cool'.encode())
            print("Sent some data...")
        except socket.error:
            pass
        else:
            print("error")

        #if not data:
        #    print('Bye')
        #    break
    c.close()

def Main():
    host = ""
    port = 12345
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print("socket binded to post", port)
    s.listen(5)
    print("socket is listening")
    while True:
        c, addr = s.accept()
        print('Connected to :', addr[0], ':', addr[1])
        start_new_thread(threaded, (c,))
    s.close()
if __name__ == '__main__':
    Main()
