from server import app, loadClubs, loadCompetitions, POINTS_PER_PLACE


def test_full():
    """
    GIVEN: The gudlift-registration Flask app is running
    WHEN: every function of this app is executed in sequential order
    THEN: each function must return the expected response, without any error
    """
    # run loadClubs()
    clubs = loadClubs()
    assert isinstance(clubs, list) and isinstance(clubs[0], dict)

    # run loadCompetitions()
    competitions = loadCompetitions()
    assert isinstance(competitions, list) and isinstance(competitions[0], dict)

    with app.test_client() as test_client:
        club = clubs[0]

        # run index()
        response = test_client.get("/")
        assert response.status_code == 200

        # run showSummary()
        email = club['email']
        known_email_response = test_client.post(
            "/showSummary", data={'email': email})
        header = bytes(f'Welcome, {email}', 'utf-8')
        assert header in known_email_response.data
        assert known_email_response.status_code == 200

        # run book()
        competition = competitions[-1]
        url_valid_comp = f'/book/{competition["name"]}/{club["name"]}'
        valid_comp_response = test_client.get(url_valid_comp)
        confirm = f'<title>Booking for {competition["name"]} || GUDLFT</title>'
        assert bytes(confirm, 'utf-8') in valid_comp_response.data
        assert valid_comp_response.status_code == 200

        # run purchasePlaces()
        points = int(club["points"])
        places = int(competition["numberOfPlaces"])
        to_book = 1

        places_booked_response = test_client.post('/purchasePlaces', data={
            'club': club['name'],
            'competition': competition['name'],
            'places': to_book,
        })
        club_result = f'Points available: {points - to_book * POINTS_PER_PLACE}'
        comp_result = f'Number of Places: {places - to_book}'
        assert bytes(club_result, 'utf-8') in places_booked_response.data
        assert bytes(comp_result, 'utf-8') in places_booked_response.data
        assert places_booked_response.status_code == 200

        # run logout()
        logout_response = test_client.get('/logout')
        message = b'You should be redirected automatically to the target ' \
                  b'URL: <a href="/">/</a>.'
        assert message in logout_response.data
        assert logout_response.status_code == 302
