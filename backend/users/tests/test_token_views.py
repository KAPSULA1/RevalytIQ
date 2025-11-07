import json

import pytest
from django.contrib.auth import get_user_model
from django.test import override_settings


TOKEN_URL = "/api/auth/token/"


@pytest.fixture
def demo_user():
    user = get_user_model().objects.create_user(
        username="demo",
        email="demo@example.com",
        password="password123",
    )
    return user


@pytest.mark.django_db
@override_settings(
    ALLOWED_HOSTS=[
        "testserver",
        "revalyt-iq.vercel.app",
        "revalytiq-backend.onrender.com",
        ".revalytiq.com",
        "localhost",
        "127.0.0.1",
    ]
)
@pytest.mark.parametrize(
    ("host", "forwarded_host", "expected_domain"),
    [
        ("revalyt-iq.vercel.app", None, "revalyt-iq.vercel.app"),
        (
            "revalytiq-backend.onrender.com",
            "revalyt-iq.vercel.app",
            "revalyt-iq.vercel.app",
        ),
        ("app.revalytiq.com", None, "revalytiq.com"),
        ("localhost", None, ""),
        ("127.0.0.1", None, ""),
    ],
)
def test_cookie_domain_follows_request_host(
    client,
    demo_user,
    host,
    forwarded_host,
    expected_domain,
):
    response = client.post(
        TOKEN_URL,
        data=json.dumps({"username": "demo", "password": "password123"}),
        content_type="application/json",
        HTTP_HOST=host,
        **({"HTTP_X_FORWARDED_HOST": forwarded_host} if forwarded_host else {}),
    )
    assert response.status_code == 200
    access_cookie = response.cookies["revalyt_access"]
    refresh_cookie = response.cookies["revalyt_refresh"]
    assert (access_cookie["domain"] or "") == expected_domain
    assert (refresh_cookie["domain"] or "") == expected_domain
