#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sqlite3
from os import system
from os import sep as path_sep
from terminaltables import AsciiTable
from shutil import get_terminal_size


# Global Database handles
conn = None
c = None


def clear_screen():
    ret_code = system('clear')    # Linux clearscreen
    if ret_code != 0:
        system('cls')       # Windows clearscreen


def display_table(table):
    print("\n")
    print(table.table)


def tabularize(table_data):
    table = AsciiTable(table_data)
    table.inner_row_border = True
    table.justify_columns = {0: 'center', 1: 'center', 2: 'center'}
    return table


def format_width(string, width, sep=' '):
    'Formats a string within the given width, where width is in percentage \
    of the total terminal width'

    term_width = get_terminal_size((80, 20))[0]
    col_width = int((term_width * width) / 100)

    if len(string) <= col_width:
        return string

    s = col_width

    for i in range(col_width, 1, -1):
        if string[i] == sep:
            s = i
            break

    string = string[:s] + sep + '\n' + format_width(string[s+1:], width)
    return string


def display_movie_details(movie):
    'Print the details of the selected movie in a tabulated form'

    title = movie[1].replace('\n', '')
    year = movie[2]
    imdbRating = movie[3]
    table = []

    movie_info = c.execute(
        "SELECT plot, actors, awards, genre, released, runtime, file "
        "FROM movies WHERE title=? AND year=?", (title, year))
    movie_info = movie_info.fetchone()

    plot = movie_info[0]
    actors = movie_info[1]
    awards = movie_info[2]
    genre = movie_info[3]
    released = movie_info[4]
    runtime = movie_info[5]
    file = movie_info[6]

    table.append(['Movie Title', format_width(title, 70)])
    table.append(['Year', year])
    table.append(['IMDB Rating', str(imdbRating)])
    table.append(['Genre', format_width(genre, 70)])
    table.append(['Released', format_width(released, 70)])
    table.append(['Actors', format_width(actors, 70)])
    table.append(['Awards', format_width(awards, 70)])
    table.append(['Runtime', format_width(runtime, 70)])
    table.append(['Plot', format_width(plot, 70)])
    table.append(['File Location', format_width(file, 70, path_sep)])

    table = tabularize(table)
    display_table(table)

    print("\n\t     Press ENTER to continue ..... ", end='')
    input()
    clear_screen()


def build_movie_table():

        # Skeleton of Table Structure
        movie_table = [['Sr.No.', 'TITLE', 'YEAR', 'IMDB']]

        # List of movies which cannot be sorted based on IMDB ratings
        imdb_na = []

        for i in c.execute("SELECT title,year,imdbRating FROM movies "
                           "ORDER BY imdbRating DESC"):

            row = list(i)

            row[0] = format_width(row[0], 60)

            if str(row[2]) == 'N/A':
                imdb_na.append(row)
            else:
                movie_table.append(row)

        # Add movies with no IMDB rating at the end
        for i in imdb_na:
            movie_table.append(i)

        for i in range(1, len(movie_table)):
            movie_table[i] = [i] + movie_table[i]

        return movie_table


def db_reader(db_file):
    'Main driver function for the reader program'

    # Initialize Database Handlers
    global conn, c
    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    movie_table = build_movie_table()
    table_view = tabularize(movie_table)
    display_table(table_view)

    while 1:
        print("\n\n\t Enter a movie number (0 to exit) :- ", end='')
        choice = input()

        try:
            choice = int(choice)
            if(choice < 0 or choice > len(movie_table)):
                raise ValueError
        except ValueError:
            print("\n\t Please enter a valid choice ..\n")
            continue

        if choice == 0:
            print("\n")
            break

        display_movie_details(movie_table[choice])
        display_table(table_view)
