import requests

class OrderPage:
    BASE = "http://localhost:8080"
    def __init__(self, driver):
        self.driver = driver

    def create_order(self, name):
        r = requests.post(
            f"{self.BASE}/create_order",
            json={"name": name}
        )
        return r.json()["order_id"]