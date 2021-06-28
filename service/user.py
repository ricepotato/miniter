import bcrypt
import datetime
import jwt


class UserService:
    def __init__(self, user_dao, config):
        self.user_dao = user_dao
        self.config = config

    def create_new_user(self, new_user):
        hashed_password = bcrypt.hashpw(
            new_user["password"].encode("UTF-8"), bcrypt.gensalt()
        )
        new_user["password"] = hashed_password.decode("UTF-8")

        new_user_id = self.user_dao.insert_user(new_user)
        return new_user_id

    def login(self, credential):
        email = credential["email"]
        password = credential["password"]
        user_credential = self.user_dao.get_user_id_and_password(email)

        if user_credential and bcrypt.checkpw(
            password.encode("UTF-8"), user_credential["hashed_password"].encode("UTF-8")
        ):
            return user_credential["id"]
        else:
            return None

    def generate_access_token(self, user_id):
        payload = {
            "user_id": user_id,
            "exp": datetime.datetime.utcnow()
            + datetime.timedelta(seconds=60 * 60 * 24),
        }
        token = jwt.encode(payload, self.config["JWT_SECRET_KEY"], "HS256")
        return token

    def follow(self, user_id, follow_id):
        return self.user_dao.insert_follow(user_id, follow_id)

    def unfollow(self, user_id, unfollow_id):
        return self.user_dao.insert_unfollow(user_id, unfollow_id)
