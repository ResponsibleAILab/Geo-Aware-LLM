## Geo Aware LLM process
  
This repository is an example use case for *Data and Resources Paper: A Multi-granularity Decade-Long Geo-Tagged Twitter Dataset for Spatial Computing*. It shows the creation of a dataset for fine tuning an llm to simulate a reply to a tweet from a specific time and place. The `gpt.json` file in this repository can be used to interface the generated prompt and completion pairs with [text-generation-ui](https://github.com/oobabooga/text-generation-webui) in the `training/formats` folder.
  
### Abstract
The widespread use of social media platforms has led to the generation of a huge amount of geo-tagged information embedded within user-generated content. This data holds significant potential for location-aware applications and location-based services. However, the spatial computing community still lacks access to a comprehensive, large-scale social media dataset that spans extensive regions and encompasses multiple levels of location granularity over an extended period. In this research paper, we present a geo-tagged Twitter dataset comprising tweets from over 100 countries spanning a period of more than 10 years. The dataset includes four levels of location granularity: country, state/province, city, and neighboring regions. Additionally, we categorize locations into two types: user profile locations and tweet locations.  
  
### API Documentation
**Notes:**  
- This is the backend service for `https://sigspatial.yunhefeng.me/`.
- Functions for querying the paper's dataset and Twitters official API are included in this repository.  
- `lib/geo_api.py` contains `get_by_coordinates` function which uses the paper's dataset to retrieve tweet ids based on proximity to a given coordinate.  
- Dates are php formatted strings in the form of "yyyy-mm-dd".  
- If one or more of the dates are left empty, then it will be assumed to query all records regardless of time.  

#### Shared Parameters
All methods have these parameters and are optional.  
All methods use the GET http method.  

from_date: the start date for your query.  
to_date: the end date for your query.   
language: the language code to filter the tweets for, example: 'en'.

#### Query Coordinates
**url:** `https://sigspatial.yunhefeng.me/api/query_coordinates.php`  
**description:** Queries the dataset based on a distance to a given coordinate.  
**parameters:**  
distance: the distance from the given coordinate.  
latitude: the latitude of the given coordinate.  
longitude: the longitude of the given coordinate.  

#### Query Tweet Locations
**url:** `https://sigspatial.yunhefeng.me/api/query_tweet_location.php`  
**description:** Queries the dataset based on the user inputted tweet location  
**parameters:**  
region: The tweets location is assumed using named entity recognition, this also queries based on the user inputted text. If either string partially match the query string, the tweet is returned if all other query parameters also match.  
country: the country code for the tweet, ex: US.

#### Query User Location
**url:** `https://sigspatial.yunhefeng.me/api/query_user_location.php`  
**description:** Queries the dataset based on the user inputted location in their Twitter bio.  
**parameters:**  
city: assumed using named entity recognition matched to cities around the world.   
country: country code assumed using named entity recognition, ex: US.  