# locustfile.py
import random
from locust import HttpUser, task, between

# --- Shared Betting Logic ---
# Moved to a separate class to avoid repetition
class BettingTasks:
    def __init__(self, user):
        self.user = user
        self.active_event_id = 5 # IMPORTANT: Update this to your active event ID!
        self.valid_cashier_ids = list(range(1, 26)) # Assumes new IDs are 1-25

    def place_bet(self):
        BET_DENOMINATIONS = [20, 50, 100, 500, 1000]
        BET_WEIGHTS = [0.05, 0.10, 0.40, 0.30, 0.25] 

        random_cashier_id = random.choice(self.valid_cashier_ids)
        bet_amount = random.choices(BET_DENOMINATIONS, BET_WEIGHTS)[0]
        choices = ["Meron", "Wala"]
        random_choice = random.choice(choices)

        self.user.client.post(
            "/api/place-bet/",
            json={
                "event": self.active_event_id,
                "cashier": random_cashier_id,
                "amount": str(bet_amount),
                "bet_choice": random_choice
            },
            name="/api/place-bet/"
        )

# --- User Types Simulating Different Hardware ---

class DesktopCashier(HttpUser):
    # Desktop users are fast, they wait 1-3 seconds between bets
    wait_time = between(1, 3)
    # Give this user type a higher weight, making them more common
    weight = 10

    def on_start(self):
        self.tasks = BettingTasks(self)

    @task
    def place_bet_task(self):
        self.tasks.place_bet()

class TabletCashier(HttpUser):
    # Tablet users are a bit slower, waiting 2-5 seconds
    wait_time = between(2, 5)
    weight = 10

    def on_start(self):
        self.tasks = BettingTasks(self)

    @task
    def place_bet_task(self):
        self.tasks.place_bet()

class HandheldCashier(HttpUser):
    # Handheld POS users are the slowest, waiting 3-7 seconds
    wait_time = between(3, 7)
    weight = 5

    def on_start(self):
        self.tasks = BettingTasks(self)

    @task
    def place_bet_task(self):
        self.tasks.place_bet()