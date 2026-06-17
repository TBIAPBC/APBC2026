# A4 - Markov

Generates random text based on training data.


## Usage

### Synopsis

```bash
juwei95-Markov.py [-h] [-o k] [-w] [-s seed] [filename]
```

### Positional arguments

| Argument   | Description                                                                          |
| ---------- | ------------------------------------------------------------------------------------ |
| `filename` | The input file containing the training data, if omitted the input is read from stdin |

### Options

| Opt       | Option        | Description                                                                                                          |
| --------- | ------------- | -------------------------------------------------------------------------------------------------------------------- |
| `-h`      | `--help`      | Show a help message and exit                                                                                         |
| `-o k`    | `--order k`   | Use Markov order k                                                                                                   |
| `-w`      | `--words`     | Use word-based generation instead of character-based generation                                                      |
| `-s seed` | `--seed seed` | Initialize the random number generator with seed. Same input with the same seed will always produce the same output. |


### Example

```bash
python3 juwei95-Markov.py erlkoenig.txt -o 5
```


## Details

* The next output token is randomly selected from a list of non-unique possible continuations for the current context. The chance of a continuation beeing selected is implicitly determined by its number of occurences in the training data, after the given context.
* ⚠️ ***Warning***: There is no hard limit on the amount of text produced. Chances are that the generator will not terminate by itself. You may have to use `ctrl + c` to kill it.
* Implemented in python using only standard library modules.
* Tested using python 3.12.12 on Ubuntu 24.04.3 LTS under WSL.
