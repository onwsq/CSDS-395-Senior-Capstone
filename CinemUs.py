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
movie_genres = {}
parse_dates = ['Date']
data = pd.read_csv('NetflixViewingHistory.csv', parse_dates=parse_dates)
df = data.values
timestamp = pd.Timestamp(datetime(2021, 10, 10))
currentday = timestamp.today()
# print(df[0][1])
for i in df:
    if (currentday - i[1]).days < 90: 
        string = re.search('^([^:])+', i[0])
        if string[0] in movies.keys():
            movies[string[0]] = movies[string[0]]+1
        elif string[0] in shows.keys():
            shows[string[0]] = shows[string[0]]+1
        else:
            search = ia.search_movie(string[0])
            # print("search "+str(search)+"\n")
            if len(search) > 0:
                info = ia.get_movie(search[0].movieID)
                if info['kind'] == 'movie':
                    movies.update({string[0]:1})
                else:
                    shows.update({string[0]:1})
# only shows really need to be sorted by value
# becaue most people only watch movies once
print(sorted(shows))

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


