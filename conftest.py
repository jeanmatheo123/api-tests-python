import pytest
import requests

JSONPLACEHOLDER_URL = "https://jsonplaceholder.typicode.com"
HTTPBIN_URL = "https://httpbin.org"


@pytest.fixture(scope="session")
def jsonplaceholder():
    """A requests.Session pre-configured for jsonplaceholder, reused across
    the whole run so every test isn't paying for a fresh TCP/TLS handshake."""
    session = requests.Session()
    session.headers.update({"Content-Type": "application/json"})
    yield _BaseUrlSession(session, JSONPLACEHOLDER_URL)


@pytest.fixture(scope="session")
def httpbin():
    session = requests.Session()
    yield _BaseUrlSession(session, HTTPBIN_URL)


class _BaseUrlSession:
    """Thin wrapper so tests can write jsonplaceholder.get("/posts/1")
    instead of repeating the full URL in every single test."""

    def __init__(self, session: requests.Session, base_url: str):
        self._session = session
        self._base_url = base_url

    def __getattr__(self, method_name):
        def request(path: str, **kwargs):
            return getattr(self._session, method_name)(f"{self._base_url}{path}", **kwargs)

        return request
