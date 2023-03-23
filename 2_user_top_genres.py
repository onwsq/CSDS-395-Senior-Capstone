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
genres1 = []
genres2 = []
# DATA 1 IS USER 1 INFO
# THIS DATA IS READING CSV CREATED FORM "initial_csv_cleaning.py"
# BUT WILL PROB BE A DATA BUCKET LATER ON
data1 = pd.read_csv('o_movies.csv')
df1 = data1.values
# DATA 2 IS USER 2 INFO
data2 = pd.read_csv('a_movies.csv')
df2 = data2.values
exact_match = []
one_match = []
genres_in_exact_match = []
index = 0
min_list = 1



for i in df1:
    # only watched once
    if i[1] == 1:
        temp = i[2:]
        genres1 = np.concatenate((genres1, temp))
    cleaned_genres1 = [x for x in genres1 if str(x) != 'nan']

# list of most common genres for user 1
common_genres1 = [genre for genre, val in Counter(cleaned_genres1).most_common()]

if len(common_genres1) > 4:
    top_5_u1 = common_genres1[0:5]
else:
    top_5_u1 = common_genres1

# list of top sub-genres off of top genres
res1 = [(a, b) for idx, a in enumerate(top_5_u1) for b in top_5_u1[idx + 1:]]

# get top 3 subgenres or however many available
if len(res1) > 2:
    res1 = res1[0:3]
    print(res1[0:3])
else:
    index = len(res1)
    print(res1)



## repeat functions for user 2
for i in df2:
    # only watched once
    if i[1] == 1:
        temp = i[2:]
        genres2 = np.concatenate((genres2, temp))
    cleaned_genres2 = [x for x in genres2 if str(x) != 'nan']


common_genres2 = [genre for genre, val in Counter(cleaned_genres2).most_common()]

if len(common_genres2) > 4:
    top_5_u2 = common_genres2[0:5]
else:
    top_5_u2 = common_genres2

res2 = [(a, b) for idx, a in enumerate(top_5_u2) for b in top_5_u2[idx + 1:]]

if len(res2) > 2:
    res2 = res2[0:3]
    print(res2[0:3])
else:
    if len(res2) < index:
        min_list = 2
        index = len(res2)
    print(res2)



#res1 and res2 are list of top 3 subgenres for each user
#top_5_u[x] is list of top genres
if index == 0:
    index = 3

# designate the shorter list to parse through if there is one
if min_list == 1:
    shorter_list = res1
    longer_list = res2
else:
    shorter_list = res2
    longer_list = res2
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
        top_5_u1.remove(val[1])
        top_5_u1.remove(val[0])
        top_5_u2.remove(val[1])
        top_5_u2.remove(val[0])
        i-=1
    i+=1

# if less than 3 exact subgenre matches found
# go back to top 5 genre list and extract commonalities
if len(exact_match) < 3:
    print("user 1 top5"+str(top_5_u1))
    print("user 2 top5"+str(top_5_u2))
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

print(fin)

# FIN IS LIST OF SUBGENRES/GENRES DEPENDING ON COMMONALITIES
# NOW NEED TO PROVIDE LIST OF MOVIES
