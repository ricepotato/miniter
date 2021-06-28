import os
import dotenv
from model.database import Database
from model.user import UserDao
from model.tweet import TweetDao


dotenv.load_dotenv(verbose=True)


def setup_function():
    db_file = os.environ.get("SQLITE_DB_FILE", "db.sqlite")
    if os.path.exists(db_file):
        os.remove(db_file)


def test_tweetdao():
    db = Database()
    db.create_all()

    user_dao = UserDao(db)
    tweet_dao = TweetDao(db)
    user1_id = user_dao.insert_user(
        {
            "email": "sukjun40@naver.com",
            "name": "사공석준",
            "password": "password1",
            "profile": "profile1",
        }
    )
    assert user1_id
    assert tweet_dao.insert_tweet(user1_id, "tweet text")

    user2_id = user_dao.insert_user(
        {
            "email": "ricepotato40@gmail.com",
            "name": "사공석준2",
            "password": "password2",
            "profile": "profile2",
        }
    )
    assert user2_id
    assert tweet_dao.insert_tweet(user2_id, "tweet text2")
    assert user_dao.insert_follow(user1_id, user2_id)
    timeline = tweet_dao.get_timeline(user1_id)
    assert len(timeline) == 2


def test_userdao():
    db = Database()
    db.create_all()

    user_dao = UserDao(db)
    user_id = user_dao.insert_user(
        {
            "email": "sukjun40@naver.com",
            "name": "사공석준",
            "password": "password1",
            "profile": "profile1",
        }
    )
    assert user_id

    res = user_dao.get_user_id_and_password("sukjun40@naver.com")
    assert user_id == res["id"]
    assert res["password"] == "password1"

    follow_id = user_dao.insert_user(
        {
            "email": "ricepotato40@gmail.com",
            "name": "사공석준2",
            "password": "password2",
            "profile": "profile2",
        }
    )
    assert follow_id
    assert user_dao.insert_follow(user_id, follow_id)
    assert user_dao.delete_follow(user_id, follow_id)
