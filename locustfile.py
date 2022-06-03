import random
from time import sleep
from locust import HttpUser, task, between

from server import clubs, competitions


class SecretaryUser(HttpUser):
    wait_time = between(0.5, 5)

    @task
    def landing(self):
        self.client.get('/', name='/index')

    @task(2)
    def show_summary(self):
        email = random.choice(clubs)['email']
        self.client.post(
            '/showSummary', data={'email': email}, name='/summary')

    @task(2)
    def click_on_book(self):
        club = random.choice(clubs)["name"]
        competition = random.choice(competitions)["name"]
        url = f'/book/{competition}/{club}'
        self.client.get(url, name='/book')

    @task
    def purchase_places(self):
        club = random.choice(clubs)['name']
        competition = random.choice(competitions)["name"]
        places = random.choice(range(1, 4))
        self.client.post(
            '/purchasePlaces',
            name='/purches',
            data={
                'club': club,
                'competition': competition,
                'places': places
            }
        )

    @task(2)
    def display_points(self):
        self.client.get('/points', name='/points')

    @task
    def logout(self):
        self.client.get('/logout', name='/logout')
