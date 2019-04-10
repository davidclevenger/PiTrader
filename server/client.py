import socket


def Main():
    host = 'com1575.eecs.utk.edu'
    port = 12345
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((host,port))
    s.setblocking(0)
    while True:
        #print("v")
        message = input('')
        #print("o")
        if message is not '':
            s.send(message.encode('ascii'))
        print("r")
        curReadString = ''
        print("q")
        while curReadString is not None:
            try:
                print("a")
                data = s.recv(1024)
                print("b")
                curReadString = str(data.decode('ascii'))
                print(curReadString)
            except socket.error:
                print("d")
            else:
                print("error")
                break

        #if ans == 'y': 
        #   continue
        #else: 
        if message == 'exit':
            break
    s.close()

if __name__ == '__main__':
    Main()
