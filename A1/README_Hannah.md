"HannahSophie08-WordCount.cpp" takes an input text file, reads the contents, counts the number of words as well as the number of different words and either outputs these counts or a list of the words with the respective count. The code is written in C++. 

# Compile: 
clang++ -std=c++14 HannahSophie08-WordCount.cpp -o HannahSophie08-WordCount

# Run the code: 
./HannahSophie08-WordCount input.txt

# Options:
- "-I" => Ignores uppercase characters and changes them to lowercase. When using this option "Hello" and "hello" are considered the same word
- "-l" => a sorted list of the words (sorted by count and then by alphabet) and their respective count is printed
- "-o output_file.txt" => output is written in defined output file 

# Output:
- without "l": different words / total words
- with "l": list of words and their counts, sorted by count and for identical counts by the alphabet
- with "-o output_file.txt": output is written in output file, otherwise it is printed to the terminal 

# Example 
- Example input: "Hello world, hello world, example.
- ./HannahSophie08-WordCount input.txt 
    output: 3 / 5 
- ./HannahSophie08-WordCount input.txt -l
    output: 
    world 2
    Hello 1
    example 1
    hello 1
- ./HannahSophie08-WordCount input.txt -l -I
    output: 
    hello 2
    world 2
    example 1

# Information:
- Compiler: clang++
- C++ Version: C++14

19.03.2026

    




=> C++14