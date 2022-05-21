from server import loadCompetitions


def test_competition_list():
    """
    GIVEN: an app tries that calls the function: loadCompetitions
    WHEN: the function is called
    THEN: it should return a list in which each competition is stored as a
        dictionary with the keys: 'name', 'date', 'numberOfPlaces'
    """
    competitions = loadCompetitions()
    keys = ['name', 'date', 'numberOfPlaces']
    assert isinstance(competitions, list)
    assert isinstance(competitions[0], dict)
    assert all(key in competitions[0].keys() for key in keys)
