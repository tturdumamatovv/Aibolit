import logging
import requests
from celery import shared_task
from django.db import transaction
from apps.medicine.models import Product

logger = logging.getLogger(__name__)

@shared_task
def load_products_from_api():
    logger.info("Начало выполнения задачи по загрузке товаров из API")

    # Учетные данные для авторизации
    login = "site"
    password = "123"

    # URL для запроса
    url = "http://193.176.239.110/1cBaseCabinet/hs/A8/data"

    # Тело запроса
    payload = {
        "Request": "Goods",
        "Date": "20240313000000"
    }

    try:
        # Выполнение запроса
        logger.info("Отправка запроса к API")
        response = requests.post(url, json=payload, auth=(login, password))

        if response.status_code == 200:
            logger.info("Получен успешный ответ от API")
            data = response.json()

            products_to_create = []
            products_to_update = []
            existing_products = {product.code: product for product in Product.objects.all()}

            for item in data:
                logger.debug(f"Обработка товара: {item['name']} с кодом {item['code']}")
                if item['code'] in existing_products:
                    product = existing_products[item['code']]
                    product.name = item['name']
                    product.sklad = item['sklad']
                    product.ostatok = item['ostatok']
                    product.price = item['price']
                    product.manufacturer = item['manufacturer']
                    product.country = item['country']
                    products_to_update.append(product)
                else:
                    products_to_create.append(Product(
                        code=item['code'],
                        name=item['name'],
                        sklad=item['sklad'],
                        ostatok=item['ostatok'],
                        price=item['price'],
                        manufacturer=item['manufacturer'],
                        country=item['country']
                    ))

            with transaction.atomic():
                if products_to_create:
                    Product.objects.bulk_create(products_to_create, batch_size=1000)
                    logger.info(f"Создано товаров: {len(products_to_create)}")
                if products_to_update:
                    Product.objects.bulk_update(products_to_update, ['name', 'sklad', 'ostatok', 'price', 'manufacturer', 'country'], batch_size=1000)
                    logger.info(f"Обновлено товаров: {len(products_to_update)}")

            logger.info("Задача по загрузке товаров успешно выполнена")
        else:
            error_message = f"Ошибка выполнения запроса: {response.status_code}"
            logger.error(error_message)
            raise Exception(error_message)
    except Exception as e:
        logger.error(f"Произошла ошибка: {str(e)}")
        raise
