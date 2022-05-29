from server import app, competitions, clubs, MAX_ALLOWED_TO_BOOK,\
    POINTS_PER_PLACE


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

        # Test that booking a number of places that the points can afford
        # works and the places will be confirmed.
        enough_points_response = test_client.post(url, data={
            'club': club['name'],
            'competition': competition['name'],
            'places': '1',
        })
        assert b'Great-booking complete!' in enough_points_response.data
        assert enough_points_response.status_code == 200

        # Test that booking more places than the points allow is not
        # possible and the places will not be confirmed.
        not_enough_points_response = test_client.post(url, data={
            'club': club['name'],
            'competition': competition['name'],
            'places': '6',
        })
        assert b'Your club does not have enough points.'\
               in not_enough_points_response.data
        assert not_enough_points_response.status_code == 200


def test_max_to_buy():
    """
    GIVEN a secretary who tries to book places in a competition
    WHEN he tries to book more than 12 places in one competition
    THEN he should not be able to book more than 12 places
    or more places than available.
    """
    with app.test_client() as test_client:
        club = clubs[0]
        competition = competitions[1]
        url = '/purchasePlaces'

        # Test that booking more than the allowed max. of 12 places is not
        # possible and an error message is displayed.
        more_than_allowed_response = test_client.post(url, data={
            'club': club['name'],
            'competition': competition['name'],
            'places': MAX_ALLOWED_TO_BOOK + 1,
        })
        message = f'Sorry, its not allowed to book more than '\
                  f'{MAX_ALLOWED_TO_BOOK} places.'
        assert bytes(message, 'utf-8') in more_than_allowed_response.data
        assert more_than_allowed_response.status_code == 200

        # Test that booking a valid and available number of places works and
        # the places will be confirmed.
        enough_places_response = test_client.post(url, data={
            'club': club['name'],
            'competition': competition['name'],
            'places': '2',
        })
        assert b'Great-booking complete!' in enough_places_response.data
        assert enough_places_response.status_code == 200

        # Test that booking more than the available number of places is not
        # possible and the places will not be confirmed.
        not_enough_places_response = test_client.post(url, data={
            'club': club['name'],
            'competition': competition['name'],
            'places': MAX_ALLOWED_TO_BOOK,
        })
        message = f"{competition['name']} has only "\
                  f"{int(competition['numberOfPlaces'])} places left."
        assert bytes(message, 'utf-8') in not_enough_places_response.data
        assert not_enough_places_response.status_code == 200


def test_deducted_points():
    """
    GIVEN a secretary wishes to redeem points for a place in a competition
    WHEN The number of places is confirmed.
    THEN The amount of points used should be deducted from the club's balance,
        and the booked places should be deducted from the competitions places.
    """
    with app.test_client() as test_client:
        club = clubs[0]
        competition = competitions[-1]
        url = '/purchasePlaces'

        points = int(club["points"])
        places = int(competition["numberOfPlaces"])
        to_book = 1

        places_booked_response = test_client.post(url, data={
            'club': club['name'],
            'competition': competition['name'],
            'places': to_book,
        })

        club_result = f'Points available: {points-to_book*POINTS_PER_PLACE}'
        comp_result = f'Number of Places: {places-to_book}'
        assert bytes(club_result, 'utf-8') in places_booked_response.data
        assert bytes(comp_result, 'utf-8') in places_booked_response.data
        assert places_booked_response.status_code == 200
