import socket

host = socket.gethostbyname(socket.gethostname())
port = 8000
print(host)
def server():

    with socket.socket() as sock:
        sock.bind((host, port))
        sock.listen(10)
        print("Started Server")
        conn, addr = sock.accept()
        print(f'Connection {addr}')
        while True:
            with conn:
                try:
                    request = conn.recv(1024)
                    print(request.decode())
                    conn.sendall(b"Ok is connect!")
                except:
                    print("Stopped Server")
                    break


if __name__ == '__main__':
    server()