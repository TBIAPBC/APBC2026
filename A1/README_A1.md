# A1 Assignment, Word Count
A pythons script which uses command-line tools to count word frequencies in text files. It supports all languages and case insensitivity.

## Usage
Run the script from the terminal by providing a text file as the primary argument.

### Basic Command
By default, the script prints only the **total word count** found in the file.

```bash
python WordCount.py input.txt

| Flag | Full Name | Description |
| :--- | :--- | :--- |
| **-l** | `--list` | **List Mode**: Displays every unique word and its frequency, sorted by count (highest first) and alphabetically for ties. |
| **-I** | `--ignore_case` | **Case Insensitivity**: Treats "Word" and "word" as the same entry. |
| **-h** | `--help` | Displays the help menu with all available arguments. |
