# Generated by Django 3.0.3 on 2020-02-04 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_product_ingridients'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='drying_method',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='product',
            name='drying_time',
            field=models.IntegerField(blank=True),
        ),
    ]