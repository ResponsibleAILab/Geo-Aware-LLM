import os
import json

from lib.util import load_tweets, save_file
from lib.twitter_api import api_get_tweets_for_ids

# assumes step 1_filter_geo_tweets has already been run
# use the saved csv file here
geo_tweets_file_name = 'data/london_tweets.csv'

# jsonl file to save api data to
save_api_data_file_name = 'data/london_api_data.jsonl'

# stop execution if the input file is not found
if not os.path.exists(geo_tweets_file_name):
    raise Exception(f'Geo tweets file does not exist at: {geo_tweets_file_name}')

# load data from csv
geo_ids = []
for tweet in load_tweets(geo_tweets_file_name):
    geo_ids.append(tweet.reply_to_tweet_id)

# load data from api
file_data = ''
for tweet in api_get_tweets_for_ids(geo_ids):
    file_data += json.dumps(tweet) + '\n'

# save data as jsonl
save_file(save_api_data_file_name, file_data)