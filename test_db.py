import os
import dotenv
from model.database import Database
from model.user import UserDao


dotenv.load_dotenv(verbose=True)


def setup_function():
    db_file = os.environ.get("SQLITE_DB_FILE", "db.sqlite")
    if os.path.exists(db_file):
        os.remove(db_file)


def test_db():
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
