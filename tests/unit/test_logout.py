from server import app


def test_logout_successful():
    """
    GIVEN: a secretary that is logged in and on the welcome page.
    WHEN: he clicks the link to logout.
    THEN: he should be redirected to the index page
    """
    with app.test_client() as test_client:
        url = '/logout'
        logout_response = test_client.get(url)
        message = b'You should be redirected automatically to the target ' \
                  b'URL: <a href="/">/</a>.'
        assert message in logout_response.data
        assert logout_response.status_code == 302
