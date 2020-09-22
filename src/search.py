from memedict import search
from sys import argv

def descript(name):
    return(search(name))

def main(argv):
    print(search(argv[1]))

if __name__ == "__main__":
    main(argv)