import socket
import pickle


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "127.0.0.1"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def getP(self):
        return self.p

    def connect(self) -> bool:
        try:
            self.client.connect(self.addr)
            return True
        except:  # noqa: E722
            return False

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            raise e

    def close(self) -> None:
        try:
            self.client.send(pickle.dumps("exit"))
        except:  # noqa: E722
            pass
