from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class LoginPage(BasePage):
    LOGIN = (By.ID, "login")
    PASSWORD = (By.ID, "password")
    SUBMIT = (By.ID, "submit")

    def open(self, base_url):
        self.driver.get(f"{base_url}/login")

    def login(self, username, password):
        self.type(self.LOGIN, username)
        self.type(self.PASSWORD, password)
        self.click(self.SUBMIT)