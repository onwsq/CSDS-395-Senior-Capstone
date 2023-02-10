import csv
import numpy as np
import pandas as pd
import imdb
import requests
import re
from datetime import date
from datetime import datetime
from collections import Counter


ia = imdb.IMDb()
genres = []
shows = {}
total_genres = 0
data = pd.read_csv('movies.csv')
df = data.values

print(df)

for i in df:
    # only watched once
    if i[1] == 1:
        temp = i[2:]
        genres = np.concatenate((genres, temp))
    cleaned_genres = [x for x in genres if str(x) != 'nan']
print(cleaned_genres)
print(len(cleaned_genres))

common_genres = [genre for genre, val in Counter(cleaned_genres).most_common()]
print(common_genres)

# print(df[0][1])
#Avatar: the last airbender :
# for i in df:
#     # for the last 3 months
#     if (currentday - i[1]).days < 90: 
#         shows_keywords = False
#         string = re.search('^([^:])+', i[0])
#         # if there's more than 1 colon it's prob a tv show
#         if i[0].count(":") > 1:
#             shows_keywords = True
#         # if it's already in our list
#         if string[0] in movies.keys() or string[0] in shows.keys():
#             # already exists
#             if string[0] in movies.keys():
#                 movies[string[0]] = movies[string[0]]+1
#                 movies_val += 1
#             elif string[0] in shows.keys():
#                 shows[string[0]] = shows[string[0]]+1
#                 shows_val +=1
#         # otherwise need to check if new entry of tv show/movie
#         else:
#             # probably a tv show
#             if shows_keywords == True:
#                 shows.update({string[0]:1})
#                 shows_val += 1
#             # need to verify is tv show or movie
#             # ex: Heartstopper: episodename
#             else:
#                 # if there's no colon then def a movie
#                 if ":" not in i[0]:
#                     movies.update({i[0]:1})
#                     movies_val += 1
#                 else:
#                     # search for title
#                     search = ia.search_movie(i[0])
#                     if len(search) > 0:
#                         print("have to search for: "+str(i[0]))
#                         # get info of the movie
#                         info = ia.get_movie(search[0].movieID)
#                         if info['kind'] != 'movie':
#                             shows.update({string[0]:1})
#                             shows_val += 1
#                             # print(shows)
#                         else:
#                             movies.update({i[0]:1})
#                             movies_val += 1
#                             # print(movies)


# print(type(movies))
# print(movies)
# print(shows)
# field_names = ['Title', 'Occurrences']


# pd.DataFrame.from_dict(data=movies, orient='index', columns=['Occurrences']).to_csv('movies.csv', header=True)
# pd.DataFrame.from_dict(data=shows, orient='index', columns=['Occurrences']).to_csv('shows.csv', header=True)

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


