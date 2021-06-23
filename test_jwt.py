import jwt
import unittest


class JwtTestCase(unittest.TestCase):
    def tearDown(self):
        pass

    def setUp(self):
        pass

    def test_jwt(self):
        data_to_encode = {"some": "payload"}
        encryption_secret = "secrete"
        algorithm = "HS256"

        encoded = jwt.encode(data_to_encode, encryption_secret, algorithm=algorithm)
        decoded = jwt.decode(encoded, encryption_secret, algorithms=[algorithm])

        assert decoded["some"] == data_to_encode["some"]