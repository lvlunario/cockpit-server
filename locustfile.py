# locustfile.py
import random
from locust import HttpUser, task, between

# --- Shared Betting Logic ---
class BettingTasks:
    # It now accepts the active_event_id when created
    def __init__(self, user, active_event_id):
        self.user = user
        self.active_event_id = active_event_id
        self.valid_cashier_ids = list(range(1, 25))
    
    def place_bet(self):
        # ... (this part of the code is unchanged) ...
        BET_DENOMINATIONS = [20, 50, 100, 500, 1000]
        BET_WEIGHTS = [0.25, 0.30, 0.40, 0.10, 0.05]
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

# --- Base User Class with Initialization Logic ---
class BaseCashier(HttpUser):
    abstract = True # This tells Locust not to run this user directly
    
    def on_start(self):
        """Called once for each simulated user when they start."""
        self.active_event_id = None
        try:
            with self.client.get("/api/events/active/", catch_response=True) as response:
                if response.ok:
                    self.active_event_id = response.json()['id']
                    print(f"User found active event: {self.active_event_id}")
                else:
                    response.failure("Could not find active event")
        except Exception as e:
            print(f"Failed to get active event: {e}")

# --- User Types Simulating Different Hardware ---
class DesktopCashier(BaseCashier):
    wait_time = between(1, 3)
    weight = 10

    @task
    def place_bet_task(self):
        if self.active_event_id:
            tasks = BettingTasks(self, self.active_event_id)
            tasks.place_bet()

class TabletCashier(BaseCashier):
    wait_time = between(2, 5)
    weight = 10

    @task
    def place_bet_task(self):
        if self.active_event_id:
            tasks = BettingTasks(self, self.active_event_id)
            tasks.place_bet()

class HandheldCashier(BaseCashier):
    wait_time = between(3, 7)
    weight = 5

    @task
    def place_bet_task(self):
        if self.active_event_id:
            tasks = BettingTasks(self, self.active_event_id)
            tasks.place_bet()