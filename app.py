import dotenv
import os
from flask import Flask
from flask_cors import CORS
from model.database import Database
from model.tweet import TweetDao
from model.user import UserDao
from service import UserService, TweetService
from view import create_endpoints


dotenv.load_dotenv(verbose=True)


class Services:
    pass


def create_app():
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")
    CORS(app)

    db = Database()

    user_dao = UserDao(db)
    tweet_dao = TweetDao(db)

    services = Services
    services.user_service = UserService(user_dao, app.config)
    services.tweet_service = TweetService(tweet_dao)

    create_endpoints(app, services)

    return app
