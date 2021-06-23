import bcrypt
import unittest


class BcryptTestCase(unittest.TestCase):
    def tearDown(self):
        pass

    def setUp(self):
        pass

    def test_bcrypt(self):
        password = "secret password"
        b = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        hashed_password = b.decode("UTF-8")
        print(hashed_password)
        assert bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("UTF-8"))
