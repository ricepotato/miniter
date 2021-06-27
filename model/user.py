from model.tables import User, Follow
from sqlalchemy.orm.exc import NoResultFound


class UserDao:
    def __init__(self, database):
        self.db = database

    def insert_user(self, user):
        with self.db.session_scope() as s:
            new_user = User(
                email=user["email"],
                password=user["password"],
                profile=user["profile"],
                name=user["name"],
            )
            s.add(new_user)
            s.flush()
            return new_user.id

    def get_user_id_and_password(self, email):
        with self.db.session_scope() as s:
            try:
                obj = s.query(User).filter(User.email == email).one()
                return {"id": obj.id, "password": obj.password}
            except NoResultFound:
                return None

    def insert_follow(self, user_id, follow_id):
        with self.db.session_scope() as s:
            obj = Follow(user_id=user_id, follow_id=follow_id)
            s.add(obj)

        return True

    def delete_follow(self, user_id, follow_id):
        with self.db.session_scope() as s:
            obj = (
                s.query(Follow)
                .filter(Follow.user_id == user_id)
                .filter(Follow.follow_id == follow_id)
            )
            obj.delete()
        return True
