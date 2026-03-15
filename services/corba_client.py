import requests

class OrderService:
    BASE = "http://localhost:8080"

    def prepare_order(self, order_id):
        requests.post(f"{self.BASE}/prepare/{order_id}")