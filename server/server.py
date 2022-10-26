from socket import socket


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


def run_command(command: str, message: str) -> str:
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
    return message


def run_commands(message: str) -> str:
    words = message.split()
    if len(words) < 3 or words[0] != 'COMMAND':
        return message
    message = ' '.join(words[2:])
    for command in words[1]:
        message = run_command(command, message)
    return message


class Server:

    def __init__(self, sock: socket,
                 host: str = 'localhost',
                 port: int = 50000):
        self.socket = sock
        self.address = (host, port)
        self.connections = None
        self._setup()

    def _setup(self):
        self.socket.bind(self.address)
        self.socket.listen(1)

    def accept(self):
        args = self.socket.accept()
        self.connections = [Client(*args)]

    def run(self):
        while True:
            self.accept()
            client = self.connections[0]
            with client.socket:
                while (message := client.receive()):
                    message = run_commands(message)
                    client.send(message)


def main():
    with socket() as s:
        server = Server(s)
        server.run()


if __name__ == '__main__':
    main()
