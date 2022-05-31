from server import app, clubs


def test_display_points():
    """
    GIVEN a user or secretary who wants to se the current points of each club
    WHEN they visit the got directed to the /points route
    THEN they should see a table of all clubs and their current points
    """
    with app.test_client() as test_client:
        club_names = [club['name'] for club in clubs]
        points_response = test_client.get('/points')
        assert all(
            bytes(name, 'utf-8') in points_response.data for name in club_names
        )
