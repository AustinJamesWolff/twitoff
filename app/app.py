from flask import Flask, render_template
from .models import DB, User

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
        # Do this when visiting home page
        return render_template('base.html')
    
    @app.route("/test")
    def test():
        # create a user in the DB
        # removes everything from the DB
        DB.drop_all()
        # creates a new DB with indicated tables
        DB.create_all()
        # create a user object from .models class
        ryan = User(id=1, username='ryanallred')
        # Add user to database
        DB.session.add(ryan)
        # Save the database 
        DB.session.commit()



    return app
