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