from flask import Flask, render_template
from .models import DB, User, Tweet

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
    
    @app.route("/test")
    def test():
        # create a user in the DB
        # removes everything from the DB
        DB.drop_all()
        # creates a new DB with indicated tables
        DB.create_all()
        # create a user object from .models class
        ryan = User(id=1, username='ryanallred')
        julian = User(id=2, username='julian')
        # Add user to database
        DB.session.add(ryan)
        DB.session.add(julian)
        # Save the database 
        # DB.session.commit()
        # display new user on page
        # Make some tweets
        tweet1 = Tweet(id=1, text='some tweet text', user=ryan)
        tweet2 = Tweet(id=2, text='some OTHER tweet text', user=julian)
        # Add the tweets
        DB.session.add(tweet1)
        DB.session.add(tweet2)
        DB.session.commit()
        # query to get all users
        users = User.query.all()
        return render_template('base.html', users=users, title='test')



    return app
