import pytest
from jsonschema import validate

from schemas import COMMENT_SCHEMA, USER_SCHEMA

pytestmark = pytest.mark.jsonplaceholder


def test_user_matches_schema(jsonplaceholder):
    response = jsonplaceholder.get("/users/1")

    assert response.status_code == 200
    validate(instance=response.json(), schema=USER_SCHEMA)


def test_nonexistent_user_returns_404(jsonplaceholder):
    response = jsonplaceholder.get("/users/9999")

    assert response.status_code == 404


def test_comments_for_a_post_all_reference_that_post(jsonplaceholder):
    response = jsonplaceholder.get("/posts/1/comments")

    assert response.status_code == 200
    comments = response.json()
    assert len(comments) > 0

    for comment in comments:
        validate(instance=comment, schema=COMMENT_SCHEMA)
        assert comment["postId"] == 1


def test_filtering_comments_by_query_param_matches_the_nested_route(jsonplaceholder):
    # jsonplaceholder supports both /posts/1/comments and /comments?postId=1 —
    # they should describe the same relationship, so cross-check them instead
    # of trusting either one in isolation.
    nested = jsonplaceholder.get("/posts/1/comments").json()
    filtered = jsonplaceholder.get("/comments", params={"postId": 1}).json()

    assert {c["id"] for c in nested} == {c["id"] for c in filtered}
