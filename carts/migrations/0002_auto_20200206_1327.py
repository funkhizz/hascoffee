# Generated by Django 3.0.3 on 2020-02-06 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
        ('carts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='products',
            field=models.ManyToManyField(blank=True, to='products.Product'),
        ),
    ]
