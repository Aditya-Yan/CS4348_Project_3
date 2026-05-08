# Development Log

## 05-08-26 2:39 AM

For this project, I need to implement a command-line program that will create and manage index files. As it was described in the project instructions, I need to support create, insert, soach, load, print, and extract commands. For this project I plan on using Python because I feel that it will be the simplest to implement with its file handling and built-in support for converting integers to 8-byte big-endian format. This will save me time when doing the project.

### Plan

I plan on doing this project in six sessions which I will list below

1. Create constants, header logic, and the create command
2. Implement node serialization and deserialization
3. Implement search
4. Implement insertion without splitting
5. Implement full B-Tree insertion with splitting
6. Implement load, print, extract, and final error handling