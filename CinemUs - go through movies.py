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

top_5 = common_genres[0:5]
print(top_5)

res = [(a, b) for idx, a in enumerate(top_5) for b in top_5[idx + 1:]]
print(res[0:3])



