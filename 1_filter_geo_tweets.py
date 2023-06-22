import os
from datetime import date

from lib.filters import filter_geo_tweets
from lib.util import load_tweets, save_tweets

# Dallas, TX, US
# location = (32.782893, -96.799738)
# distance = 150 # in km from location

# New York, NY, US
# location = (40.785303, -73.963272)
# distance = 100

# London, UK
# location = (51.510422, -0.124413)
# distance = 100

# location: In the form of (lat, lon)
# distance: in km from location
location = (51.510422, -0.124413)
distance = 100

language = 'en'
start_date = date.fromisoformat('2020-03-13')
end_date = date.fromisoformat('2020-03-17')

# input file, ensure the csv data is for the date range you want
geo_tweets_file = 'data/geo_tweets.csv'

# output file
save_file_name = 'data/london_tweets.csv'

if os.path.exists(geo_tweets_file):
    raise Exception(f'Input file not found at: {geo_tweets_file}')

tweets = load_tweets(geo_tweets_file)

geo_tweets = filter_geo_tweets(location, distance, start_date, end_date, language, tweets)

save_tweets(save_file_name, geo_tweets)