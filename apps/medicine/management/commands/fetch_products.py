import requests
from django.core.management.base import BaseCommand

from apps.medicine.models import Product, Category


class Command(BaseCommand):
    help = 'Fetch products and categories from external API and save to database'

    def handle(self, *args, **kwargs):
        base_url = 'http://193.176.239.110/1cBaseCabinet/hs/A8/data'
        auth = ('site', '123')
        headers = {'Content-Type': 'application/json'}

        # Fetch products
        products_data = {"Request": "Goods"}
        response = requests.post(base_url, auth=auth, headers=headers, json=products_data)

        if response.status_code == 200:
            products = response.json()
            for product_data in products:
                category = Category.objects.filter(code=product_data.get('categoryCode')).first()
                Product.objects.update_or_create(
                    code=product_data['code'],
                    defaults={
                        'name': product_data['name'],
                        'sklad': product_data['sklad'],
                        'ostatok': product_data['ostatok'],
                        'price': product_data['price'],
                        'manufacturer': product_data.get('manufacturer', ''),
                        'country': product_data.get('country', ''),
                        'category': category
                    }
                )
            self.stdout.write(self.style.SUCCESS('Products fetched and saved successfully.'))
        else:
            self.stderr.write(f"Failed to fetch products: {response.status_code} - {response.text}")
