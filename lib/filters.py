from datetime import date
from typing import List, Tuple

from lib.classes import Tweet
from lib.util import extract_groups, haversine

def filter_language(language: str, tweets: List[Tweet]) -> List[Tweet]:
    filtered = []
    for tweet in tweets:
        if tweet.lang != language:
            continue
        filtered.append(tweet)
    return filtered

def filter_locations(reference_point, tweets, distance):
    filtered = []
    for tweet in tweets:
        if tweet.location.has_data == False:
            continue
        location = tweet.location.coordinates
        for point in location:
            dist = haversine(reference_point, point)
            if dist <= distance:
                filtered.append(tweet)
                break
    return filtered

# center is in the form of (lat, lon)
def filter_location(center: Tuple[float, float], distance: int, tweets: List[Tweet]) -> List[Tweet]:
    return filter_locations(center, tweets, distance)

def filter_reply(is_reply: bool, tweets: List[Tweet]) -> List[Tweet]:
    filtered = []
    for tweet in tweets:
        if (tweet.reply_to_tweet_id != None and tweet.reply_to_tweet_id != 'None') == is_reply:
            filtered.append(tweet)
    return filtered

def filter_date(start_date: date, end_date: date, tweets: List[Tweet]) -> List[Tweet]:
    # string form of python date object
    regex_pattern = r"[A-Z][a-z]{2} [A-Z][a-z]{2} (\d{2}) \d\d:\d\d:\d\d \+0000 \d\d\d\d"

    filtered = []
    for tweet in tweets:
        [day] = extract_groups(tweet.time, regex_pattern)
        tweet_date = date.fromisoformat(f'2020-03-{day}')
        if tweet_date > end_date or tweet_date < start_date:
            continue
        filtered.append(tweet)
    return filtered

def filter_geo_tweets(
        location: Tuple[float, float], 
        distance: int,
        start_date: date,
        end_date: date,
        language: str,
        tweets: List[Tweet]
    ):
    geo_tweets = filter_reply(True, tweets)
    print(f'Found {len(geo_tweets)} replies')
    geo_tweets = filter_language(language, geo_tweets)
    print(f'Filtered to {len(geo_tweets)} tweets for specified language')
    geo_tweets = filter_location(location, distance, geo_tweets)
    print(f'Filtered to {len(geo_tweets)} tweets in specified location')
    geo_tweets = filter_date(start_date, end_date, geo_tweets)
    print(f'Filtered to {len(geo_tweets)} tweets for specified date')
    return geo_tweets