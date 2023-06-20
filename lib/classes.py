import re
import json

class Location:
    def __init__(self, data):
        items = data.split('|')
        if len(items) > 5:
            self.has_data = False
            return
        self.has_data = True
        self.country = items[0]
        self.name = items[1]
        self.city_state = items[2]
        self.coord_type = items[3]
        self.coordinates = []
        coords = json.loads(items[4])
        if isinstance(coords, list):
            for item in coords:
                self.coordinates.append((float(item[0]), float(item[1])))

def maybe_get_property(obj: dict, prop: str) -> any:
    if prop not in obj:
        return None
    return obj[prop]

def get_tweet_text(obj: dict) -> str:
    # get tweet text
    if ('extended_tweet' in obj):
        if ('full_text' in obj['extended_tweet']):
            tweet_text = obj['extended_tweet']['full_text']
            tweet_text = re.sub(r'\n', ' ', tweet_text)
            tweet_text = re.sub(r'\r', ' ', tweet_text)
        else:
            if ('text' in obj):
                tweet_text = obj['text']
                tweet_text = re.sub(r'\n', ' ', tweet_text)
                tweet_text = re.sub(r'\r', ' ', tweet_text)
            else:
                tweet_text = 'None'
    elif ('text' in obj):
        tweet_text = obj['text']
        tweet_text = re.sub(r'\n', ' ', tweet_text)
        tweet_text = re.sub(r'\r', ' ', tweet_text)
    else:
        tweet_text = 'None'

    return tweet_text

class Tweet:
    def __init__(self, line: str):
        data = line.split('|@|||$|')
        self.loaded = False
        if len(data) < 15:
            return
        self.loaded = True
        self.time = data[0]
        self.tweet_id = int(data[1])
        self.text = data[2]
        self.lang = data[3]
        self.geo = data[4]
        self.coordinates = data[5]
        self.place = data[6]
        self.user_id = int(data[7])
        self.user_location = data[8]
        self.location = Location(self.place)
        self.verified = data[9]
        self.geo_enabled = data[10]
        self.utc_offset = data[11]
        self.flag_retweet = data[12]
        self.flag_quote = data[13]
        reply_id = data[14]
        if reply_id != 'None':
            self.reply_to_tweet_id = int(data[14])
        else:
            self.reply_to_tweet_id = None
        self.replies = []

    def to_csv(self):
        return '|@|||$|'.join([self.time, str(self.tweet_id), self.text, self.lang, self.geo, self.coordinates, self.place, str(self.user_id), self.user_location, \
                self.verified, self.geo_enabled, self.utc_offset, self.flag_retweet, self.flag_quote, str(self.reply_to_tweet_id)])