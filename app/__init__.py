from .app import create_app

# Telling flask to use create_app function (factory)
# now our app will be named "APP"
APP = create_app()