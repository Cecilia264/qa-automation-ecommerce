"""Page Object Model for the SauceDemo login screen.

Encapsulates selectors and user interactions so tests stay focused on intent
rather than on DOM details. See https://www.saucedemo.com.
"""

from __future__ import annotations

import re

from playwright.sync_api import Page, expect


class LoginPage:
    """Login page at the root of the application."""

    PATH = "/"

    # User-facing validation messages exposed by SauceDemo.
    ERROR_REQUIRED_USERNAME = "Username is required"
    ERROR_INVALID_CREDENTIALS = "Username and password do not match"
    ERROR_LOCKED_OUT = "Sorry, this user has been locked out"

    def __init__(self, page: Page) -> None:
        self.page = page
        self.username_input = page.get_by_placeholder("Username")
        self.password_input = page.get_by_placeholder("Password")
        self.login_button = page.get_by_role("button", name="Login")
        self.error_message = page.locator('[data-test="error"]')
        self.login_logo = page.locator(".login_logo")

    def open(self) -> LoginPage:
        """Navigate to the login page using the configured base URL."""
        self.page.goto(self.PATH, wait_until="domcontentloaded")
        return self

    def expect_loaded(self) -> None:
        """Assert that the login form is rendered and ready for input."""
        expect(self.login_logo).to_have_text("Swag Labs")
        expect(self.username_input).to_be_visible()
        expect(self.password_input).to_be_visible()
        expect(self.login_button).to_be_enabled()

    def login(self, username: str, password: str) -> None:
        """Fill the credentials and submit the form."""
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

    def expect_error(self, message: str | re.Pattern[str]) -> None:
        """Assert that the validation banner contains the given message."""
        expect(self.error_message).to_be_visible()
        expect(self.error_message).to_contain_text(message)

    def expect_successful_login(self) -> None:
        """Assert that authentication redirected to the inventory page."""
        expect(self.page).to_have_url(re.compile(r"/inventory\.html$"))
        expect(self.page.locator(".inventory_list")).to_be_visible()
