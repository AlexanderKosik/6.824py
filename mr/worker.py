#!python3

# Can we load a go.so from python?

# Worker
# Request a filename and content (ignore filename) via RPC from coordinator
# Call map in Worker
# Call reduce in Worker

# Unclear: When do we know when to call reduce on all workers?

from socket import *
from threading import Thread
import time
import random

def request(sock: socket):
    sock.send(b'next')


addr = ('localhost', 20_001)

sock = socket(AF_INET, SOCK_STREAM)
sock.connect(addr)
print(f"Connected to {addr}")

while True:
    try:
        sock.send(b'next')
        resp = sock.recv(2048)
        if resp != '':
            print(f"Processing {resp}")
            time.sleep(random.randint(2, 5))
    except BrokenPipeError:
        print("Connection lost")
        raise SystemExit(0)

