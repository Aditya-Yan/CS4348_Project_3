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

## 05-08-26 3:04 AM

### Session 2

In this session I want to add the B-Tree node structure. On top of this, I am going to add helper functions for reading and writing headers and nodes so I do not have to repeat code.

### Session Reflection

This section also was not too hard to implement, I just had to make sure that I followed the 512-byte block format. I had to make sure that each node stored 19 keys, 19 values, and 20 child pointers. One thing that I did forget to do initally was to pad the unused values with zeros. I realized that I had to do this so that each node would take up exactly one block.

## 05-08-26 3:26 AM

### Session 3

In this session I want to implement the search command. As stated in the project instructions, the search commands expects an index filename and a key. I just have to remember to convert the key into an unsigned integer before searching.

### Mid-Session Thought
I am a little unsure about how I should convert to unsigned integers on whether or not I should use masks as the use of masks would make this project more complicated. I think I am leaning toward not using masks and instead just convert the input into its 8-byte unsigned big-endian representaion using to_bytes()

### Session Reflection

I got the search command working properly and tested it. Was not too bad either. One mistake I did make though was for my unsigned integer conversion, I only checked if the number is negative. I then changed this to make sure that the parser I created also didn't allow values over 2^64 -1. I did this by using pythons to_bytes() function and checked for errors. Also for this section, I am assuming by "converting" to unsigned integers, it is fine to just reject keys that are not in the range from 0 to 2^64 -1 because if we were to just convert using masks, then duplicate detection would become weird and searching would become confusing with huge positive numbers.

## 05-08-26 3:47 AM

### Interjection

I think I will change the plan I had at the beginning of the project a little bit. In this next section, I will just implement the entire insert logic. Then I will split up the rest between the last two sessions. The new plan is as follows:

4. Implement insert command
5. Implement load command and csv argument logic
6. Implement print and extract commands with their argument logic

### Session 4

In this session I am going to implement the insert command with and without splitting. I am expecting this session to be the hardest one as I have to do the B-Tree splitting properly. As stated in the project description, this command expects an index filename, key, and value. Both the key and value are parsed using the unsigned 64-bit parser. In order to efficiently do this section, I will list the different cases I will have to handle in implementing this command. The different cases will the empty tree case, normal leaf insertion, duplicate keys, splitting full children, and creating a new root when the old root is full.

### Mid-Session Thought

This session is definitely hard as I expected. I am messing up small details when implementing these cases which is messing up the entire tree. For example, I chose the wrong median intially when splitting. I also have to be careful with child pointers and parent pointers during splitting because I accidently caused the file structure to become inconsistent if only one is updated correctly.

### Session Reflection

This was definitely the hardest section to do as I expected because of the B-Tree splitting. This is because I had to handle multiple cases such as the empty tree case, normal leaf insertion, duplicate keys, splitting full children, and creating a new root when the old root is full. For example, as I mentioned before, I initially chose the incorrect median key when splitting a full node which was leading to issues. I also forgot to update the root id initially when the new root split which caused future searches to start from the old root and the tree ended up wrong. Finally, I forgot to check for duplicate keys intitially, even though it was in my plan. 