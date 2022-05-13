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


def test_showSummary():
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


# def test_book():
#     """
#     GIVEN
#     WHEN
#     THEN
#     """
#

def test_purchasePlaces():
    """
    GIVEN a secretary who wants to book places in a competition
    WHEN he tries to book x number of places
    THEN he should not be able to use more than their points allowed
    """
    with app.test_client() as test_client:
        club = clubs[1]
        competition = competitions[0]
        url = '/purchasePlaces'
        enough_points_response = test_client.post(url, data={
            'club': club['name'],
            'competition': competition['name'],
            'places': '4',
        })
        assert b'Great-booking complete!' in enough_points_response.data
        assert enough_points_response.status_code == 200

        not_enough_points_response = test_client.post(url, data={
            'club': club['name'],
            'competition': competition['name'],
            'places': '6',
        })
        assert b'Great-booking complete!' not in not_enough_points_response.data
        assert not_enough_points_response.status_code == 200
