import requests
import psycopg2

class PostgresClient:
    def __init__(self, host="localhost", db="orders", user="postgres", password="postgres"):
        try:
            self.connection = psycopg2.connect(
                host=host,
                database=db,
                user=user,
                password=password
            )
        except Exception:
            self.connection = None

    def get_order_status(self, order_id: int):
        if self.connection:
            query = """
            SELECT status
            FROM orders
            WHERE id = %s
            """
            with self.connection.cursor() as cursor:
                cursor.execute(query, (order_id,))
                result = cursor.fetchone()

            return result[0] if result else None

        r = requests.get(f"http://localhost:8080/order/{order_id}")
        return r.json()["status"]