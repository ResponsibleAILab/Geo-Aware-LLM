
import re
from typing import List

def replace_regex_matches(pattern: re, replacement: str, text: str) -> str:
    return re.sub(pattern, replacement, text)

def find_api_tweet(id: int, tweets: List[dict]):
    for tweet in tweets:
        if tweet['id'] == id:
            return tweet
    return None

def create_completions(geo_tweets: List[dict], api_tweets: List[dict]) -> List[dict]:
    # string to help llm determine when to stop generating tokens
    end_token = '\n\n####\n\n'

    mention_pattern = r'@\w+'
    completions = []
    for tweet in geo_tweets:
        # get tweet the geo tweet responded to
        api_tweet = find_api_tweet(tweet['in_reply_to_user_id'], api_tweets)
        if api_tweet == None:
            continue

        # anonymize user data so llm doesn't write someones actual handle in simulated tweet
        prompt = replace_regex_matches(mention_pattern, '@user', api_tweet['text']) + end_token
        completion_text = replace_regex_matches(mention_pattern, '@user', tweet['text']) + end_token

        # OpenAI style completion format
        completions.append({
            'prompt': prompt,
            'completion': completion_text
        })
        
    return completions