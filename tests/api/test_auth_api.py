"""API tests for the authentication endpoint.

Target: https://reqres.in/api/login (public demo REST API).

ReqRes only validates that the expected fields are *present*; it does not
check whether the credentials belong to a real user. Therefore the "failed
login" scenarios below exercise the documented validation rules (HTTP 400
with an explanatory error), not a wrong-password rejection.
"""

from __future__ import annotations

import pytest
import requests

LOGIN_URL = "https://reqres.in/api/login"

VALID_CREDENTIALS = {
    "email": "eve.holt@reqres.in",
    "password": "cityslicka",
}


@pytest.mark.api
@pytest.mark.smoke
def test_login_success_returns_token(api_session: requests.Session) -> None:
    """A login with both required fields returns 200 and a token."""
    response = api_session.post(LOGIN_URL, json=VALID_CREDENTIALS, timeout=15)

    assert response.status_code == 200, response.text

    body = response.json()
    assert isinstance(body.get("token"), str)
    assert body["token"].strip(), "The token must not be empty"


@pytest.mark.api
@pytest.mark.parametrize(
    ("payload", "expected_error"),
    [
        pytest.param(
            {"email": "peter@klaven"},
            "Missing password",
            id="missing-password",
        ),
        pytest.param(
            {"password": "cityslicka"},
            "Missing email or username",
            id="missing-email",
        ),
        pytest.param(
            {"email": "", "password": ""},
            "Missing email or username",
            id="empty-credentials",
        ),
    ],
)
def test_login_failure_returns_validation_error(
    api_session: requests.Session,
    payload: dict[str, str],
    expected_error: str,
) -> None:
    """An incomplete login is rejected with 400 and a descriptive error."""
    response = api_session.post(LOGIN_URL, json=payload, timeout=15)

    assert response.status_code == 400, response.text

    body = response.json()
    assert body.get("error") == expected_error
    assert "token" not in body
