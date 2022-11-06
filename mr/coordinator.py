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
from itertools import islice

CHUNK_SIZE = 50

map_queue = Queue()
reduce_queue = Queue()

intermediate = []

def add_random_to_queue(queue, amount=100):
    """
    Fill queue with random data
    """
    print(f"Filling queue with {amount} items of random data")
    for _ in range(amount):
        random_string = "".join(random.choice(string.ascii_lowercase) for _ in range(8))
        queue.put(random_string)

def handle_connection(sock, addr):
    """
    Pass one item from map_queue to client
    """
    try:
        while True:
            msg = sock.recv(2048)
            if msg != '' and not map_queue.empty():
                item = map_queue.get()
                data = ("mapf", item)
                num_bytes = sock.send(pickle.dumps(data))
                print(f"--> Delivering {num_bytes} bytes {data} to {addr[0]}:{addr[1]}")
                response = sock.recv(8192)
                words = pickle.loads(response)
                print(f"<-- Received {len(response)} bytes from {addr[0]}:{addr[1]}")
                intermediate.append(words)
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


def add_chunks_to_queue(filename, queue):
    with open(filename) as f:
        while True:
            chunk = "".join(islice(f, CHUNK_SIZE))
            if not chunk:
                break
            queue.put(chunk)


def parse_args():
    input_files = sys.argv[1:]

    for file in input_files:
        add_chunks_to_queue(file, map_queue)

def main():

    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, True)
    sock.bind(('localhost', 20_001))
    sock.listen()
    print("Listening for new connections...")

    Thread(target=listener, args=[sock]).start()    


main()
