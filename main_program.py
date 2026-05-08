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

def parse_u64(value):
    try:
        number = int(value)

        # Convert into unsigned 64-bit bytes.
        unsigned_bytes = number.to_bytes(8, "big", signed=False)

        # Convert back from unsigned bytes into Python integer.
        return int.from_bytes(unsigned_bytes, "big", signed=False)

    except OverflowError:
        raise ValueError("number outside unsigned 64-bit range")

    except ValueError:
        raise ValueError("invalid unsigned 64-bit integer")


def search_tree(file, block_id, key):
    if block_id == 0:
        return None

    node = read_node(file, block_id)

    i = 0
    while i < len(node.keys) and key > node.keys[i]:
        i += 1

    if i < len(node.keys) and key == node.keys[i]:
        return key, node.values[i]

    if node.children[i] == 0:
        return None

    return search_tree(file, node.children[i], key)


def search_index(filename, key):
    if not os.path.exists(filename):
        print("ERROR: index file does not exist")
        return

    try:
        with open(filename, "rb") as file:
            root_id, next_id = read_header(file)
            result = search_tree(file, root_id, key)

            if result is None:
                print("ERROR: key not found")
            else:
                print(f"{result[0]},{result[1]}")

    except Exception:
        print("ERROR: invalid index file")



def insert_into_leaf(node, key, value):
    i = len(node.keys) - 1

    node.keys.append(0)
    node.values.append(0)

    while i >= 0 and key < node.keys[i]:
        node.keys[i + 1] = node.keys[i]
        node.values[i + 1] = node.values[i]
        i -= 1

    node.keys[i + 1] = key
    node.values[i + 1] = value


def split_child(file, parent, index, child, next_id):
    new_child = Node(next_id, parent.block_id)

    median_key = child.keys[T - 1]
    median_value = child.values[T - 1]

    new_child.keys = child.keys[T:]
    new_child.values = child.values[T:]

    child.keys = child.keys[:T - 1]
    child.values = child.values[:T - 1]

    if not child.is_leaf():
        new_child.children = child.children[T:]
        child.children = child.children[:T] + [0] * T

        for child_id in new_child.children:
            if child_id != 0:
                temp = read_node(file, child_id)
                temp.parent = new_child.block_id
                write_node(file, temp)

    parent.keys.insert(index, median_key)
    parent.values.insert(index, median_value)
    parent.children.insert(index + 1, new_child.block_id)
    parent.children = parent.children[:MAX_CHILDREN]

    write_node(file, child)
    write_node(file, new_child)
    write_node(file, parent)

    return next_id + 1


def insert_non_full(file, node, key, value, next_id):
    i = len(node.keys) - 1

    if node.is_leaf():
        insert_into_leaf(node, key, value)
        write_node(file, node)
        return next_id

    while i >= 0 and key < node.keys[i]:
        i -= 1

    i += 1
    child = read_node(file, node.children[i])

    if len(child.keys) == MAX_KEYS:
        next_id = split_child(file, node, i, child, next_id)

        node = read_node(file, node.block_id)

        if key > node.keys[i]:
            i += 1

    child = read_node(file, node.children[i])
    return insert_non_full(file, child, key, value, next_id)


def insert_index(filename, key, value):
    if not os.path.exists(filename):
        print("ERROR: index file does not exist")
        return

    try:
        with open(filename, "r+b") as file:
            root_id, next_id = read_header(file)

            existing = search_tree(file, root_id, key)
            if existing is not None:
                print("ERROR: duplicate key")
                return

            if root_id == 0:
                root = Node(next_id)
                insert_into_leaf(root, key, value)

                write_node(file, root)
                write_header(file, root.block_id, next_id + 1)

                print("Inserted")
                return

            root = read_node(file, root_id)

            if len(root.keys) == MAX_KEYS:
                new_root = Node(next_id)
                next_id += 1

                new_root.children[0] = root.block_id
                root.parent = new_root.block_id
                write_node(file, root)

                next_id = split_child(file, new_root, 0, root, next_id)
                root_id = new_root.block_id

                new_root = read_node(file, root_id)
                next_id = insert_non_full(file, new_root, key, value, next_id)
            else:
                next_id = insert_non_full(file, root, key, value, next_id)

            write_header(file, root_id, next_id)
            print("Inserted")

    except Exception:
        print("ERROR: invalid index file")


def main():
    if len(sys.argv) < 2:
        print("ERROR: missing command")
        return

    command = sys.argv[1]

    try:
        if command == "create":
            if len(sys.argv) != 3:
                print("ERROR: create requires an index filename")
                return

            create_index(sys.argv[2])

        elif command == "search":
            if len(sys.argv) != 4:
                print("ERROR: search requires an index filename and key")
                return

            key = parse_u64(sys.argv[3])
            search_index(sys.argv[2], key)

        elif command == "insert":
            if len(sys.argv) != 5:
                print("ERROR: insert requires an index filename, key, and value")
                return

            key = parse_u64(sys.argv[3])
            value = parse_u64(sys.argv[4])
            insert_index(sys.argv[2], key, value)

        else:
            print("ERROR: unknown command")

    except ValueError:
        print("ERROR: key and value must be unsigned 64-bit integers")


if __name__ == "__main__":
    main()