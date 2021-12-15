from flask import Flask, render_template
from requests.api import get
from app.models import DB, User, Tweet
from app.twitter import get_user_and_tweets

# Create a factory for serving app when launched
def create_app():

    # initializes our Flask app
    app = Flask(__name__)

    # Configuration
    app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

    # Connect our database to our app object
    DB.init_app(app)

    # Make our "Home" or "root" route
    @app.route("/")
    def root():
        users = User.query.all()
        # Do this when visiting home page
        return render_template('base.html', users=users)

    @app.route("/update")
    def update():
        users = User.query.all()
        usernames = [user.username for user in users]
        for username in usernames:
            get_user_and_tweets(username)
        return "updated"
    

    @app.route("/populate")
    def populate():
        get_user_and_tweets('ryanallred')
        get_user_and_tweets('nasa')
        # ryan = User(id=1, username='ryanallred')
        # julian = User(id=2, username='julian')
        # # Add user to database
        # DB.session.add(ryan)
        # DB.session.add(julian)
        # tweet1 = Tweet(id=1, text='some tweet text', user=ryan, vect=[1,2,3], user_id=1)
        # tweet2 = Tweet(id=2, text='some OTHER tweet text', user=julian, vect=[1,2,3], user_id=2)
        # # Add the tweets
        # DB.session.add(tweet1)
        # DB.session.add(tweet2)
        # DB.session.commit()
        return "Created some users"
    
    @app.route("/reset")
    def test():
        # create a user in the DB
        # removes everything from the DB
        DB.drop_all()
        # creates a new DB with indicated tables
        DB.create_all()

        return "reset database"



    return app
