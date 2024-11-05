# Programming Challenge
Implementation of hiring interview programming challenge for <company name removed>.

## Problem

You are given a very, very large plain text file where each line contains a plain text string. The file has at most 1 billion lines; lines may have different lengths, but each line has at most 1000 characters.

Your goal is to write a program that will print an arbitrary line from the file. Your program will be run many times (although you don't know exactly how many times it will be run in advance), and you don't know in advance which lines might be selected. Thus, your solution should be optimized to minimize the runtime for each additional execution. The first execution of the program may take longer than subsequent runs, and you may use additional disk storage to improve performance.

Your program should take two command-line arguments: the path of the input file from which to print lines, and the index of the line you want to print. Your program should write the line to standard output.

Full challenge description is at file **_Engineer Coding Challenge.pdf_**

## Solution

Solution was implemented using local sqlite3 database, which caches position of every Nth line (configurable through command line parameter) as well as position of already accessed lines.

When accessing specific line, the program gets nearest previous cached position and seeks from there.

Program raises exception, when requesting line exceeding number of lines in file.

## Files

- `random_line.py` Script which prints specific line from large file using caching to speed up

```
usage: random_line.py [-h] [-i INDEXING_INTERVAL] [--debug | --no-debug] [input_file] [index]

Prints an arbitrary line from the file. 
Caches line positions for faster retrival on additional runs.
Cache is stored in file cache.db in te root of the project.

positional arguments:
  input_file
  index

options:
  -h, --help            show this help message and exit
  -i INDEXING_INTERVAL, --indexing_interval INDEXING_INTERVAL
                        Set how often new lines are cached during file traversal.
                        Set to 0 to disable continuous indexing. Default 1000
  --debug, --no-debug   See debug messages
```

- `cache.py` - Implementation of local cache, idea is, that it may be extended to use different type of database or technology to cache lines (eq. Redis) 


- `input_file.txt` - Sample input data


- `create_data.py` - Script used to create test data


```
usage: create_data.py [-h] [-f FILE_NAME] [-l LINES]

Creates text file with a lot of random texts, with a maximum of 1000 chars per line (+ \n).

options:
  -h, --help            show this help message and exit
  -f FILE_NAME, --file_name FILE_NAME
                        Created file name. Default input_file.txt
  -l LINES, --lines LINES
                        Number of generated lines. Default 1 000 000
```

- `requirements.txt` Project requirements

## Instalation
No extra setup is necessary, just install Python (Implemented using version 3.12).

There are no additional libraries required to run the script.

## Notes

- Used `black` to format source files.
Execute command `pip install -r .\requirements.txt` to set it up and `black *.py` command to run it.
- To clear cache delete `cache.db` file which is created on first run.


