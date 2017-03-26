#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sqlite3
from os import system
from terminaltables import AsciiTable
from shutil import get_terminal_size

try:
    input = raw_input
except NameError:
    pass

# Global Database handles
conn = None
c = None

column_width = {
    'title': None,
    'imdb': None,
    'year': None,
    'genre': None,
    'released': None,
    'actors': None,
    'runtime': None,
    'awards': None,
    'plot': None,
    }


def calc_column_width():

    global column_width
    width = get_terminal_size((80, 24))[0]

    column_width['title'] = int(width * 0.2)
    column_width['imdb'] = int(width * 0.06)
    column_width['title'] = int(width * 0.2)


def clear_screen():
    ret_code = system('clear')    # Linux clearscreen
    if ret_code != 0:
        system('cls')       # Windows clearscreen


def display_table(table):
    print(table.table.encode('utf-8'))


def tabularize(table_data):
    table = AsciiTable(table_data)
    table.inner_row_border = True
    table.justify_columns = {0: 'center', 1: 'center', 2: 'center'}
    return table


def format_width(string, width):

    if len(string) <= width:
        return string

    s = width

    for i in range(width, 1, -1):
        if string[i] == ' ':
            s = i
            break

    string = string[:s] + '\n' + format_width(string[s+1:], width)
    return string


def display_movie_details(movie):
    'Print the details of the selected movie in a tabulated form'
    title = movie[1].encode('utf-8')
    year = movie[2].encode('utf-8')
    imdbRating = movie[3]
    table = []

    movie_info = c.execute(
        "select plot,actors,awards,genre,released,runtime from movies where "
        "title=? and year=?", (title, year))
    movie_info = movie_info.fetchone()
    if movie_info is None:
        plot = 'N/A'
        actors = 'N/A'
        awards = 'N/A'
        genre = 'N/A'
        released = 'N/A'
        runtime = 'N/A'
    else:
        plot = movie_info[0].encode('utf-8', 'ignore')
        actors = movie_info[1].encode('utf-8', 'ignore')
        awards = movie_info[2].encode('utf-8', 'ignore')
        genre = movie_info[3].encode('utf-8', 'ignore')
        released = movie_info[4].encode('utf-8', 'ignore')
        runtime = movie_info[5].encode('utf-8', 'ignore')

    table.append(['Movie Title', format_width(title, 20)])
    table.append(['Year', year])
    table.append(['IMDB Rating', str(imdbRating)])
    table.append(['Genre', format_width(genre, 20)])
    table.append(['Released', released])
    table.append(['Actors', format_width(actors, 25)])
    table.append(['Awards', awards])
    table.append(['Runtime', format_width(runtime, 15)])
    table.append(['Plot', format_width(plot, 35)])

    table = tabularize(table)
    display_table(table)

    '''
    print("#" * 60)
    print("\n\t Movie Name :-  " + title)
    print("\n\n\t Year :-  " + year)
    print("\n\t IMDB Rating :-  " + str(imdbRating))
    print("\n\t Genre :-  " + genre)
    print("\n\t Released :-  " + released)
    print("\n\t Actors :-  " + actors)
    print("\n\t Awards :-  " + awards)
    print("\n\t Runtime :-  " + runtime)
    print("\n\t Plot :- " + plot)
    print("\n")
    print("#" * 60)
    '''

    print("\n\t Press ENTER to continue ..... ", end='')
    input()
    clear_screen()


def build_movie_table():

        # Skeleton of Table Structure
        movie_table = [['Sr.No.', 'TITLE', 'YEAR', 'IMDB']]

        # List of movies which cannot be sorted based on IMDB ratings
        imdb_na = []

        for i in c.execute("select title,year,imdbRating from movies "
                           " order by imdbRating desc"):

            row = list(i)

            # If the movie name is greater than 28 characters, format it well
            # to display it within the column width
            # TODO :- Make it more generic
            if len(row[0].encode('utf-8', 'ignore')) > 28:
                s = 0
                for k in range(28, len(i[0])):
                    if row[0][k] == ' ':
                        s = k
                        break
                row[0] = row[0][:s] + '\n' + row[0][s:]

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
    'Main driver function'

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
        except ValueError:
            print("\n\t Please enter a valid choice ..\n")
            continue

        if(choice < 0 or choice > len(movie_table)+1):
            print("\n\t Please enter a valid choice ..\n")
        if choice == 0:
            break

        display_movie_details(movie_table[choice])
        display_table(table_view)
