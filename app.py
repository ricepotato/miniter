import jwt
import functools
import bcrypt
import datetime
from flask import Flask, jsonify, request, Response, g, current_app
from flask.json import JSONEncoder


class CustomJsonEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)

        return JSONEncoder.default(self, obj)


def get_user_by_id(id):
    try:
        return current_app.users[id]
    except KeyError:
        return None


def login_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        access_token = request.headers.get("Authorization")
        if access_token is not None:
            try:
                payload = jwt.decode(
                    access_token, current_app.config["JWT_SECRET_KEY"], "HS256"
                )
            except jwt.InvalidTokenError:
                payload = None

            if payload is None:
                return Response(status=401)
            user_id = payload["user_id"]
            g.user_id = user_id
            g.user = get_user_by_id(user_id)
        else:
            return Response(status=401)

        return f(*args, **kwargs)

    return decorated_function


def create_app(test_config=None):
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = "5t0eob3vs3"
    app.users = {}
    app.tweets = []
    app.id_count = 1
    app.json_encoder = CustomJsonEncoder

    @app.route("/ping", methods=["GET"])
    def ping():
        return "pong"

    @app.route("/sign-up", methods=["POST"])
    def sign_up():
        new_user = request.json
        new_user["id"] = app.id_count
        new_user["password"] = bcrypt.hashpw(
            new_user["password"].encode("UTF-8"), bcrypt.gensalt()
        ).decode("UTF-8")
        app.users[app.id_count] = new_user
        app.id_count = app.id_count + 1

        return jsonify(new_user)

    @app.route("/login", methods=["POST"])
    def login():
        credential = request.json
        email = credential["email"]
        password = credential["password"]

        try:
            user = next(user for _, user in app.users.items() if user["email"] == email)
            if bcrypt.checkpw(
                password.encode("UTF-8"), user["password"].encode("UTF-8")
            ):
                user_id = user["id"]
                payload = {
                    "user_id": user_id,
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=60),
                }
                token = jwt.encode(payload, app.config["JWT_SECRET_KEY"], "HS256")
                return jsonify({"access_token": token})

        except StopIteration:
            pass

        return "", 401

    @app.route("/tweet", methods=["POST"])
    @login_required
    def tweet():
        payload = request.json
        user_id = g.user_id
        tweet = payload["tweet"]

        if user_id not in app.users:
            return "user not found.", 400

        if len(tweet) > 300:
            return "tweet too long", 400

        app.tweets.append({"user_id": user_id, "tweet": tweet})

        return "", 200

    @app.route("/follow", methods=["POST"])
    @login_required
    def follow():
        payload = request.json
        user_id = g.user_id
        user_id_to_follow = int(payload["follow"])

        if user_id not in app.users or user_id_to_follow not in app.users:
            return "user not found.", 400

        user = app.users[user_id]
        user.setdefault("follow", set()).add(user_id_to_follow)

        return jsonify(user)

    @app.route("/unfollow", methods=["POST"])
    @login_required
    def unfollow():
        payload = request.json
        user_id = g.user_id
        user_id_to_follow = int(payload["unfollow"])

        if user_id not in app.users or user_id_to_follow not in app.users:
            return "user not found.", 400

        user = app.user[user_id]
        user.setdefault("follow", set()).discard(user_id_to_follow)

        return jsonify(user)

    @app.route("/timeline/<int:user_id>", methods=["GET"])
    @login_required
    def timeline(user_id):
        if user_id not in app.users:
            return "user not found.", 400

        follow_list = app.users[user_id].get("follow", set())
        follow_list.add(user_id)
        timeline = [tweet for tweet in app.tweets if tweet["user_id"] in follow_list]

        return jsonify({"user_id": user_id, "timeline": timeline})

    return app
