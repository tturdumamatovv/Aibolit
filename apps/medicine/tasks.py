import logging
import requests
from celery import shared_task
from django.db import transaction
from apps.medicine.models import Product


@shared_task(bind=True)
def load_products_from_api(self):
    print("Начало выполнения задачи по загрузке товаров из API")

    login = "site"
    password = "123"
    url = "http://193.176.239.110/1cBaseCabinet/hs/A8/data"
    payload = {"Request": "Goods", "Date": "20240313000000"}

    try:
        print("Отправка запроса к API")
        response = requests.post(url, json=payload, auth=(login, password), timeout=5000)
        response.raise_for_status()  # Добавьте проверку успешного выполнения запроса
        data = response.json()

        products_to_create = []
        products_to_update = []
        existing_products = {product.code: product for product in Product.objects.all()}

        for item in data:
            print(f"Обработка товара: {item['name']} с кодом {item['code']}")
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
                print(f"Создано товаров: {len(products_to_create)}")
            if products_to_update:
                Product.objects.bulk_update(products_to_update, ['name', 'sklad', 'ostatok', 'price', 'manufacturer', 'country'], batch_size=1000)
                print(f"Обновлено товаров: {len(products_to_update)}")

        print("Задача по загрузке товаров успешно выполнена")
    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса к API: {e}")
        self.retry(exc=e, countdown=60, max_retries=3)
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")
        self.retry(exc=e, countdown=60, max_retries=3)
