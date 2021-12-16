from flask_sqlalchemy import SQLAlchemy

# Create a DB object
# Open up DB connection
DB = SQLAlchemy()

# Create a table in the DB
# using Python classes

class User(DB.Model):
    # for the different columns in our db,
    # Each one will be its own attribute
    # on this Python class

    # ID Column Schema
    id = DB.Column(DB.BigInteger, primary_key=True, nullable=False)

    # Username Column Schema
    username = DB.Column(DB.String, nullable=False)
    # the backref down below adds a list of tweets here

    def __repr__(self):
        return f'<User: {self.username}>'

class Tweet(DB.Model):
    # ID Schema
    id = DB.Column(DB.BigInteger, primary_key=True, nullable=False)
    # Text Schema
    text = DB.Column(DB.Unicode(300), nullable=False)
    # User Schema
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey('user.id'), nullable=False)
    # Set up a relatonship between tweets and IDs
    # This will automatically add a new id to both 
    # the tweet and the user
    embeddings = DB.Column(DB.PickleType, nullable=False)
    user = DB.relationship('User', backref=DB.backref('tweets'), lazy=True)

    def __repr__(self):
        return f'<User: {self.text}>'
    
