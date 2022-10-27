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

def keyFunc(element: Tuple[str, int]):
    return element[0]

def main():
    if len(sys.argv) < 2:
        print(f"Usage: {__filename__} inputfiles")

    input_files = sys.argv[1:]

    # Intermediate result structure returned from map
    intermediate = []

    # Read content of every input file and pass to map function
    for file in input_files:
        with open(file) as f:
            content = f.read()
            intermediate.extend(mapf(file, content))

    # sort intermediate
    intermediate.sort(key=keyFunc)

    output_file = "mr-out-seq-py.txt"

    # Group elements to list by same key 
    grouped_data = {key: group for key, group in groupby(intermediate, key=keyFunc)}

    # Call the reduce function for every element that has the same key. 
    with open(output_file, "wt") as f:
        for key, group in grouped_data.items():
            reduction = reducef(key, list(group))
            f.write(f"{key} {reduction}\n")
    

main()
