import socket

server = (socket.gethostbyname(socket.gethostname()), 8000)


def client():
    with socket.socket() as soc:
        soc.bind(("", 0))
        soc.connect(server)
        soc.sendto(b"Hello", server)
        data = soc.recv(1024)
        print(data.decode())


if __name__ == '__main__':
    client()