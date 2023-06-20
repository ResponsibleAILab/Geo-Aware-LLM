import os
import json

from lib.util import load_tweets, open_file
from lib.completions import create_completions

# filtered set of tweets for location from step 1_filter_geo_tweets.py
geo_tweets_file_name = 'data/london_tweets.csv'

# data returned from api in step 2_get_tweets_from_api.py
api_original_file_name = 'data/london_api_data.jsonl'

# file name to save to, using json instead of jsonl because more fine tuning processes use that format
completion_file_name = 'data/london_completions.json'

if os.path.exists(geo_tweets_file_name):
    raise Exception(f'Geo tweets input file not found at: {geo_tweets_file_name}')

if os.path.exists(api_original_file_name):
    raise Exception(f'API tweets input file not found at: {api_original_file_name}')

# load csv file
geo_tweets = load_tweets(geo_tweets_file_name)

# load api data from jsonl file
api_tweets = []
api_loaded = 0
for line in open_file(api_original_file_name).split('\n'):
    try:
        api_tweets.append(json.loads(line))
    except:
        continue

print(f'Loaded {len(api_tweets)} api tweets')

completions = create_completions(geo_tweets, api_tweets)
with open(completion_file_name, 'w') as f:
    f.write(json.dumps(completions))

print(f'Wrote {len(completions)} completions to file')