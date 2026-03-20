#!/bin/bash

set -x

python juwei95-WordCount.py WordCount-test1.in | diff - WordCount-test1.out &&
python juwei95-WordCount.py -l WordCount-test2.in | diff - WordCount-test2.out &&
python juwei95-WordCount.py -l -I WordCount-test3.in | diff - WordCount-test3.out
