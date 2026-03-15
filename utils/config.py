from dataclasses import dataclass
import os

@dataclass
class Config:
    base_url: str = os.getenv("BASE_URL", "http://localhost:8080")
    db_host: str = os.getenv("DB_HOST", "localhost")
    db_name: str = os.getenv("DB_NAME", "orders")
    db_user: str = os.getenv("DB_USER", "postgres")
    db_password: str = os.getenv("DB_PASSWORD", "postgres")

config = Config()