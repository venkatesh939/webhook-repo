from flask import Flask
from flask import request
from app.webhook.routes import webhook
from app.extensions import initialize_mongo


app = Flask(__name__)

# Creating our flask app
def create_app():

    # registering all the blueprints
    app.register_blueprint(webhook)
    
    # Initialize MongoDB with the app
    initialize_mongo(app)

    return app
