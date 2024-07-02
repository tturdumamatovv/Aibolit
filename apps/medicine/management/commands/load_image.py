import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
from django.core.management.base import BaseCommand
from apps.medicine.models import Product, ProductImage


class Command(BaseCommand):
    help = 'Fetch images from Aibolit.kg based on product name'

    def handle(self, *args, **options):
        products = Product.objects.all()

        for product in products:
            search_url = f'https://www.aibolit.kg/search?q={quote_plus(product.name)}'
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

            try:
                response = requests.get(search_url, headers=headers)
                soup = BeautifulSoup(response.content, 'html.parser')

                # Find images related to products
                images = soup.find_all('img', class_='category-list')  # Adjust class or other attributes as per HTML structure

                if images:
                    image_url = images[0]['src']  # Assuming first image related to the product

                    # Save the image for the product
                    product_image = ProductImage(product=product, image=image_url, main=True)
                    product_image.save()

                    self.stdout.write(self.style.SUCCESS(f'Successfully saved image for {product.name}'))
                else:
                    self.stderr.write(self.style.ERROR(f'No image found for {product.name}'))
            except Exception as e:
                self.stderr.write(self.style.ERROR(f'Failed to fetch image for {product.name}: {str(e)}'))
