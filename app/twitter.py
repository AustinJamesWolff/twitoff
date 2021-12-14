from os import getenv
import tweepy

# Get our API keys
key = getenv("TWITTER_API_KEY")
secret = getenv("TWITTER_API_KEY_SECRET")

# Connect to the twitter API
TWITTER_AUTH = tweepy.OAuthHandler(key, secret)
TWITTER = tweepy.API(TWITTER_AUTH)

# Add a new user if they don't already exist
# If they already exist just grab their most recent tweets

def add_or_update_user(username):
    """Takes username (twitter handle)and pulls user tweet"""
    
