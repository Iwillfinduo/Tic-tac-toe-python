import json
import socket
import threading


class HostingClient:
    def __init__(self, host, port, name='host'):
        self.host = host
        self.port = port
        self.name = name
        self.is_connected = False
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(1)
        print("Now you are a host")
        self.connection, self.address = None, None
        threading.Thread(target=self.run, daemon=True).start()

    def run(self):
        self.connection, self.address = self.server_socket.accept()
        print("new connection from {address}".format(address=self.address))
        self.is_connected = True
        self._receive_data()

    def _receive_data(self):
        self.turn = None
        self.row = None
        self.col = None
        self.name = None
        while True:
            data = self.connection.recv(1024).decode('utf-8')
            data = json.loads(data)
            if data.get('turn') is not None:
                self.turn = data['turn']
            if data.get('row') is not None:
                self.row = data['row']
                self.col = data['col']
            if data.get('name') is not None:
                self.name = data['name']
            print(data)

class Connection:
    def __init__(self, ip, name):
        self.host = ip.split(':')[0]
        self.port = int(ip.split(':')[1])
        address_to_server = (self.host, self.port)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.connect(address_to_server)
        threading.Thread(target=self.run, daemon=True).start()

    def run(self):
        self._receive_data()

    def _receive_data(self):
        self.turn = None
        self.row = None
        self.col = None
        self.name = None
        while True:
            data = self.server_socket.recv(1024).decode('utf-8')
            data = json.loads(data)
            if data.get('turn') is not None:
                self.turn = data['turn']
            if data.get('row') is not None:
                self.row = data['row']
                self.col = data['col']
            if data.get('name') is not None:
                self.name = data['name']
            print(data)
