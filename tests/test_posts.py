import pytest
from jsonschema import validate

from schemas import POST_SCHEMA

pytestmark = pytest.mark.jsonplaceholder


def test_get_all_posts_returns_the_full_collection(jsonplaceholder):
    response = jsonplaceholder.get("/posts")

    assert response.status_code == 200
    posts = response.json()
    assert len(posts) == 100
    validate(instance=posts[0], schema=POST_SCHEMA)


def test_get_single_post_matches_schema(jsonplaceholder):
    response = jsonplaceholder.get("/posts/1")

    assert response.status_code == 200
    validate(instance=response.json(), schema=POST_SCHEMA)


def test_get_nonexistent_post_returns_404(jsonplaceholder):
    response = jsonplaceholder.get("/posts/99999")

    assert response.status_code == 404


def test_create_post_echoes_the_body_and_assigns_an_id(jsonplaceholder):
    payload = {"title": "QA framework post", "body": "created by an automated test", "userId": 1}
    response = jsonplaceholder.post("/posts", json=payload)

    assert response.status_code == 201
    created = response.json()
    assert created["title"] == payload["title"]
    assert created["body"] == payload["body"]
    assert created["userId"] == payload["userId"]
    assert isinstance(created["id"], int)


def test_update_post_reflects_the_new_values(jsonplaceholder):
    payload = {"id": 1, "title": "updated by a test", "body": "new body", "userId": 1}
    response = jsonplaceholder.put("/posts/1", json=payload)

    assert response.status_code == 200
    assert response.json()["title"] == "updated by a test"


def test_patch_updates_only_the_given_field(jsonplaceholder):
    # PATCH vs. PUT is exactly the distinction worth testing here: PUT above
    # replaces the whole resource, PATCH should touch only what's sent and
    # leave the rest of the post exactly as it was.
    original = jsonplaceholder.get("/posts/1").json()
    response = jsonplaceholder.patch("/posts/1", json={"title": "patched title only"})

    assert response.status_code == 200
    patched = response.json()
    assert patched["title"] == "patched title only"
    assert patched["body"] == original["body"]
    assert patched["userId"] == original["userId"]


def test_delete_post_returns_200(jsonplaceholder):
    # jsonplaceholder is a mock API: this returns 200 with an empty body, but
    # doesn't actually delete anything server-side — a follow-up GET for the
    # same id still returns the original post. The response contract is what's
    # under test here, not real persistence.
    response = jsonplaceholder.delete("/posts/1")

    assert response.status_code == 200
    assert response.json() == {}


@pytest.mark.parametrize("post_id", [1, 50, 100])
def test_every_post_belongs_to_a_valid_user_id(jsonplaceholder, post_id):
    response = jsonplaceholder.get(f"/posts/{post_id}")

    assert 1 <= response.json()["userId"] <= 10
