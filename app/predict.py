import numpy as np
from sklearn.linear_model import LogisticRegression
from .models import User
from .twitter import vectorize_tweet

def predict_user(user0_username, user1_username, hypo_tweet_text):

    # Query datavase for our two users
    user0 = User.query.filter(User.username == user0_username).one()
    user1 = User.query.filter(User.username == user1_username).one()

    # Get a numpy array of word embeddings for each user's tweets
    user0_vect = np.array([tweet.embeddings for tweet in user0.tweets])
    user1_vect = np.array([tweet.embeddings for tweet in user1.tweets])
    
    # combine user's tweet's word embeddings to one big NP array
    # Use vstack to concat 2-D np arrays
    # Here is the X matrix
    vects = np.vstack([user0_vect, user1_vect])

    # use np.concatenate() to concat 1-D np Array
    zeroes = np.zeros(len(user0.tweets))
    ones = np.ones(len(user1.tweets))
    # Here is the y vector
    labels = np.concatenate([zeroes, ones])

    # Train our Logistic Regression
    # instantiate the class
    log_reg = LogisticRegression()
    # Fit the model
    log_reg.fit(vects, labels)

    # Generate a prediction for our hypothetical tweet
    # Vectorize hypothetical tweet text and make it 2D,
    # hence the extra square brackets
    hypo_tweet_vect = [vectorize_tweet(hypo_tweet_text)]

    prediction = log_reg.predict(hypo_tweet_vect)
    # print(prediction)

    if prediction[0] == 1.0:
        return user0_username
    else:
        return user1_username

    # return prediction[0]

# print(predict_user('ryanallred','nasa','student python school'))