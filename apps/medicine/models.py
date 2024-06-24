from django.db import models


class Category(models.Model):
    code = models.IntegerField(unique=True)
    parent_code = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=255)
    folder = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Product(models.Model):
    code = models.IntegerField(unique=True)
    name = models.CharField(max_length=255)
    sklad = models.CharField(max_length=255)
    ostatok = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    manufacturer = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name
