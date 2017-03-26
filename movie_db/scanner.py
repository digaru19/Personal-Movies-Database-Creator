#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re
import requests
import sqlite3
import os
import time


API_URL = 'http://www.omdbapi.com/'
LOCAL_DB = 'movies.db'
num_movies_found = 0
new_movies_found = 0


def init_database():
    'Initializes a Local Database'
    print("Local Database File :- %s" % LOCAL_DB)
    conn = sqlite3.connect(LOCAL_DB)
    c = conn.cursor()

    # Create the movies information table
    c.execute("""CREATE TABLE IF NOT EXISTS movies
               ( movie_id INTEGER PRIMARY KEY,
               title VARCHAR(200), year VARCHAR(20), imdbRating REAL,
               plot TEXT, actors TEXT, awards TEXT, genre VARCHAR(100),
               released VARCHAR(40), runtime VARCHAR(50), file VARCHAR(250));
                """)

    conn.commit()
    return conn


def sanitize_movie_name(movie_name):

    movie_name = movie_name.strip()

    chars_to_delete = '@=+/'
    for i in chars_to_delete:
        movie_name = movie_name.replace(i, '')

    chars_to_space = '.-_[]()'
    for i in chars_to_space:
        movie_name = movie_name.replace(i, ' ')

    return movie_name


def print_movie_info(movie_data):
    print("    " + '='*50)
    print("\t Movie Title :- %s " % movie_data.get('Title', 'N/A'))
    print("\t Year  :- %s" % movie_data.get('Year', 'N/A'))
    print("\t IMDB Rating  :- %s" % movie_data.get('imdbRating', 'N/A'))
    print("    " + '='*50)


def print_not_found(movie):
    print("    " + 'x'*50)
    print("\t Found nothing about \"" + movie + "\" !!")
    print("\t Skipping %s" % movie)
    print("    " + 'x'*50)


def write_to_db(cursor, movie_details):
    'Writes details about a movie to the local database'

    global new_movies_found, num_movies_found

    num_movies_found += 1

    # If Movie details already exist in the database, skip
    movie_name = movie_details.get('Title', 'N/A')
    cursor.execute("SELECT count(*) from movies "
                   "where title = ?", (movie_name,))

    if cursor.fetchone()[0] >= 1:
        print("    Movie :- '%s' already exists "
              "in the Local Database" % movie_name)
        return

    new_movies_found += 1
    # Fields in the table :-
    # title year imdbRating plot actors awards genre released runtime

    details = []
    details.append(movie_details.get('Title', 'N/A'))
    details.append(movie_details.get('Year', 'N/A'))
    details.append(movie_details.get('imdbRating', 'N/A'))
    details.append(movie_details.get('Plot', 'N/A'))
    details.append(movie_details.get('Actors', 'N/A'))
    details.append(movie_details.get('Awards', 'N/A'))
    details.append(movie_details.get('Genre', 'N/A'))
    details.append(movie_details.get('Released', 'N/A'))
    details.append(movie_details.get('Runtime', 'N/A'))
    details.append(movie_details.get('file', 'N/A'))
    details = tuple(details)
    cursor.execute(
        "INSERT INTO movies VALUES (NULL,?,?,?,?,?,?,?,?,?,?);", details)


def fetch_movie_data(params):

    found = False
    tries = 0
    time.sleep(1)  # Do not flood the servers  :)
    data = None

    while tries < 4:
        try:
            data = requests.get(url=API_URL, params=params)
            break
        except requests.exceptions.RequestException:
            tries += 1
            print("    Connection with the remote host failed."
                  " Retrying %d/4 .." % tries)
            time.sleep(1)

    if data is None:
        return False

    try:
        data = data.json()
    except:
        return False

    if data.get('Response', 'False') == 'True':
        # Found the (correct) movie. Hope so :)
        found = True

    if found:
        return data
    else:
        return False


def scan_directory(directory):

    conn = init_database()
    cursor = conn.cursor()

    directory = os.path.abspath(directory)

    file_list = os.listdir(directory)

    year_re = re.compile("[0-9]{4}")

    for file_name in file_list:

        movie = sanitize_movie_name(file_name)
        found = False

        print("\n    Searching for :- '%s' " % file_name)

        digits = year_re.finditer(movie)

        # First, search with movie name and year (if available)
        if digits:
            for year in digits:
                if int(year.group()) >= 1900 and int(year.group()) <= 2018:
                    k = year.span()[0] - 1
                    params = dict(t=movie[:k], y=str(year.group()),)

                    data = fetch_movie_data(params)

                    if data:
                        print_movie_info(data)
                        data['file'] = os.path.join(directory, file_name)
                        found = True
                        write_to_db(cursor, data)
                        break

        if found:
            conn.commit()
            continue

        # If year is not present in the file name, search with the
        # complete movie name, dropping the last word at each try

        no_of_words = len(movie.split())
        name = movie

        for q in range(no_of_words):

            params = dict(t=name,)

            data = fetch_movie_data(params)

            if data:
                # Display movie information, and write it to Local Database
                print_movie_info(data)
                data['file'] = os.path.join(directory, file_name)
                found = True
                write_to_db(cursor, data)
                break

            # Till now, found nothing about the Movie. Remove the last word
            # from the file name, and try again
            name = " ".join(name.split()[:-1])

        if found:
            conn.commit()
            continue
        else:
            print_not_found(file_name)

    conn.commit()
    conn.close()

    print("\n")
    print("\t Found %d new movies !! " % new_movies_found)
    print("\t Found %d total movies !! " % num_movies_found)
    print("\n")
