import tweepy
import os
import json
from time import sleep
from typing import List

def handle_errors(errors: List[dict]) -> List[int]:
    print('\n\nERRORS')
    not_found = 0
    auth_errors = 0
    suspended = 0
    for error in errors:
        if error['title'] == 'Not Found Error':
            not_found += 1
            continue
        if error['title'] == 'Authorization Error':
            auth_errors += 1
            continue
        if error['title'] == 'Forbidden':
            suspended += 1
            continue
        print(error['title'])
        print(error['detail'])
    if not_found > 0:
        print(f'Could not find {not_found} tweets')
    if auth_errors > 0:
        print(f'Unauthorized access for {auth_errors} tweets')
    if suspended > 0:
        print(f'{suspended} users were suspended')
    return [not_found, auth_errors, suspended]

def ref_to_json(referenced_tweets: List[any] | None) -> List[dict]:
        ret_data = []
        if referenced_tweets == None:
            return []
        for tweet in referenced_tweets:
            ret_data.append({
                'type': tweet.type,
                'id': tweet.id
            })
        return ret_data

def get_tweet_dict(api_tweet: tweepy.Tweet) -> dict:
    return {
        'id': api_tweet.id,
        'author_id': api_tweet.author_id,
        'lang': api_tweet.lang,
        'text': api_tweet.text, 
        'created_at': str(api_tweet.created_at),
        'conversation_id': api_tweet.conversation_id,
        'in_reply_to_user_id': api_tweet.in_reply_to_user_id,
        'referenced_tweets': ref_to_json(api_tweet.referenced_tweets)
    }

def get_tweets(client: tweepy.Client, ids: List[int]) -> List[any]:
    ret_not_found = 0
    ret_auth_errors = 0
    ret_suspended_errors = 0
    res = client.get_tweets(
        ids=ids, 
        tweet_fields=['id', 'author_id', 'lang', 'text', 'created_at', 'conversation_id', 'referenced_tweets'],
        expansions=['author_id', 'referenced_tweets.id', 'in_reply_to_user_id', 'referenced_tweets.id.author_id']
    )
    if res.errors != None and len(res.errors) > 0:
        [not_found, auth_errors, suspended_errors] = handle_errors(res.errors)
        ret_not_found = not_found
        ret_auth_errors = auth_errors
        ret_suspended_errors = suspended_errors
    return [res.data, ret_not_found, ret_auth_errors, ret_suspended_errors]

def api_get_tweets_from_ids(ids: List[int]) -> List[dict]:
    if not os.path.exists('twitter_key.txt'):
        raise "Twitter bearer token file not found: twitter_key.txt, please create file and place bearer token inside it"

    key = ''
    with open('twitter_key.txt', 'r') as f:
        key = f.read()

    client = tweepy.Client(bearer_token=key)

    batches = []
    current_batch = []
    idx = 0
    # Can look up a maximum of 100 ids per api request
    for id in ids:
        if idx % 100 == 0 and idx != 0:
            id_str = ''
            for id in current_batch:
                id_str += str(id) + ','
            batches.append(id_str[:len(id_str) - 1])
            current_batch = []
        current_batch.append(id)
        idx += 1
    if len(ids) % 100 != 0:
        batches.append(current_batch)

    tweets = []
    bad_batches = []
    idx = 0
    total_not_found = 0
    total_auth_errors = 0
    total_suspended = 0
    for batch in batches:
        # Rate limit API calls
        sleep(5)

        idx += 1
        print(f'\n\nGetting batch {idx} of {len(batches)}')
        try:
            [tweet_batch, not_found, auth_errors, suspended_errors] = get_tweets(client, batch)
            total_not_found += not_found
            total_auth_errors += auth_errors
            total_suspended += suspended_errors
            print(f'Found {len(tweet_batch)} tweets, recieved {not_found + auth_errors + suspended_errors} errors')
        except Exception as e:
            print('Error getting batch')
            print(e)
            bad_batches.append(idx)
            continue
        print(f'Batch retrieved successfully')
        for tweet in tweet_batch:
            tweets.append(get_tweet_dict(tweet))

    print(f'\n\nProcess complete:')
    print(f'Could not find {total_not_found} tweets')
    print(f'Unauthorized access for {total_auth_errors} tweets')
    print(f'Tried to access {total_suspended} suspended users')
    print(f'{total_not_found + total_auth_errors + total_suspended} total errors')
    print(f'Found {len(tweets)} tweets successfuly')

    if len(bad_batches) > 0:
        print(f'Writting bad batch indexes to: data/twitter_api_bad_batches.json')
        with open('data/twitter_api_bad_batches.json', 'w') as f:
            f.write(json.dumps(bad_batches))
    return tweets