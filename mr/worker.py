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
import pickle
import re
from typing import Tuple, List

def mapf(filename: str, content: str) -> Tuple[str, int]:
    """
    Filename is currently not used.
    Content is split by words
    Returns a list with every word and count 1
    """
    regex = r"[^\w]"
    words = [word for word in re.split(regex, content) if word]

    # Return our intermediate result
    return [(word, 1) for word in words]

def reducef(word: str, values: List):
    return len(values)

addr = ('localhost', 20_001)

sock = socket(AF_INET, SOCK_STREAM)
sock.connect(addr)
print(f"Connected to {addr}")

while True:
    try:
        sock.send(b'next')
        resp = sock.recv(4096)
        if resp != '':
            func, content = pickle.loads(resp)
            if func == "mapf":
                result = mapf("", content)
                sock.send(pickle.dumps(result))
            elif func == "reducef":
                ...
            else:
                print(f"Critical error. Received unknown function {func}")
                raise SystemExit(1)
            print(f"Processing {func}, {content}")
            time.sleep(random.randint(2, 5))
    except BrokenPipeError:
        print("Connection lost")
        raise SystemExit(0)

