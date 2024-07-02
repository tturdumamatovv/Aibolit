from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from .models import Product


@registry.register_document
class ProductDocument(Document):
    name = fields.TextField(
        fields={'raw': fields.KeywordField()}
    )

    class Index:
        name = 'products'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }

    class Django:
        model = Product
        fields = [
            'code',
            'sklad',
            'ostatok',
            'price',
            'manufacturer',
            'country',
            'expiration_date',
            'dosage',
            'dosage_form',
            'packaging',
            'composition',
            'contraindications',
            'indications',
            'side_effects',
            'description',
            'storage_rules',
            'discount_percent',
            'discounted_price',
            'is_product_of_the_day',
        ]
