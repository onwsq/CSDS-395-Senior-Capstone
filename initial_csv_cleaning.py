import csv
import numpy as np
import pandas as pd
import imdb
import requests
import re
from datetime import date
from datetime import datetime
import time

ia = imdb.IMDb()
movies = {}
shows = {}
movies_val = 0
shows_val = 0
shows_first_bit = []
movie_genres = {}
parse_dates = ['Date']
#### THIS IS THE CSV THAT IS BEING READ FOR THE PROFILE ####
data = pd.read_csv('OliviaNetflixViewingHistory.csv', parse_dates=parse_dates)
df = data.values
timestamp = pd.Timestamp(datetime(2021, 10, 10))
currentday = timestamp.today()
total_runtime = 0


# going through all entries within csv
for i in df:
    # for the last 3 months
    # THIS VALUE WE NEED TO FINALIZE
    if (currentday - i[1]).days < 150: 
        shows_keywords = False
        # if there's more than 1 colon it's prob a tv show
        if i[0].count(":") > 1:
            # get rid of everything except first colon
            second_index = i[0].index(":", i[0].index(":")+ 1)
            if second_index != -1:
                updated_str = i[0][0:second_index]
            else:
                updated_str = i[0] 
            shows_keywords = True
        else:
            updated_str = i[0]
        # now everything only has 1 colon max
        # what we care about rn
        # clean to see if tv shows/movies need to be shortened
        # if there are digits
        temp = updated_str.partition(':')[0]
        if bool(re.search(r'\d', str(updated_str))) == True:
            shows_keywords = True
            updated_str = temp
        else:
            # remove colon in case show: ep doesn't have a number in ep title
            show_ep_no_number = temp
        
        # if it's already in our list
        if updated_str in movies.keys():
            movies[updated_str][0] = movies[updated_str][0]+1
            movies_val += 1
        elif updated_str in shows.keys() or temp in shows_first_bit:
            if temp in shows_first_bit:
                shows[temp][0] = shows[temp][0]+1
                shows_val += 1
            else:
                shows[updated_str][0] = shows[updated_str][0]+1
                shows_val += 1
        else:
            print(updated_str)
            if shows_keywords == True:
                shows.update({updated_str:[1]})
                shows_val += 1
            else:
                search = ia.search_movie(updated_str)
                # found a match
                if len(search) > 0:
                    print("doing search: "+str(updated_str))
                    start = time.time()
                    info = ia.get_movie(search[0].movieID)
                    if info['kind'] == 'movie':
                        genres = info.data['genres']
                        genres.insert(0, 1)
                        if len(genres) > 0:
                            movies.update({updated_str:genres})
                    end = time.time()
                    print("runtime to do search: "+str(end-start))
                    total_runtime += end-start
                else:
                    # assume it's a movie if w/ colon has no results
                    shows.update({temp:[1]})
                    shows_first_bit.append(temp)
    


print(total_runtime)
# CREATING A NEW CSV WITH RELEVANT MOVIE DATA
# PARAMETER AFTER to_csv IS THE CSV TITLE, PROBABLY HAVE TO MAKE THAT VARIABLE
# ((RN '0_movies.csv' IS JUST HARD CODED))
# SEND THIS TO A DATA BUCKET TO STORE INFO??
# NEED TO ADD TO THIS DATA BUCKET WHEN USERS CHOOSE A MOVIE
pd.DataFrame.from_dict(data=movies, orient='index').to_csv('0_movies.csv', header=True)
# CREATING DATA BUCKET FOR SHOWS
# COMMENTED OUT RN BC NOT RELEVANT
pd.DataFrame.from_dict(data=shows, orient='index', columns=['Occurrences']).to_csv('shows.csv', header=True)


