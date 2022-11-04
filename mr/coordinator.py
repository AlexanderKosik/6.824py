#!python3

# Reads all the input files passed as command line parameters

# Stores this in a dict[filename, content]

# Provides an TCP Server for RPC from workers
# MIT example uses unix sockets. --> Refer to "How Linux works?"

# Return value of RPC should propably be [filename, content]

from queue import Queue
import string
import random
from socket import *
from threading import Thread
import sys
import pickle


todo_queue = Queue()

# fill with random data
i = 100
print(f"Filling queue with {i} items of random data")
for _ in range(i):
    random_string = "".join(random.choice(string.ascii_lowercase) for _ in range(8))
    todo_queue.put(random_string)

def handle_connection(sock, addr):
    """
    Pass one item from todo_queue to client
    """
    try:
        while True:
            msg = sock.recv(2048)
            if msg != '' and not todo_queue.empty():
                item = todo_queue.get()
                data = ("map", item)
                num_bytes = sock.send(pickle.dumps(data))
                print(f"Delivering {num_bytes} bytes {data} to {addr[0]}:{addr[1]}")
            else:
                print("Done. Queue is empty")
                sys.exit(0)
    except BrokenPipeError:
            print("Connection from client closed...")

def listener(sock):
    while True:
        client, addr = sock.accept()
        print("Got new connection from", addr)
        Thread(target=handle_connection, args=[client, addr]).start()


def main():
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, True)
    sock.bind(('localhost', 20_001))
    sock.listen()
    print("Listening for new connections...")

    Thread(target=listener, args=[sock]).start()    


main()
