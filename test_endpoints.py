import pytest
import json
from app import create_app


@pytest.fixture
def api():
    app = create_app()
    app.config["TEST"] = True
    api = app.test_client()

    return api


def setup_function():
    pass


def teardown_function():
    pass


def test_ping(api):
    resp = api.get("/ping")
    assert b"pong" in resp.data


def test_tweet(api):
    new_user = {
        "email": "sukjun40@naver.com",
        "password": "password1",
        "name": "사공석준",
        "profile": "test profile",
    }

    resp = api.post(
        "/sign-up", data=json.dumps(new_user), content_type="application/json"
    )
    assert resp.status_code == 200

    resp_json = json.loads(resp.data.decode("utf-8"))
    new_user_id = resp_json["id"]

    resp = api.post(
        "/login",
        data=json.dumps(
            {"email": "sukjun40@naver.com", "password": "password1"},
        ),
        content_type="application/json",
    )

    resp_json = json.loads(resp.data.decode("utf-8"))
    access_token = resp_json["access_token"]

    resp = api.post(
        "/tweet",
        data=json.dumps({"tweet": "hello world!"}),
        content_type="application/json",
        headers={"Authorization": access_token},
    )

    assert resp.status_code == 200
