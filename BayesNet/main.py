import sys, getopt
from ReadInput import *

def main(argv):
    inputfile = ''
    testfile = ''
    opts, args = getopt.getopt(argv,"hi:i:",["model=","test="])
    for opt, arg in opts:
        if opt in ("--model"):
            inputfile = arg
        elif opt in ("--test"):
            testfile = arg
    rp = ReadInput(inputfile)
    rp.generate()
    rp.model.println()
    tp = ReadInput(testfile)
    print(tp.file.read())

if __name__ == "__main__":
    main(sys.argv[1:])