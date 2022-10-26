#!python3

# Sequentiell implementation of map reduce 
# (does not make sense, just for learning purposes)

import sys

def mapf():
    pass

def reducef():
    pass

def main():
    if len(sys.argv) < 2:
        print(f"Usage: {__filename__} inputfiles")

    input_files = sys.argv[1:]
    print(input_files)


main()
