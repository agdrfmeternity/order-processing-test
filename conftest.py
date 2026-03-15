import pytest
import threading
import time
import requests
import allure
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from mock_server.app import run
from services.postgres_client import PostgresClient
from services.corba_client import OrderService

@pytest.fixture(scope="session", autouse=True)
def server():
    thread = threading.Thread(target=run, daemon=True)
    thread.start()
    for _ in range(10):
        try:
            requests.get("http://localhost:8080/login")
            break
        except Exception:
            time.sleep(0.5)
    yield

@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)

    yield driver

    driver.quit()

@pytest.fixture
def db_client():
    return PostgresClient()

@pytest.fixture
def corba_service():
    return OrderService()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get("driver", None)
        if driver:
            screenshot = driver.get_screenshot_as_png()
            allure.attach(
                screenshot,
                name=f"screenshot_{item.name}",
                attachment_type=allure.attachment_type.PNG
            )