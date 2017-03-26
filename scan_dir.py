#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''

DESCRIPTION:
    Scans through all the files and directories in a given directory
    one level deep, tries to find a movie which matches the name of a
    file in the directory one-level deep, and if found one, stores its
    information in a Local SQLite Database, for later usages.
    It uses OMDB's API for fetching the information about a movie.

AUTHOR:
    Shubham Dighe <digsblogger@gmail.com>

EXAMPLE Usage:
    python run.py <DIRECTORY_PATH>

'''

import os
import sys
from movie_db import scan_directory

if len(sys.argv) < 2:
    print("Enter the directory to scan :- ", end='')
    directory = input()
else:
    directory = sys.argv[1]

if not os.path.isdir(directory):
    print("Enter a valid directory path ..")
    print("Directory '%s' does not exist" % directory)
else:
    scan_directory(directory)
