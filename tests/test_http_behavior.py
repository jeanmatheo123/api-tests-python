import pytest

pytestmark = pytest.mark.httpbin


@pytest.mark.parametrize("status_code", [200, 201, 404, 418, 500])
def test_arbitrary_status_codes_are_returned_as_requested(httpbin, status_code):
    response = httpbin.get(f"/status/{status_code}")

    assert response.status_code == status_code


def test_custom_headers_are_echoed_back(httpbin):
    response = httpbin.get("/headers", headers={"X-Custom-Header": "qa-framework"})

    assert response.json()["headers"]["X-Custom-Header"] == "qa-framework"


def test_correct_basic_auth_succeeds(httpbin):
    response = httpbin.get("/basic-auth/jean/secret123", auth=("jean", "secret123"))

    assert response.status_code == 200
    assert response.json() == {"authenticated": True, "user": "jean"}


def test_wrong_basic_auth_credentials_are_rejected(httpbin):
    response = httpbin.get("/basic-auth/jean/secret123", auth=("jean", "not-the-password"))

    assert response.status_code == 401


def test_redirect_is_followed_to_its_final_destination(httpbin):
    response = httpbin.get("/redirect-to", params={"url": "https://httpbin.org/get"})

    assert response.status_code == 200
    assert response.url == "https://httpbin.org/get"
    assert len(response.history) == 1
    assert response.history[0].status_code == 302


def test_redirect_can_be_inspected_without_following_it(httpbin):
    response = httpbin.get(
        "/redirect-to", params={"url": "https://httpbin.org/get"}, allow_redirects=False
    )

    assert response.status_code == 302
    assert response.headers["Location"] == "https://httpbin.org/get"
