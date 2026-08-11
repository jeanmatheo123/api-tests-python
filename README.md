# API Tests (Python)

![API Tests](https://github.com/jeanmatheo123/api-tests-python/actions/workflows/ci.yml/badge.svg)

API test suite built with pytest, `requests` and `jsonschema`, covering two different kinds of public APIs on purpose:

- **[JSONPlaceholder](https://jsonplaceholder.typicode.com)** — a fake REST API for CRUD-style resources (posts, users, comments). It's a mock: writes are echoed back with a plausible response but nothing is actually persisted, which the delete/update tests call out explicitly rather than pretending otherwise.
- **[httpbin](https://httpbin.org)** — not a resource API at all, but a service for inspecting HTTP behavior itself: arbitrary status codes, header echoing, basic auth, redirects. This is here to test protocol-level handling (does the client actually get a 401 back, does a redirect get followed correctly) rather than any particular business data.

## What's covered

**`tests/test_posts.py`** — schema validation on both a single resource and a full collection, a 404 on a missing id, create/update/delete against the mock API's actual contract, and a parametrized check across several post ids.

**`tests/test_users_and_comments.py`** — schema validation for a nested resource (a user's address/geo/company), a 404 case, and a cross-check that `/posts/1/comments` and `/comments?postId=1` describe the same data — two different routes into the same relationship shouldn't be trusted independently.

**`tests/test_http_behavior.py`** — parametrized status codes, header echoing, correct vs. incorrect basic auth, and redirects tested both ways: followed automatically (checking `response.history`) and inspected raw with `allow_redirects=False`.

## Structure

```
conftest.py     session-scoped fixtures — a small base-URL-aware wrapper around
                requests.Session so tests write jsonplaceholder.get("/posts/1")
                instead of the full URL every time
schemas.py      jsonschema definitions, one per resource shape
tests/          one file per API area
```

## Running it

```bash
python -m venv .venv
.venv\Scripts\activate        # .venv/bin/activate on Linux/macOS
pip install -r requirements.txt
pytest -v
```

Run just one API's tests with the markers registered in `pytest.ini`:

```bash
pytest -m jsonplaceholder
pytest -m httpbin
```

## CI

GitHub Actions runs the full suite on every push to `main`, on pull requests, and weekly.
