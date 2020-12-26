import socket
import pickle

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = input("ip")
        self.port = int(input("port"))
        self.addr = (self.server, self.port)
        self.connect()

    def connect(self):
        self.client.connect(self.addr)
        print(self.recv())
        print("======")

    def recv(self):
        header_size = self.client.recv(8)
        while len(header_size) < 8:
            header_size += self.client.recv(8-len(header_size))
        header_size = int.from_bytes(header_size, "little")
        header = self.client.recv(header_size)
        while len(header) < header_size:
            header += self.client.recv(header_size-len(header))
        header = pickle.loads(header)
        data = self.client.recv(header["message_length"])
        while len(data) < header["message_length"]:
            data += self.client.recv(header["message_length"]-len(data))
        if header["type"] == "obj":
            data = pickle.loads(data)
        elif header["type"] == "str":
            data = data.decode("utf-8")
        return data, header["request"]



    def send(self, type, data):
        if type == "obj":
            array = pickle.dumps(data)
        elif type == "str":
            array = str.encode(data)
        else:
            return
        header = {"type": type, "message_length": len(array)}
        header_array = pickle.dumps(header)
        header_length = len(header_array)
        header_length = int.to_bytes(header_length, 8, "little")
        self.client.sendall(header_length)
        self.client.sendall(header_array)
        self.client.sendall(array)


