from server import app, competitions, clubs


def test_index():
    """
    GIVEN an email was entered on the index page to register,
    WHEN the '/' page is posted to (GET),
    THEN check that the response (200) is returned.
    """

    with app.test_client() as test_client:
        response = test_client.get("/")
        assert response.status_code == 200


def test_unknown_email_response():
    """
    GIVEN an email was entered on the index page to register,
    WHEN the '/showSummary' page is posted to (POST),
    THEN check that an appropriate response is returned.
    """

    with app.test_client() as test_client:
        url = "/showSummary"
        known_email_response = test_client.post(
            url, data={'email': 'john@simplylift.co'})
        unknown_email_response = test_client.post(
            url, data={'email': 'nils@gmail.com'}
        )
        assert known_email_response.status_code == 200
        assert unknown_email_response.status_code == 200
