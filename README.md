# GITHUB LINK

https://github.com/Aditya-Yan/CS4348_Project_3


## Overview

This project implements a command-line index file manager which uses a B-Tree that is stored inside a binary file. This program supports creating index files, inserting key/value pairs, searching for keys, loading data from CSV files, extracting to CSV files as well, and printing the contents of the tree to the standard output.

The B-Tree is stored using a fixed-size 512-byte blocks and it uses a minimum degree of 10. All integers are stored as an unsigned 64-bit big-endian value

This program was implemented in Python.

---

# Files

## project3.py
This is the main program that the user runs.

Features:
- Command-Line Interfaces: This program supports create, insert, search, load, print, and extract commands from the command line with their arguments.
- Persistent Storage: Stores the B-Tree directly inside a binary index file as mentioned
- Fixed Block Structure: Every node occupies exactly one 512-byte block
- Supports CSV: Can extract data from B-Tree to a CSV and load data from a CSV to a B-Tree
- Error Handling: Is able to handle errors such as invalid commands, invalid arguments, duplicate keys, values/keys out of range, and missing files

# Commands

## Create an Index File

```bash
python3 project3.py create test.idx
```

Creates a new empty index file.

---

## Insert a Key/Value Pair

```bash
python3 project3.py insert test.idx 15 100
```

Inserts the key/value pair into the B-Tree.

---

## Search for a Key

```bash
python3 project3.py search test.idx 15
```

Searches the B-Tree for the given key and prints the key/value pair if found.

---

## Load Data From a CSV File

```bash
python3 project3.py load test.idx input.csv
```

Loads comma-separated key/value pairs from a CSV file into the index.

### Example CSV Format

```text
15,100
20,200
35,500
```

---

## Print All Key/Value Pairs

```bash
python3 project3.py print test.idx
```

Prints all key/value pairs in sorted order.

---

## Extract Data Into a CSV File

```bash
python3 project3.py extract test.idx output.csv
```

Extracts all key/value pairs into a CSV file.

---

# How to Run the Program

## Requirements
- Python 3 installed

Run commands using:

```bash
python3 project3.py <command> <arguments>
```


# Notes

- The program stores all numbers as unsigned 64-bit integers using big-endian byte order, duplicate keys are not allowed, and each node can contain up to 19 keys