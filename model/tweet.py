from typing import Type

from sqlalchemy.sql.functions import user
from model.tables import Tweet, Follow
from model.database import Database


class TweetDao:
    def __init__(self, database: Type[Database]):
        self.db = database

    def insert_tweet(self, user_id, tweet):
        with self.db.session_scope() as s:
            obj = Tweet(user_id=user_id, tweet=tweet)
            s.add(obj)
        return True

    def get_timeline(self, user_id):
        with self.db.session_scope() as s:
            rs = s.query(Follow).filter(Follow.user_id == user_id)
            follow_id_list = [item.follow_id for item in rs]
            follow_id_list.append(user_id)
            tweets = s.query(Tweet).filter(Tweet.user_id.in_(follow_id_list))
            return [
                {"user_id": tweet.user_id, "tweet": tweet.tweet} for tweet in tweets
            ]
