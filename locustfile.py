import random
from locust import HttpUser, task, between

class CashierUser(HttpUser):
    wait_time = between(1, 5) # Wait 1-5 seconds between bets
    
    @task
    def place_bet(self):
        # Select a random cashier and event(update logic once real cashiers are in place)
        random_cashier_id = random.randint(1, 10)
        event_id = 1 # Assuming we have one event with ID 1
        bet_amount = round(random.uniform(10.0, 500.0), 2)
        choices = ["Team A Win", "Team B Win", "Draw"]
        random_choice = random.choice(choices)
        
        self.client.post(
            "/api/place-bet/",
            json={
                "event": event_id,
                "cashier": random_cashier_id,
                "amount": str(bet_amount),
                "bet_choice": random_choice
            }
        )