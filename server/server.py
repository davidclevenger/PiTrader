import socket
from _thread import *
import threading
import signal
import os
from datetime import datetime as datetime
import time
import shutil

print_lock = threading.Lock()

port = 12348

class Connection:
    def __init__(self, username, comm, auth, refresh, code):
        self.username = username
        self.comm = comm
        self.token = auth
        self.refresh = refresh
        self.code = code

class Server:
    def __init__(self):
        global port
        self.connections = {}  # connected clients { username -> socket }
        self.pool = []
        self.master_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.master_sock.bind(('',port))

        # setup signal handlers
        signal.signal(signal.SIGTERM, self.close)
        signal.signal(signal.SIGTRAP, signal.SIG_IGN)
        signal.signal(signal.SIGINT, signal.SIG_IGN)

    def close(self):
        self.master_sock.close()

    def listen(self):
        self.master_sock.listen()

        while True:
            client, _ = self.master_sock.accept()
            msg = client.recv(1024)
            msg = msg.decode()
            fields = msg.split(',')
            username = fields[1]
            code = client.recv(4096)
            code = code.decode()
            curr = Connection(username, client, fields[2], fields[3], code)
            self.connections[username] = curr

            # setup directory structure
            os.makedirs('./users/{}'.format(username), exist_ok=True)

            # delete code if already present
            if os.path.exists('./users/{}/strategy.py'):
                os.remove('./users/{}/strategy.py'.format(username))

            # store code in directory
            with open("./users/{}/strategy.py".format(username), "w") as codefile:
                codefile.write(code)

            tmp = threading.Thread(None, self.handle_client, username, (username,))
            tmp.start()

            # return success to signal
            client.send('OK'.encode())

    def handle_client(self, username):
        connection = self.connections[username]
        curr_time = datetime.today()

        # EST assumed
        # rebalance after market close
        while True:
            # rebalance
            if 16 < curr_time.hour < 17 and 35 < curr_time.minute < 45:
                usercode = __import__("users.{}.strategy".format(username))
                usercode.strategy(connection.token)
                time.sleep(720) # 12 minutes, force wait to outside interval
                del usercode

            else:
                time.sleep(300) # 5 minutes, will hit at least once in interval above

def main():
    server = Server()
    server.listen()


"""
def threaded(c):
    data = None
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
"""

if __name__ == '__main__':
    main()
