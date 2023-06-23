import json
from datetime import date

from lib.geo_api import get_by_coordinates
from lib.util import save_file, save_jsonl_file
from lib.twitter_api import api_get_tweets_from_ids
from lib.completions import create_completions

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
start_date = date.fromisoformat('2020-01-01')
end_date = date.fromisoformat('2021-01-01')

# files for tweets from dataset api
geo_ids_file = 'data/london_geo_tweet_ids.json'
geo_tweets_file = 'data/london_geo_tweets.jsonl'

# files for original tweets
original_tweet_ids_file = 'data/london_original_tweet_ids.json'
original_tweets_file = 'data/london_original_tweets.jsonl'

# use json instead of jsonl to increase compatability with fine tuning tools
completions_file = 'data/london_tweet_completions.json'

# Get tweet ids from geo api
print('Fetching ids from geo dataset')
geo_ids = get_by_coordinates(location, distance, start_date, end_date, language)
save_file(geo_ids_file, json.dumps(geo_ids))

print(f'Geo api returned {len(geo_ids)} tweet ids')
geo_tweets = api_get_tweets_from_ids(geo_ids)
save_jsonl_file(geo_tweets_file, geo_tweets)

original_ids = []
for tweet in geo_tweets:
    # creates a larger dataset if searching for replies here instead of original posts
    if tweet['in_reply_to_user_id'] == None:
        continue
    original_ids.append(tweet['in_reply_to_user_id'])
print(f'Filtered to {len(original_ids)} replies')
save_file(original_tweet_ids_file, json.dumps(original_ids))

original_tweets = api_get_tweets_from_ids(original_ids)
save_jsonl_file(original_tweets_file, original_tweets)

print('Creating completions')
completions = create_completions(geo_tweets, original_tweets)
save_file(completions_file, json.dumps(completions))
print(f'Wrote {len(completions)} completions to file')