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
data1 = pd.read_csv('o_movies.csv')
df1 = data1.values
data2 = pd.read_csv('a_movies.csv')
df2 = data2.values
exact_match = []
one_match = []
index = 0
min_list = 1


for i in df1:
    # only watched once
    if i[1] == 1:
        temp = i[2:]
        genres1 = np.concatenate((genres1, temp))
    cleaned_genres1 = [x for x in genres1 if str(x) != 'nan']


common_genres1 = [genre for genre, val in Counter(cleaned_genres1).most_common()]

if len(common_genres1) > 4:
    top_5_u1 = common_genres1[0:5]
else:
    top_5_u1 = common_genres1

res1 = [(a, b) for idx, a in enumerate(top_5_u1) for b in top_5_u1[idx + 1:]]

if len(res1) > 2:
    res1 = res1[0:3]
    print(res1[0:3])
else:
    index = len(res1)
    print(res1)


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


if index == 0:
    index = 3

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
    if val in longer_list or val_swapped_order in longer_list:
        if val in longer_list:
            longer_list.remove(val)
        elif val_swapped_order in longer_list:
            longer_list.remove(val_swapped_order)
        shorter_list.remove(val)
        exact_match.append('-'.join(val))
        i-=1
    i+=1


shorter_list = [genre for t in shorter_list for genre in t]
longer_list = [genre for t in longer_list for genre in t]
shorter_list = [*set(shorter_list)]
longer_list = [*set(longer_list)]
print("longer list: "+str(longer_list))
print("shorter list: "+str(shorter_list))

for val in shorter_list:
    if val in longer_list:
        one_match.append(val)


if len(exact_match) < 3:
    more_needed = 3 - len(exact_match)
    print("more needed:"+str(more_needed))
    if len(one_match) >= more_needed:
        temp = one_match[0:more_needed]
    else:
        temp = one_match
    fin = np.concatenate((exact_match, temp))
else:
    fin = exact_match

print(fin)
