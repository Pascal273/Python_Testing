from server import app, competitions, clubs


def test_purchasePlaces():
    """
    GIVEN a secretary wishes to book a number of places for a competition
    WHEN he tries to book a number of places on a competition that has
         happened in the past
    THEN he  should not be able to book a place on a post-dated competition
    """
    with app.test_client() as test_client:
        pass
