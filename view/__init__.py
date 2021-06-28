import functools
import jwt
from flask import request, jsonify, current_app, Response, g
from flask.json import JSONEncoder


class CustomJsonEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)

        return JSONEncoder.default(self, obj)


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
        else:
            return Response(status=401)

        return f(*args, **kwargs)

    return decorated_function


def create_endpoints(app, services):
    app.json_encoder = CustomJsonEncoder
    user_service = services.user_service
    tweet_service = services.tweet_service

    @app.route("/ping", methods=["GET"])
    def ping():
        return "pong"

    @app.route("/sign-up", methods=["POST"])
    def sign_up():
        new_user = request.json
        new_user_id = user_service.create_new_user(new_user)

        return jsonify({"user_id": new_user_id})

    @app.route("/login", methods=["POST"])
    def login():
        credential = request.json
        user_id = user_service.login(credential)
        if user_id:
            token = user_service.generate_access_token(user_id)
            return jsonify({"user_id": user_id, "access_token": token})
        else:
            return "", 401

    @app.route("/tweet", methods=["POST"])
    @login_required
    def tweet():
        user_tweet = request.json
        tweet = user_tweet["tweet"]
        user_id = g.user_id

        result = tweet_service.tweet(user_id, tweet)
        if result is None:
            return "tweet too long", 400

        return "", 200

    @app.route("/follow", methods=["POST"])
    @login_required
    def follow():
        payload = request.json
        user_id = g.user_id
        follow_id = payload["follow"]

        user_service.follow(user_id, follow_id)

        return "", 200

    @app.route("/unfollow", methods=["POST"])
    @login_required
    def unfollow():
        payload = request.json
        user_id = g.user_id
        unfollow_id = payload["unfollow"]

        user_service.unfollow(user_id, unfollow_id)

        return "", 200

    @app.route("/timeline/<int:user_id>", methods=["GET"])
    def timeline(user_id):
        timeline = tweet_service.timeline(user_id)
        return jsonify({"user_id": user_id, "timeline": timeline})

    @app.route("/timeline", methods=["GET"])
    @login_required
    def user_timeline():
        timeline = tweet_service.timeline(g.user_id)
        return jsonify({"user_id": g.user_id, "timeline": timeline})
