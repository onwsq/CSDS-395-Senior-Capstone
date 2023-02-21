import csv
import numpy as np
import pandas as pd
import imdb
import requests
import re
from datetime import date
from collections import Counter
import datetime
from imdb import IMDb

def getActorPref():
    actor_name = input("Do you have a preference for a specific actor? If so, please enter their name. Otherwise, enter 'no': ")
    if actor_name == 'no':
        actor_name = None
    return actor_name

def getGenrePref():
    genre = input("Choose a genre: ")
    return genre

def getReleaseYearRange():
    while True:
        print("Select a release year range:")
        print("1. Before 2000s")
        print("2. 2000s")
        print("3. 2010s")
        print("4. Just Released (<2 years)")
        release_year_range = input("Enter your choice (1, 2, 3, or 4): ")
        if release_year_range in ["1", "2", "3", "4"]:
            break  # Exit the loop if the input is valid
        else:
            print("Enter a valid response (1, 2, 3, or 4): ")

    if release_year_range == '1':
        release_year_range = ('1900', '1999')
    elif release_year_range == '2':
        release_year_range = ('2000', '2023')
    elif release_year_range == '3':
        release_year_range = ('2010', '2023')
    elif release_year_range == '4':
        release_year_range = ('2021', '2023')
    else:
        release_year_range = None
    return release_year_range

def getDurationRange():
    while True:
        print("Select a duration range:")
        print("1. Under 2 hours")
        print("2. Over 2 hours")
        duration_range = input("Enter your choice (1 or 2): ")
        if duration_range in ["1", "2"]:
            break
        else:
            print("Enter a valid response (1 or 2): ")

    if duration_range == '1':
        duration_range = ('0', '120')
    elif duration_range == '2':
        duration_range = ('120', '1000')
    else:
        duration_range = None
    return duration_range


def get_actor_movies(actor_name):
    '''

    # search for the actor by name
    search_results = ia.search_person(actor_name)
    print(search_results)

    # get the person ID for the first search result
    person_id = search_results[0].getID()
    print(person_id)
    # get the person object for that ID
    person = ia.get_person(person_id)

    # update the person object with filmography data
    ia.update(person, 'filmography')

    movies = []
    # loop through the filmography and print the titles of the movies
    for credit_type in person['filmography']:
        if credit_type == 'actor':
            for movie in person['filmography'][credit_type]:
                title = movie['title']
                movies.append(title)

    return movies
'''

    # search for the actor by name
    search_results = ia.search_person(actor_name)

    '''# print out the IDs of the search results
    for person in search_results:
        print(person.personID, person['name'])
    '''

    # get the person ID
    person_id = search_results[0].personID
    #print(person_id)
    # get the person object for that ID
    person = ia.get_person(person_id)
    #print(person)
    # update the person object with filmography data
    ia.update(person, 'filmography')

    movies = []
    # loop through the filmography and print the titles of the movies
    for credit_type in person['filmography']:
        if credit_type == 'actress':
            for movie in person['filmography'][credit_type]:
                title = movie['title']
                movies.append(title)
                #print(title)

    return movies

def getMoviesByGenre(genre):
    # get the top 50 movies in the specified genre
    top50 = ia.get_top50_movies_by_genres(genre)
    print(top50)
    # extract the top 5 movies from the list
    top5 = [movie["title"] for movie in top50[:5]]

    # print the top 5 movies
    print(f"Top 5 movies in the {genre} genre:")
    for i, movie in enumerate(top5):
        print(f"{i + 1}. {movie}")


def main():
    username = input("Enter your username: ")
    #TODO: Give the most popular movies within the users top genres.
    # Look up the user's username to find their profile and get their top genres
    # show the top 3-5? movies from their top genres
    # give links to the movies

    # if they dont want any of those movies:
    actor_name = getActorPref()
    if actor_name is not None:
        actorMoviesList = get_actor_movies(actor_name)
        print(f"\nHere are movies {actor_name} is in:")
        print(actorMoviesList)
    else:
        genre = getGenrePref()
        releaseYearRange = getReleaseYearRange()
        durationRange = getDurationRange()

        genreMoviesList = getMoviesByGenre(genre)
        print(genreMoviesList)

    print("\nYour preferences: ")
    if actor_name:
        print(f"Actor: {actor_name}")
    else:
        print(f"Genre: {genre}")
        print(f"Release Year Range: {releaseYearRange}")
        print(f"Duration Range: {durationRange}")

ia = IMDb()
main()