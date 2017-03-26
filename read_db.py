#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''

DESCRIPTION:
    It is a 'reader' utility for the movies database created by the
    'writer' utility.

AUTHOR:
    Shubham Dighe <digsblogger@gmail.com>

EXAMPLE Usage:
    python read_db.py <DATABASE_FILE>

'''


import os
import sys
from movie_db import db_reader

if sys.version_info < (3,):
    print("Please use Python 3.3+")
    sys.exit()

DEFAULT_DB = 'movies.db'

if len(sys.argv) < 2:
    print("\t No Database File specified !!")
    print("\t Using default : %s " % DEFAULT_DB)
    db_file = DEFAULT_DB
else:
    db_file = sys.argv[1]

if not os.path.isfile(db_file):
    print("Enter a valid file path ..")
    print("File '%s' does not exist" % db_file)
else:
    db_reader(db_file)
