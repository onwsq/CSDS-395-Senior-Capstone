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
top_genres = ['Comedy-Drama', 'Romance']

top250 = ia.get_top250_moves()

i = 0
