from flask import Flask, render_template, request
from requests.api import get
from app.models import DB, User, Tweet
from app.twitter import get_user_and_tweets
from os import getenv
from .predict import predict_user

# Create a factory for serving app when launched
def create_app():

    # initializes our Flask app
    app = Flask(__name__)

    # Configuration
    app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URI')

    # Connect our database to our app object
    DB.init_app(app)

    # Make our "Home" or "root" route
    @app.route("/")
    def root():
        # Do this when visiting home page
        return render_template('base.html', title='Home', users=User.query.all())

    # Update users with their latest tweets
    @app.route("/update")
    def update():
        users = User.query.all()
        usernames = [user.username for user in users]
        for username in usernames:
            get_user_and_tweets(username)
        return "All users have been updated to include their latest tweets."

    
    @app.route("/reset")
    def test():
        # create a user in the DB
        # removes everything from the DB
        DB.drop_all()
        # creates a new DB with indicated tables
        DB.create_all()

        return render_template('base.html', title="Reset Database")

    # This route is NOT just displaying info
    # This route will change the database
    @app.route('/user', methods=['POST'])
    @app.route('/user/<name>', methods=['GET'])
    def user(name=None, message=''):
        # grab the username the user has input into the input box
        name = name or request.values['user_name']
        try:
            if request.method == 'POST':
                get_user_and_tweets(name)
                message = f'User "{name}" was successfully added.'
            tweets = User.query.filter(User.username == name).one().tweets
        except Exception as e:
            message = f'Error adding {name}: {e}'
            tweets = []
        else:
            return render_template('user.html', title=name, tweets=tweets, message=message)

    @app.route('/compare', methods=['POST'])
    def compare():
        user0, user1 = sorted([request.values['user0'], request.values['user1']])

        if user0 == user1:
            message = 'Cannot compare a user to themselves.'
        else:
            tweet_text = request.values['tweet_text']
            prediction = predict_user(user0, user1, tweet_text)
            message = '''"{}" is more likely to be said by {} than {}.'''.format(
                tweet_text, 
                user1 if prediction else user0, 
                user0 if prediction else user1)
        return render_template('prediction.html', title='Prediction', message=message)
        
    return app
