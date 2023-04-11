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
    # search for the actor by name
    search_results = ia.search_person(actor_name)
    # get the person ID
    person_id = search_results[0].personID
    # get the person object for that ID
    person = ia.get_person(person_id)
    # update the person object with filmography data
    ia.update(person, 'filmography')

    movies = []
    # loop through the filmography and print the titles of the movies
    for credit_type in person['filmography']:
        if credit_type == 'actress':
            for movie in person['filmography'][credit_type]:
                title = movie['title']
                movies.append(title)

    # if the movies list is empty (actor wasn't found by .personID)
    if not movies:
        # get the person ID using .getID() for the first search result
        person_id = search_results[0].getID()
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

def getMoviesByGenre(genre,N):
    # get the top 50 movies in the specified genre
    top50 = ia.get_top50_movies_by_genres(genre)
    # print(top50)
    test = [movie for movie in top50[:N]]
    print("test list array thing: "+str(test))
    # extract the top 5 movies from the list
    topN = [movie["title"] for movie in top50[:N]]

    # print the top 5 movies
    print(f"\nTop {N} movies in the {genre} genre:")
    for i, movie in enumerate(topN):
        print(f"{i + 1}. {movie}")


# NEW METHOD TO GET PLOT AND MOVIE TITLE
def getMovieAndPlots(genre,N):
    # get the top 50 movies in the specified genre
    top50 = ia.get_top50_movies_by_genres(genre)
    # print(top50)
    topN = top50[:N]
    # extract the top 5 movies from the list

    # print the top 5 movies
    print(f"\nTop {N} movies in the {genre} genre:")
    for i, movie in enumerate(topN):
        ###################### movie.data['plot'] gets the plot summary
        print(f"{i + 1}. {movie['title']}"+"\n"+movie.data['plot'])
        # link = mp.get_poster(title=movie['title'])
        print(movie['cover url'])


# OLIVIA'S INTEGRATED STUFF
# This method reads the data generated from "initial_csv_cleaning.py"
# Reads the list of movies and their associated genres
# returns top 5 main genres
# and returns top 3 subgenres as well
def getTop5(filename):
    # filename would replace the o_movies
    data = pd.read_csv(filename)
    df = data.values
    genres = []
    for i in df:
        # only watched once
        if i[1] == 1:
            temp = i[2:]
            genres = np.concatenate((genres, temp))
        cleaned_genres = [x for x in genres if str(x) != 'nan']

    # list of most common genres for user 1
    common_genres = [genre for genre, val in Counter(cleaned_genres).most_common()]

    if len(common_genres) > 4:
        top_5 = common_genres[0:5]
    else:
        top_5 = common_genres

    # list of all possible sub-genres off of top genres
    res = [(a, b) for idx, a in enumerate(top_5) for b in top_5[idx + 1:]]
    print("this user's top 5:"+str(top_5))
    print("this user's subgenres: "+str(res))
    return [top_5, res]

# This method takes two user profiles and finds their common genres + subgenres
# Utilizes getTop5 method to get list of genres for each user
# and then finds commonalities between them
def getCommonTopGenres(username1, username2):

    # username will replace the hardcoded csv files
    # THIS DATA IS READING CSV CREATED FROM "initial_csv_cleaning.py"
    # BUT WILL PROB BE A DATA BUCKET LATER ON

    # top_5_u[x] is a list of top five genres
    # (Romance, comedy, horror, etc)
    # sub_u[x] is a list of top subgenres derived from top genres
    # (Comedy-horror, Romance-horror, etc)
    top_5_u1 = getTop5('o_movies.csv')[0]
    sub_u1 = getTop5('o_movies.csv')[1]
    top_5_u2 = getTop5('a_movies.csv')[0]
    sub_u2 = getTop5('a_movies.csv')[1]


    exact_match = []

    # designate the shorter list to parse through if there is one
    if len(sub_u1) < len(sub_u2):
        shorter_list = sub_u1
        longer_list = sub_u2
    else:
        shorter_list = sub_u2
        longer_list = sub_u1
    i = 0
    while i < len(shorter_list) and len(exact_match) < 3:
        val = shorter_list[i]
        val_swapped_order = (val[1], val[0])
        # get matching subgenres
        # order of genre may be swapped
        # ex: comedy-horror v horror-comedy
        # so checking for those cases
        if val in longer_list or val_swapped_order in longer_list:
            if val in longer_list:
                longer_list.remove(val)
            elif val_swapped_order in longer_list:
                longer_list.remove(val_swapped_order)
            shorter_list.remove(val)
            exact_match.append('-'.join(val))
            # remove these genres from top 5 genres
            # so unique genres are remaining in each user's top genre list
            # for example, if we have a comedy-drama as a matching subdrama,
            # we don't necessarily want "comedy" and "drama" as further matches
            # which may be repetitive
            # this can be changed later tho
            if val[1] in top_5_u1:
                top_5_u1.remove(val[1])
            if val[0] in top_5_u1:
                top_5_u1.remove(val[0])
            if val[1] in top_5_u2:
                top_5_u2.remove(val[1])
            if val[0] in top_5_u2:
                top_5_u2.remove(val[0])
            i-=1
        i+=1

    # if less than 3 exact subgenre matches found
    # go back to top 5 genre list and extract commonalities
    if len(exact_match) < 3:
        # print("user 1 top5 after deletion"+str(top_5_u1))
        # print("user 2 top5 after deletion"+str(top_5_u2))
        print("exact match"+str(exact_match))
        # user 1 has more genres to look through
        if len(top_5_u1) > len(top_5_u2):
            # loop through shorter list to find matching genres
            for val in top_5_u2:
                if val in top_5_u1:
                    exact_match.append(val)
        else:
            for val in top_5_u1:
                if val in top_5_u2:
                    exact_match.append(val)
        if len(exact_match) > 3:
            fin = exact_match[0:3]
        else:
            fin = exact_match
        # shorter_list = [genre for t in shorter_list for genre in t]
        # longer_list = [genre for t in longer_list for genre in t]
        # shorter_list = [*set(shorter_list)]
        # longer_list = [*set(longer_list)]
        # print("longer list: "+str(longer_list))
        # print("shorter list: "+str(shorter_list))

        # for val in shorter_list:
        #     if val in longer_list:
        #         one_match.append(val)

        # more_needed = 3 - len(exact_match)
        # print("more needed:"+str(more_needed))
        # if len(one_match) >= more_needed:
        #     temp = one_match[0:more_needed]
        # else:
        #     temp = one_match
        # fin = np.concatenate((exact_match, temp))
    else:
        fin = exact_match[0:3]

    print("The top genres between you and you!"+ str(fin))

    # print out top 3 movie with relevant genres
    # THIS IS THE DATA WE SHOW TO THE USERS
    for val in fin:
        genres = val.split("-")
        getMovieAndPlots(genres, 5)
    

def getTopGenres(username):
    data = pd.read_csv('commonGenres.csv')
    # getting top 3 genres
    top_genres = data['genre'].head(3)
    topGenresList = top_genres.tolist()
    print(topGenresList)
    return topGenresList


def main():
    username = input("Enter your username: ")
    username2 = input("Enter the profile you want to mesh with: ")
    #TODO: Look up the user's username to find their profile and get their top genres
    # give links to the movies
    # the parameters of the getCommonTopGenres will be the specific profile,
    # which will then link to the movie/genre data
    # hard coded for now
    getCommonTopGenres("balh", ";bah")

    # additional movie print outs if the subgenres become repetitive
    print("just for funsies, we find movies with both you and your friend's top 2 genres")
    
    user1 = getTop5('o_movies.csv')[0]
    user2 = getTop5('a_movies.csv')[0]
    if len(user1) > 1:
        user1 = user1[0:2]
    if len(user2) > 1:
        user2 = user2[0:2]
    four_genres = np.concatenate((user1, user2))
    # get rid of possible top 2 duplicates within each person's top genres
    four_genres = [*set(four_genres)]
    getMovieAndPlots(four_genres, 5)

    # ANOUSHKA'S CODE THAT GIVES INDIVIDUAL TOP GENRES
    # print("Would you like to see your own top genres?")
    # print("\nMovie suggestions based on your top genres: ") 
    # topGenresList = getTopGenres(username)
    # for genre in topGenresList:
    #     getMoviesByGenre(genre, 3)


    while True:
        pref = input("\nWould rather have movie suggestions based on your preferences? Enter y/n:")
        if pref in ["y", "n"]:
            if pref in ["y"]:
                # if they dont want any of those movies:
                actor_name = getActorPref()
                # if they have an actor preference
                if actor_name is not None:
                    actorMoviesList = get_actor_movies(actor_name)
                    print(f"\nHere are movies {actor_name} is in:")
                    print(actorMoviesList)
                    break
                # if they don't have an actor preference
                else:
                    #TODO: currently just giving the top 5 movies in the genre they prefer. Need to add release year range and duration range
                    genre = getGenrePref()
                    releaseYearRange = getReleaseYearRange()
                    durationRange = getDurationRange()

                    genreMoviesList = getMoviesByGenre(genre, 5)
                    print(genreMoviesList)
                    break

                print("\nYour preferences: ")
                if actor_name:
                    print(f"Actor: {actor_name}")
                else:
                    print(f"Genre: {genre}")
                    print(f"Release Year Range: {releaseYearRange}")
                    print(f"Duration Range: {durationRange}")
            else:
                break
        else:
            print("Enter a valid response (y or n): ")


ia = IMDb()
main()