from server import app, competitions, clubs, url_for


def test_book():
    """
    GIVEN a secretary wishes to book a number of places for a competition
    WHEN he tries to book a number of places on a competition that has
         happened in the past
    THEN he  should not be able to book a place on a post-dated competition
    """
    with app.test_client() as test_client:
        club = clubs[0]
        competition = competitions[0]
        url = f'book/{competition["name"]}/{club["name"]}'
        invalid_comp_response = test_client.get(url)
        print(invalid_comp_response.data)
        assert invalid_comp_response.status_code == 200
        assert b'Sorry, but you cant book places on past competitions.' in invalid_comp_response.data
