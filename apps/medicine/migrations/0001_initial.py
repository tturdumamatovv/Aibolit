# Generated by Django 5.0.6 on 2024-06-22 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.IntegerField(unique=True)),
                ('name', models.CharField(max_length=255)),
                ('sklad', models.CharField(max_length=255)),
                ('ostatok', models.IntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('manufacturer', models.CharField(blank=True, max_length=255, null=True)),
                ('country', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
    ]
