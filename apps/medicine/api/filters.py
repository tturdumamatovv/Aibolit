from django_filters import rest_framework as filters
from apps.medicine.models import Product, Purpose


class ProductFilter(filters.FilterSet):
    PURPOSE_CHOICES = Purpose.PRODUCT_CHOICES  # Получаем доступ к выбору из модели Purpose

    purposes = filters.ChoiceFilter(field_name='purposes__purpose_type',
                                    choices=PURPOSE_CHOICES,
                                    method='filter_purposes',
                                    label='Тип назначения',
                                    empty_label='Выберите тип назначения')

    product_types = filters.CharFilter(field_name='product_types__name',
                                      lookup_expr='icontains',
                                      label='Вид товара',
                                      method='filter_product_types')

    volumes = filters.CharFilter(field_name='volumes__name',
                                 lookup_expr='icontains',
                                 label='Объем',
                                 method='filter_volumes')

    indications = filters.CharFilter(field_name='indications__name',
                                     lookup_expr='icontains',
                                     label='Показание',
                                     method='filter_indications')

    dosage_forms = filters.CharFilter(field_name='dosage_forms__name',
                                     lookup_expr='icontains',
                                     label='Форма выпуска',
                                     method='filter_dosage_forms')

    name = filters.CharFilter(field_name='name',
                              lookup_expr='icontains',
                              label='Название продукта')

    def filter_purposes(self, queryset, name, value):
        return queryset.filter(purposes__purpose_type=value)

    def filter_product_types(self, queryset, name, value):
        return queryset.filter(product_types__name__icontains=value)

    def filter_volumes(self, queryset, name, value):
        return queryset.filter(volumes__name__icontains=value)

    def filter_indications(self, queryset, name, value):
        return queryset.filter(indications__name__icontains=value)

    def filter_dosage_forms(self, queryset, name, value):
        return queryset.filter(dosage_forms__name__icontains=value)

    class Meta:
        model = Product
        fields = ['purposes', 'product_types', 'volumes', 'indications', 'dosage_forms']
