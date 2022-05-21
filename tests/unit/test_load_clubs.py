from server import loadClubs


def test_club_list():
    """
    GIVEN: an app tries that calls the function: loadClubs
    WHEN: the function is called
    THEN: it should return a list in which each club is stored as a dictionary
        with the keys: 'name', 'email', 'points'
    """
    clubs = loadClubs()
    keys = ['name', 'email', 'points']
    assert isinstance(clubs, list)
    assert isinstance(clubs[0], dict)
    assert all(key in clubs[0].keys() for key in keys)
