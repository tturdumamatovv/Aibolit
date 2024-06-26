# from django_elasticsearch_dsl import Document, fields, Index
#
# from .models import Product
#
# product_index = Index('products')
#
#
# @product_index.doc_type
# class ProductDocument(Document):
#     category = fields.ObjectField(properties={
#         'id': fields.IntegerField(),
#         'name': fields.TextField(),
#     })
#
#     class Django:
#         model = Product
#         fields = [
#             'name',
#             'sklad',
#             'ostatok',
#             'price',
#             'discounted_price',
#             'manufacturer',
#             'country',
#             'expiration_date',
#             'dosage',
#             'dosage_form',
#             'packaging',
#             'composition',
#             'contraindications',
#             'indications',
#             'side_effects',
#             'description',
#             'storage_rules',
#             'discount_percent',
#         ]
