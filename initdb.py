import dotenv
from model.database import Database

dotenv.load_dotenv(verbose=False)


db = Database()
db.drop_all()
db.create_all()