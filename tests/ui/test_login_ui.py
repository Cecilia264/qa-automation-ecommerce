"""UI tests for the SauceDemo login flow (Playwright + Page Object Model)."""

from __future__ import annotations

import pytest
from playwright.sync_api import Page

from pages.login_page import LoginPage

VALID_USERNAME = "standard_user"
VALID_PASSWORD = "secret_sauce"


@pytest.mark.ui
@pytest.mark.smoke
def test_successful_login(page: Page) -> None:
    """A valid standard user reaches the inventory page."""
    login_page = LoginPage(page).open()
    login_page.expect_loaded()

    login_page.login(VALID_USERNAME, VALID_PASSWORD)

    login_page.expect_successful_login()


@pytest.mark.ui
@pytest.mark.parametrize(
    ("username", "password", "expected_error"),
    [
        pytest.param(
            "",
            "",
            LoginPage.ERROR_REQUIRED_USERNAME,
            id="empty-fields",
        ),
        pytest.param(
            VALID_USERNAME,
            "wrong_password",
            LoginPage.ERROR_INVALID_CREDENTIALS,
            id="wrong-password",
        ),
        pytest.param(
            "locked_out_user",
            VALID_PASSWORD,
            LoginPage.ERROR_LOCKED_OUT,
            id="locked-out-user",
        ),
    ],
)
def test_failed_login_shows_error(
    page: Page,
    username: str,
    password: str,
    expected_error: str,
) -> None:
    """Invalid credentials keep the user on the login page with an error."""
    login_page = LoginPage(page).open()
    login_page.expect_loaded()

    login_page.login(username, password)

    login_page.expect_error(expected_error)
    assert "/inventory.html" not in page.url
