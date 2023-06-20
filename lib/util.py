import math
import re
from typing import List, Tuple, Callable
from lib.classes import Tweet
from joblib import Parallel, delayed

def open_file(filepath: str) -> str:
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()

def save_file(filepath: str, content: str):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)

def load_tweets(file_name: str = 'data/filtered_tweets.csv') -> List[Tweet]:
    print(f'Loading tweets from: {file_name}')
    with open(file_name, 'r', encoding='utf-8') as f:
        tweets = []
        for line in f.read().split('\n'):
            tweet = Tweet(line.strip())
            if not tweet.loaded:
                continue
            tweets.append(tweet)
        print(f'Loaded {len(tweets)} tweets')
        return tweets
    
def save_tweets(file_name: str, tweets: List[Tweet]):
    print(f'Saving {len(tweets)} tweets to {file_name}')
    saved_tweets = 0
    with open(file_name, 'w', encoding='utf-8') as f:
        for tweet in tweets:
            try:
                f.write(tweet.to_csv() + '\n')
                saved_tweets += 1
            except:
                continue
    print(f'Saved {saved_tweets} tweets')

def extract_groups(input_string: str, regex_pattern: re) -> List[str]:
    pattern = re.compile(regex_pattern)
    match = re.search(pattern, input_string)
    if match:
        groups = match.groups()
        return groups
    else:
        return None

def batchify(list: List[any], num_batches: int) -> List[List[any]]:
    batch_len = len(list) // num_batches
    batches = []
    current_batch = []
    for i in list:
        current_batch.append(i)
        if len(current_batch) >= batch_len:
            batches.append(current_batch)
            current_batch = []
    return batches

def flatten(stacked_list: List[List[any]]) -> List[any]:
    flattened_list = []
    for batch in stacked_list:
        for i in batch:
            flattened_list.append(i)
    return flattened_list

# function must be in the form of fn(thread_idx, batch, all_items)
def parallelize(fn: Callable[[int, List[any], List[any]], List[any]], num_threads: int, list: List[any]) -> List[any]:
    batches = batchify(list, num_threads)
    ret_batches = Parallel(n_jobs=num_threads)(
        delayed(fn)(idx, batch, list) for (batch, idx) in zip(batches, range(0, num_threads))
    )
    return flatten(ret_batches)

# Haversine formula
def haversine(coord1: Tuple[float, float], coord2: Tuple[float, float]) -> float:
    R = 6371  # radius of Earth in kilometers
    lat1, lon1 = coord1
    lat2, lon2 = coord2

    phi1, phi2 = math.radians(lat1), math.radians(lat2) 
    dphi       = math.radians(lat2 - lat1)
    dlambda    = math.radians(lon2 - lon1)

    a = math.sin(dphi/2)**2 + \
        math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2

    return 2*R*math.atan2(math.sqrt(a), math.sqrt(1 - a))