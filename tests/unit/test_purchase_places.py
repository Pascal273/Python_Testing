from server import app, competitions, clubs


def test_deducted_points():
    """
    GIVEN a secretary wishes to redeem points for a place in a competition
    WHEN The number of places is confirmed.
    THEN The amount of points used should be deducted from the club's balance.
    """
    with app.test_client() as test_client:
        club = clubs[0]
        competition = competitions[0]
        url = '/purchasePlaces'

        points = int(club["points"])
        places = 1

        places_booked_response = test_client.post(url, data={
            'club': club['name'],
            'competition': competition['name'],
            'places': places,
        })

        correct_result = f'Points available: {points-places}'
        assert bytes(correct_result, 'utf-8') in places_booked_response.data
        assert places_booked_response.status_code == 200
