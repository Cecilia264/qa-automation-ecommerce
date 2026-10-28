"""Shared fixtures and configuration for the test suite."""

from __future__ import annotations

from collections.abc import Iterator

import pytest
import requests


@pytest.fixture(scope="session")
def api_session() -> Iterator[requests.Session]:
    """Reusable HTTP session for API-level tests.

    Keeps cookies and connection pooling across the whole session.
    Combine it with the ``base_url`` fixture provided by pytest-playwright.
    """
    session = requests.Session()
    session.headers.update(
        {
            "Accept": "application/json",
            "User-Agent": "qa-automation-ecommerce/1.0",
        }
    )
    yield session
    session.close()
