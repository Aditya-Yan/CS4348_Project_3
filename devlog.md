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

## 05-08-26 2:48 AM

### Session 1
I will start this project by implementing the file header and create command.

When doing this, I need to make sure that the block ids are correct. The index file begins with the magic number, root block id, and the next block id. Since the tree is going to start empty, the root block id is 0. The next block id will start at 1 because block 0 is going to be reserved for the header.

### Session Reflection
This section was pretty straightforward. The only thing I had to actually be careful of was to make sure that every number was written as a 8-byte big-endian integer. I also made sure to include the feature where create will fail if the file exists. I am also adding the logic for accepting command line arguments as I create these commands so it is easier for me to test. Overall, pretty easy section to implement. 