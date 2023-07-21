import socket
import threading
import time

HEADER = 64
PORT = 5051
#SERVER = socket.gethostbyname(socket.gethostname())
SERVER = '192.168.0.16'
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MSG = '!DISCONNECT'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} CONNECTED")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)

        if not msg_length:
            continue

        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode(FORMAT)
        print(f"[{addr}] {msg}")

        handle_commands(msg)

        if(msg == DISCONNECT_MSG):
            connected = False

    conn.close()

def handle_commands(msg):

    if msg == '!up':
        pass
    if msg == '!down':
        pass
    if msg == '!left':
        pass
    if msg == '!right':
        pass

def start():
    server.listen()
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

print('server is starting...')
print(f'[LISTENING] SERVER IS LISTENING ON {SERVER}')
start()