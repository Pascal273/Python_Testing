from server import app, competitions, clubs


def test_book_past_competitions():
    """
    GIVEN a secretary wishes to book a number of places for a competition
    WHEN he tries to book a number of places on a competition that has
         happened in the past
    THEN he should not be able to book a place on a post-dated competition
    """
    with app.test_client() as test_client:
        club = clubs[0]
        past_comp = competitions[0]
        valid_comp = competitions[-1]

        url_invalid_comp = f'book/{past_comp["name"]}/{club["name"]}'
        invalid_comp_response = test_client.get(url_invalid_comp)
        message = b'Sorry, but you cant book places on past competitions.'
        assert message in invalid_comp_response.data
        assert invalid_comp_response.status_code == 200

        url_valid_comp = f'book/{valid_comp["name"]}/{club["name"]}'
        valid_comp_response = test_client.get(url_valid_comp)
        print(valid_comp_response.data)
        confirm = f'<title>Booking for {valid_comp["name"]} || GUDLFT</title>'
        assert bytes(confirm, 'utf-8') in valid_comp_response.data
        assert valid_comp_response.status_code == 200
