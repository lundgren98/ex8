from socket import socket

class Client:

    def __init__(self, sock: socket,
                 host: str = 'localhost',
                 port: int = 50000):
        self.address = (host, port)
        self.socket = sock

    def connect(self):
        self.socket.connect(self.address)

    def send(self, message: str):
        self.socket.sendall(message.encode())

    def receive(self, bufsize: int = 1024):
        return self.socket.recv(bufsize).decode()

    def run(self):
        self.connect()
        while True:
            self.send(input('> '))
            print(self.receive())


def main():
    with socket() as s:
        client = Client(s)
        client.run()


if __name__ == '__main__':
    main()
