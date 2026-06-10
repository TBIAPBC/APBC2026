## A4 Markov Text Generator

A python script which accepts a text file or standard input and generates a new text to terminal via Markov Model.

It implements the dictionary lookup strategy where the input is preprocessed into a markov dictionary which links text slices to possible endings.

## Usage

When using a text file as input:

```
python BeatriceHN-Markov.py file.txt -o int
```

When using standard input:

```
echo 'your input of choice' | python BeatriceHN-Markov.py -o int
```

The recognized the following flags:

| Flag    | Function          | defaults                        |         type      |
|---------|-------------------|---------------------------------|-------------------|
| - o     | Markov order k    |                     1           |   int             |
| - w     | Switch from character generation to word generation | False|    boolean |
| -s      | Seed              | None                   |            int             |
| -l      | Max length of generated text |  None                | int               |

The max length of the generated text should be used when the markov model could be infinite.

## Libraries
The following libraries have been used:
 - sys
 - textwrap
 - numpy
 - argparse