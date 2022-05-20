from server import app


def test_index():
    """
    GIVEN an email was entered on the index page to register,
    WHEN the '/' page is posted to (GET),
    THEN check that the response (200) is returned.
    """

    with app.test_client() as test_client:
        response = test_client.get("/")
        assert response.status_code == 200
