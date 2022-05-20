from server import app, competitions, clubs


def test_max_what_points_allow():
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
