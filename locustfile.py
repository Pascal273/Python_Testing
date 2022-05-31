import random
from time import sleep
from locust import HttpUser, task, between

from server import clubs, competitions


class SecretaryUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def landing(self):
        self.client.get('/')

    @task(2)
    def show_summary(self):
        email = random.choice(clubs)['email']
        self.client.post('/showSummary', data={'email': email})
