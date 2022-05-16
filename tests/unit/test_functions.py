from server import app, competitions, clubs


def test_purchasePlaces():
    """
    GIVEN a secretary who tries to book places in a competition
    WHEN he tries to book more than 12 places in one competition
    THEN he should not be able to book more than 12 places.
    """
    with app.test_client() as test_client:
        club = clubs[0]
        competition = competitions[1]
        url = '/purchasePlaces'

        # Test that booking more than the allowed max. of 12 places is not
        # possible and the places will not be confirmed.
        more_than_allowed_response = test_client.post(url, data={
            'club': club['name'],
            'competition': competition['name'],
            'places': '13',
        })
        assert b'Great-booking complete!' not in more_than_allowed_response.data
        assert more_than_allowed_response.status_code == 200

        # Test that booking a valid and available number of places works and
        # the places will be confirmed.
        enough_places_response = test_client.post(url, data={
            'club': club['name'],
            'competition': competition['name'],
            'places': '6',
        })
        assert b'Great-booking complete!' in enough_places_response.data
        assert enough_places_response.status_code == 200

        # Test that booking more than the available number of places is not
        # possible and the places will not be confirmed.
        not_enough_places_response = test_client.post(url, data={
            'club': club['name'],
            'competition': competition['name'],
            'places': '12',
        })
        assert b'Great-booking complete!' not in not_enough_places_response.data
        assert not_enough_places_response.status_code == 200
