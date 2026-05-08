import sys
import os

BLOCK_SIZE = 512
MAGIC = b"4348PRJ3"
HEADER_SIZE = 24


def write_u64(file, value):
    file.write(value.to_bytes(8, "big"))


def read_u64(file):
    return int.from_bytes(file.read(8), "big")


def create_index(filename):
    if os.path.exists(filename):
        print("ERROR: index file already exists")
        return

    with open(filename, "wb") as file:
        file.write(MAGIC)
        write_u64(file, 0)
        write_u64(file, 1)
        file.write(bytes(BLOCK_SIZE - HEADER_SIZE))

    print("Index file created")


def main():
    if len(sys.argv) < 2:
        print("ERROR: missing command")
        return

    command = sys.argv[1]

    if command == "create":
        if len(sys.argv) != 3:
            print("ERROR: create requires an index filename")
            return

        create_index(sys.argv[2])

    else:
        print("ERROR: unknown command")


if __name__ == "__main__":
    main()