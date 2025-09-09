# locustfile.py
import random
from locust import HttpUser, task, between

class CashierUser(HttpUser):
    wait_time = between(1, 4)  # Cashiers wait 1-4 seconds between bets

    # Define the realistic bet amounts and their likelihood
    # These are the "denominations" a cashier would use.
    BET_DENOMINATIONS = [20, 50, 100, 500, 1000]

    # Define the "weights" or probability for each denomination.
    # This makes smaller bets much more common than large ones.
    # (e.g., 100 PHP is 8 times more likely than 1000 PHP)
    BET_WEIGHTS = [0.05, 0.10, 0.40, 0.30, 0.25] # Must add up to 1.0

    def on_start(self):
        """Called when a Locust user starts. We'll find the cashier and event counts once."""
        # In a real scenario, you might query the API for this info.
        # For now, we'll stick to our known seeded data.
        self.cashier_count = 10
        self.main_event_id = 1

    @task
    def place_bet(self):
        # Select a random cashier ID from 1 to 10
        random_cashier_id = random.randint(1, self.cashier_count)

        # Choose a bet amount based on our weighted denominations
        # The [0] is because random.choices returns a list, and we want the first item.
        bet_amount = random.choices(self.BET_DENOMINATIONS, self.BET_WEIGHTS)[0]

        # The possible outcomes for the event
        choices = ["Meron", "Wala", "Draw"]
        random_choice = random.choice(choices)

        # Send the realistic bet data to the server
        self.client.post(
            "/api/place-bet/",
            json={
                "event": self.main_event_id,
                "cashier": random_cashier_id,
                "amount": str(bet_amount),
                "bet_choice": random_choice
            },
            name="/api/place-bet/ [denomination]" # Group stats under a clean name
        )