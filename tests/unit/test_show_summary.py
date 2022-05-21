from server import app, clubs


def test_unknown_email_response():
    """
    GIVEN an email was entered on the index page to register,
    WHEN the '/showSummary' page is posted to (POST),
    THEN check that an appropriate response is returned.
    """

    with app.test_client() as test_client:
        club = clubs[0]['email']
        url = "/showSummary"

        known_email_response = test_client.post(
            url, data={'email': club})
        header = bytes(f'Welcome, {club}', 'utf-8')
        assert header in known_email_response.data
        assert known_email_response.status_code == 200

        unknown_email_response = test_client.post(
            url, data={'email': 'unknown@gmail.com'}
        )
        print(unknown_email_response.data)
        message = b"Sorry, this email could not be found!"
        assert message in unknown_email_response.data
        assert unknown_email_response.status_code == 200
