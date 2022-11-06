#!python3

from typing import List, Tuple
from itertools import groupby
import sys
import re

# Sequential implementation of map reduce 
# (does not make sense, just for learning purposes)

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


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {__file__} inputfiles")
        raise SystemExit(1)

    input_files = sys.argv[1:]

    # Intermediate result structure returned from map
    intermediate = []

    # Read content of every input file and pass to map function
    for file in input_files:
        with open(file) as f:
            content = f.read()
            intermediate.extend(mapf(file, content))

    keyFunc = lambda x: x[0]

    # sort intermediate
    intermediate.sort(key=keyFunc)

    output_file = "mr-out-seq-py.txt"


    # Call the reduce function for every element that has the same key. 
    with open(output_file, "wt") as f:
        # Group by first attribute
        for key, group in groupby(intermediate, key=keyFunc):
            group = list(group)
            reduction = reducef(key, group)
            f.write(f"{key} {reduction}\n")
    

main()
