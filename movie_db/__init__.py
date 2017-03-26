#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys

if sys.version_info < (3, 3):
    print("Please use Python 3.3+")
    sys.exit()


from .scanner import scan_directory
from .reader import db_reader
