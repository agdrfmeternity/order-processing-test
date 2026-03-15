# Order Processing Test Framework
Прототип мини-фреймворка для интеграционного тестирования системы обработки заказов.

# Стек
- Python 3.10+
- Pytest
- Selenium
- Allure
- PostgreSQL
- CORBA (IDL + ORB)
- Flask (mock test server)

# Архитектура проекта
pages/  #Page Object Model
services/  #интеграции (DB, CORBA)
mock_server/  #локальная система заказов
tests/  #тесты
conftest.py  #pytest fixtures

# Интеграционный сценарий

Тест автоматизирует следующий сценарий:
1. Авторизация в системе
2. Создание заказа
3. Проверка записи заказа в БД со статусом **New**
4. Вызов CORBA сервиса для подготовки заказа
5. Проверка изменения статуса на **Ready**

# PostgreSQL
Для работы с БД используется библиотека **psycopg2**.

Пример SQL запроса:
SELECT status
FROM orders
WHERE id = %s

Запрос параметризован.
Если PostgreSQL недоступен, используется mock.

# CORBA
Для интеграции предполагается использование:
omniORB
omniORBpy

IDL описание сервиса
IDL файл находится в:
idl/order_service.idl
Содержимое:
module OrderSystem {

    interface OrderService {

        void prepareOrder(in long orderId);

    };

};

IDL компилируется с помощью:
omniidl -bpython order_service.idl
После компиляции генерируются Python stubs для удаленного вызова метода.

# Пример подключения к ORB
Пример фикстуры для подключения к CORBA NameService:
import CORBA
import CosNaming


def get_order_service():

    orb = CORBA.ORB_init()

    obj = orb.resolve_initial_references("NameService")

    naming_context = obj._narrow(CosNaming.NamingContext)

    name = [CosNaming.NameComponent("OrderService", "")]

    order_service_obj = naming_context.resolve(name)

    order_service = order_service_obj._narrow(OrderService.OrderService)

    return order_service

# Локальный тестовый сервер
Поскольку реальный стенд может отсутствовать, в проекте используется mock сервер на Flask.
Он эмулирует:
UI страницы
систему создания заказов
хранение заказов
CORBA сервис подготовки заказов
Сервер автоматически поднимается перед запуском тестов через pytest fixture.

# УСТАНОВКА И ЗАПУСК
1. Создание виртуального окружения
python -m venv .venv
2. Активация окружения (если по какой-то причине ещё не активировалось)
.venv\Scripts\activate
3. Установка зависимостей
pip install -r requirements.txt
4. Запуск тестов
pytest
5. Отчёт Allure
allure serve allure-results
6. Для автоматического запуска тестов используется GitHub Actions.
Pipeline выполнит установку зависимостей, запуск pytest и сгенерирует Allure отчёт.
Конфигурация находится в: 
.github/workflows/tests.yml

# РЕЗУЛЬТАТ
Фреймворк демонстрирует:
1. Использование Page Object Model
2. разделение логики на слои
3. интеграцию с БД
4. интеграцию с распределенным сервисом (CORBA)
5. использование pytest fixtures
6. генерацию Allure отчетов
7. интеграцию с CI/CD
