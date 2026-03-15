import pytest
import allure
from pages.login_page import LoginPage
from pages.order_page import OrderPage

@allure.feature("Orders")
@pytest.mark.parametrize("order_name", ["test-order"])
def test_order_processing(driver, db_client, corba_service, order_name):
    login_page = LoginPage(driver)
    order_page = OrderPage(driver)

    with allure.step("Открыть страницу логина"):
        login_page.open("http://localhost:8080")

    with allure.step("Создание заказа"):
        order_id = order_page.create_order(order_name)

    with allure.step("Проверка статуса NEW"):
        status = db_client.get_order_status(order_id)
        assert status == "New"

    with allure.step("Подготовка заказа CORBA"):
        corba_service.prepare_order(order_id)

    with allure.step("Проверка статуса READY"):
        status = db_client.get_order_status(order_id)
        assert status == "Ready"