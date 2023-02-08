import csv
import numpy as np
import pandas as pd
import imdb
import requests
import re
from datetime import date
from datetime import datetime


ia = imdb.IMDb()
movies = {}
shows = {}
movies_val = 0
shows_val = 0
movie_genres = {}
parse_dates = ['Date']
data = pd.read_csv('NetflixViewingHistory.csv', parse_dates=parse_dates)
df = data.values
timestamp = pd.Timestamp(datetime(2021, 10, 10))
currentday = timestamp.today()

# print(df[0][1])
#Avatar: the last airbender :
for i in df:
    if (currentday - i[1]).days < 90: 
        shows_keywords = False
        string = re.search('^([^:])+', i[0])
        if i[0].count(":") > 1:
            shows_keywords = True
        if string[0] in movies.keys() or string[0] in shows.keys():
            # already exists
            if string[0] in movies.keys():
                movies[string[0]] = movies[string[0]]+1
                movies_val += 1
            elif string[0] in shows.keys():
                shows[string[0]] = shows[string[0]]+1
                shows_val +=1
        else:
            # probably a tv show, with more than 1 colon in title
            if shows_keywords == True:
                shows.update({string[0]:1})
                shows_val += 1
            # need to verify is tv show or movie
            # ex: Heartstopper: episodename
            else:
                if ":" not in i[0]:
                    movies.update({i[0]:1})
                    movies_val += 1
                else:
                    search = ia.search_movie(i[0])
                    if len(search) > 0:
                        print("have to search for: "+str(i[0]))
                        info = ia.get_movie(search[0].movieID)
                        if info['kind'] != 'movie':
                            shows.update({string[0]:1})
                            shows_val += 1
                            # print(shows)
                        else:
                            movies.update({i[0]:1})
                            movies_val += 1
                            # print(movies)


print(type(movies))
print(movies)
print(shows)
field_names = ['Title', 'Occurrences']


pd.DataFrame.from_dict(data=movies, orient='index').to_csv('Names.csv')

# print("movies_val: "+str(movies_val))
# for val in movies:
#     info = ia.get_movie(movies[val])
#     print(val)
        # else:
        #     search = ia.search_movie(string[0])
        #     # print("search "+str(search)+"\n")
        #     if len(search) > 0:
        #         info = ia.get_movie(search[0].movieID)
        #         if info['kind'] == 'movie':
        #             movies.update({string[0]:1})
        #         else:
        #             shows.update({string[0]:1})
# only shows really need to be sorted by value
# becaue most people only watch movies once
# print(sorted(shows))
# print(sorted(movies))

    # showormovie = title['kind']
    # print(showormovie)
    # search = ia.search_movie(i[0])
    # # need to account for cases where IMDB can't find title
    # if len(search) > 0 :
    #     print("search "+str(search)+"\n")
    #     details = search[0].movieID
    #     series = ia.get_movie(details)
    #     genre = series.data['genres']
    #     print("genre "+str(genre)+"\n")


