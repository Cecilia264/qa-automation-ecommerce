"""Environment smoke test.

Verifies that the framework is wired up correctly and that the target
application is reachable. Replace or extend with real business tests.
"""

from __future__ import annotations

import pytest
from playwright.sync_api import Page, expect


@pytest.mark.smoke
@pytest.mark.ui
def test_login_page_is_available(page: Page, base_url: str) -> None:
    page.goto(base_url, wait_until="domcontentloaded")

    expect(page).to_have_title("Swag Labs")
    expect(page.locator("#login-button")).to_be_visible()
