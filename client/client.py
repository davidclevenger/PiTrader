from tkinter import *
import tkinter.filedialog as filedialog
import matplotlib
import sys
import os
import socket
import requests

class Server:
    def __init__(self):
        self.host = "com1575.eecs.utk.edu"
        self.port = 12345
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))

    def send(self, data):
        self.sock.send(data.encode('ascii'))

    def recv(self, amount=1024):
        return self.sock.recv(amount)
        

class Client(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)

        # Server
        self.server = Server()

        # GUI
        self.master = master
        self.un = StringVar()
        self.un.set("")
        self.pw = StringVar()
        self.pw.set("")
        self.selected_file = StringVar()
        self.selected_file.set("-")
        self.error_text = StringVar()
        self.error_text.set("No issues.")
        self.token = None
        self.refresh_token = None
        self.account_url = None

        self.setup()

    def setup(self):
        self.master.title = "PiTrader"
        self.pack(fill=BOTH, expand=1)

        user_label = Label(self, text="Robinhood username")
        user_label.place(x=20, y=80)
        username = Entry(self, text=self.un)
        username.place(x=20, y=100)

        pass_label = Label(self, text="Robinhood password ( never saved )")
        pass_label.place(x=20, y=280)
        password = Entry(self, text=self.pw, show="*")
        password.place(x=20, y=300)

        choose = Button(self, text="Pick Strategy", command=self.select_file)
        choose.place(x=100, y=0)
        selected = Label(self, textvariable=self.selected_file)
        selected.place(x=100, y= 25)

        upload = Button(self, text="Upload", command=self.upload)
        upload.place(x = 100, y = 40)

        quit = Button(self, text="Quit", command=exit)
        quit.place(x=0, y=0)

        err = Label(self, textvariable=self.error_text)
        err.place(x=300, y=0)

    def select_file(self):
        chosen = filedialog.askopenfilename()
        if not chosen.endswith(".py"):
            self.update_error_text("Strategy must be a Python file!")
            return
        else:
            self.update_error_text("No issues.")

        self.selected_file.set(chosen)


    def update_error_text(self, msg):
        self.error_text.set(msg)

    def upload(self):
        if self.selected_file.get() == '-':
            self.update_error_text("You have not selected a file!")
            return

        # get file data
        code = ""
        with open(self.selected_file.get()) as file:
            code = file.read()
            file.close()

        if code == "":
            self.update_error_text("Could not read file!")
            return

        """
        # login 
        payload = {
            'client_id': 'c82SH0WZOsabOXGP2sxqcj34FxkvfnWRZBKlBjFS',
            'expires_in': 3600,
            'grant_type': 'password',
            'password': self.pw.get(),
            'scope': 'internal',
            'username': self.un.get(),
        }

        r = requests.post('https://api.robinhood.com/oauth2/token/', data=payload)
        if r.status_code != 200:
            raise ConnectionError('Unable to establish connection with Robinhood API.')

        ret = r.json()
        self.token = ret['access_token']
        self.refresh_token = ret["refresh_token"]
        
        # get account url
        headers = {
            'Accept': 'application/json',
            'Authorization': 'Bearer {}'.format(self.token)
        }

        r = requests.get('https://api.robinhood.com/portfolios/', headers=headers)
        if r.status_code != 200:
            raise ConnectionError('Unable to establish connection with Robinhood API.')

        ret = r.json()
        acc_url = ret['results'][0]['account']
        self.account_url = acc_url
        """

        # send to server
        # to_server = 'login,' + self.un.get() + ',' + self.account_url + ',' + self.token + ',' + self.refresh_token
        to_server = 'login,USER,TOKEN,REFRESH_TOKEN'
        self.server.send(to_server)
        self.server.send(code)

        status = self.server.recv()
        if status != 'OK':
            raise IOError("Bad response from server")

def main():
    root = Tk()
    root.geometry("640x480")
    client = Client(root)
    client.mainloop()

    return 0

if __name__ == "__main__":
    sys.exit(main())
