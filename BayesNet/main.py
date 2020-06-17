from ReadInput import *


def main():
    rp = ReadInput("input.txt")
    rp.generate()
    rp.model.println()
if __name__ == "__main__":
    main()
