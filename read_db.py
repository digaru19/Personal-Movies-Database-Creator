#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''

DESCRIPTION:
    It is a reader utility for the Movies Database created by the
    'scan_dir.py' utility. It lists the movies in the descending order of
    their IMDb ratings.

AUTHOR:
    Shubham Dighe <digsblogger@gmail.com>

EXAMPLE Usage:
    python read_db.py <DATABASE_FILE_PATH>

'''


import os
import sys
from movie_db import db_reader

DEFAULT_DB = 'movies.db'

if len(sys.argv) < 2:
    print("\n No Database File specified !!")
    print(" Using default : %s " % DEFAULT_DB)
    db_file = DEFAULT_DB
else:
    db_file = sys.argv[1]

if not os.path.isfile(db_file):
    print("Please specify a valid file path ..")
    print("File '%s' does not exist" % db_file)
else:
    db_reader(db_file)
