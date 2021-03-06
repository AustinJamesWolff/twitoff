from numpy import vectorize
import requests
import ast
import spacy

# Local import
from app.models import DB, User, Tweet

# Add a new user if they don't already exist
# If they already exist just grab their most recent tweets
def get_user_and_tweets(username):
# The link at which we will be making calls
    HEROKU_URL = 'https://lambda-ds-twit-assist.herokuapp.com/user/'

    # Use the `literal_eval` method to turn the JSON response into a Python dictionary
    user = ast.literal_eval(requests.get(HEROKU_URL + username).text)
    # print(user)

    nlp = spacy.load('my_model')
    # nlp = spacy.load('src/my_nlp_model')

    try:

        # If the user already exists, create a variable of their record from the database
        if User.query.get(user['twitter_handle']['id']):
            db_user = User.query.get(user['twitter_handle']['id'])
        else:
            # Otherwise, create a new instance and add it to the database
            db_user = User(id=user['twitter_handle']['id'],
                           username=user['twitter_handle']['username'])
            DB.session.add(db_user)
    


        # If we don't add any tweets this session, we will make a note of it
        tweets_added = 0

        for tweet in user['tweets']:

            # If the tweet id exists in the database we will go against the non-unique constraint so,
            # this line of code will break the loop meaning we already obtained the other tweets
            if Tweet.query.get(tweet['id']):
                break
            else:
                tweet_text = tweet['full_text']
                # tweet_vector = vectorize(tweet['full_text'])

                # Otherwise, add a new Tweet record
                db_tweet = Tweet(id=tweet['id'], text=tweet_text, 
                embeddings=nlp(tweet_text).vector
                )

                # Append it to the User instance
                db_user.tweets.append(db_tweet)

                # Add it to the database session
                DB.session.add(db_tweet)

                # Incrementing to let us know how many tweets we added
                tweets_added += 1

    # If ANYTHING in our try statement fails, we will raise the error here
    except Exception as e:
        raise e

    DB.session.commit()


    return tweets_added

nlp = spacy.load('my_model')
def vectorize_tweet(tweet_text):
    # return the word embedding for a given string of text
    return nlp(tweet_text).vector

