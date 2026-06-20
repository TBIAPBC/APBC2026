## A1 - Word Count

- Counts words in the input stream as specified in [README.md](./README.md)
- Implemented in python using only standard library modules.
- Tested using python 3.12.12 on Ubuntu 24.04.3 LTS under WSL.

### Usage examples

```bash
./juwei95-WordCount.py < dateiname
./juwei95-WordCount.py -I dateiname
./juwei95-WordCount.py -l -I dateiname
```

### Troubleshooting

If `bash` refuses to execute the script try running:

```bash
chmod +x juwei95-WordCount.py
```

Or explicitly feed the script to your python3 interpreter:

```bash
python juwei95-WordCount.py
```

