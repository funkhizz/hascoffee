# Generated by Django 3.0.3 on 2020-02-06 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0003_cartitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='line_total',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=100),
        ),
    ]