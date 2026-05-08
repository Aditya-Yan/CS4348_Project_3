import sys
import os

BLOCK_SIZE = 512
MAGIC = b"4348PRJ3"
HEADER_SIZE = 24

T = 10
MAX_KEYS = 2 * T - 1
MAX_CHILDREN = 2 * T


class Node:
    def __init__(self, block_id, parent=0, keys=None, values=None, children=None):
        self.block_id = block_id
        self.parent = parent
        self.keys = keys if keys is not None else []
        self.values = values if values is not None else []
        self.children = children if children is not None else [0] * MAX_CHILDREN

    def is_leaf(self):
        return all(child == 0 for child in self.children)


def write_u64(file, value):
    file.write(value.to_bytes(8, "big"))


def read_u64(file):
    return int.from_bytes(file.read(8), "big")


def read_header(file):
    file.seek(0)
    magic = file.read(8)

    if magic != MAGIC:
        raise ValueError("invalid index file")

    root_id = read_u64(file)
    next_id = read_u64(file)

    return root_id, next_id


def write_header(file, root_id, next_id):
    file.seek(0)
    file.write(MAGIC)
    write_u64(file, root_id)
    write_u64(file, next_id)
    file.write(bytes(BLOCK_SIZE - HEADER_SIZE))


def read_node(file, block_id):
    file.seek(block_id * BLOCK_SIZE)

    stored_block_id = read_u64(file)
    parent = read_u64(file)
    num_keys = read_u64(file)

    keys = [read_u64(file) for _ in range(MAX_KEYS)]
    values = [read_u64(file) for _ in range(MAX_KEYS)]
    children = [read_u64(file) for _ in range(MAX_CHILDREN)]

    return Node(
        stored_block_id,
        parent,
        keys[:num_keys],
        values[:num_keys],
        children
    )


def write_node(file, node):
    file.seek(node.block_id * BLOCK_SIZE)

    write_u64(file, node.block_id)
    write_u64(file, node.parent)
    write_u64(file, len(node.keys))

    padded_keys = node.keys + [0] * (MAX_KEYS - len(node.keys))
    padded_values = node.values + [0] * (MAX_KEYS - len(node.values))
    padded_children = node.children + [0] * (MAX_CHILDREN - len(node.children))

    for key in padded_keys:
        write_u64(file, key)

    for value in padded_values:
        write_u64(file, value)

    for child in padded_children[:MAX_CHILDREN]:
        write_u64(file, child)

    used_bytes = 8 + 8 + 8 + 152 + 152 + 160
    file.write(bytes(BLOCK_SIZE - used_bytes))


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