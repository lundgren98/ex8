from socket import socket
from threading import Thread


class Client:

    def __init__(self, sock: socket, address: tuple[str, int]):
        self.socket = sock
        self.address = address

    def send(self, message: str):
        self.socket.sendall(message.encode())

    def receive(self) -> str | None:
        buf = self.socket.recv(1024)
        if buf:
            return buf.decode()
        return None


class Server:

    def __init__(self, sock: socket,
                 host: str = 'localhost',
                 port: int = 50000):
        self.socket = sock
        self.address = (host, port)
        self.connections = []
        self.broadcast = False
        self._setup()

    def _setup(self):
        self.socket.bind(self.address)
        self.socket.listen(10)

    def accept(self):
        args = self.socket.accept()
        self.connections.append(Client(*args))

    def run(self):
        client = self.connections[-1]
        print(f'{client.address} connected')
        with client.socket:
            while (message := client.receive()):
                message = self.run_commands(message)
                if self.broadcast:
                    self.broadcast = False
                    for c in self.connections:
                        c.send(message)
                else:
                    client.send(message)
        print(f'{client.address} disconnected')
        self.connections.remove(client)

    def run_command(self, command: str, message: str) -> str:
        if command.isdigit():
            return message * int(command)
        if command == 'u':
            return message.upper()
        if command == 'l':
            return message.lower()
        if command == 'r':
            return message[::-1]
        if command == 't':
            return message.title()
        if command == 'c':
            return message.capitalize()
        if command == 's':
            return message.swapcase()
        if command == 'b':
            self.broadcast = True
        return message

    def run_commands(self, message: str) -> str:
        words = message.split()
        if len(words) < 3 or words[0] != 'COMMAND':
            return message
        message = ' '.join(words[2:])
        for command in words[1]:
            message = self.run_command(command, message)
        return message


def main():
    with socket() as s:
        server = Server(s, port=50001)
        while True:
            server.accept()
            if len(server.connections) < 10:
                t = Thread(target=server.run, daemon=True)
                t.start()


if __name__ == '__main__':
    main()
