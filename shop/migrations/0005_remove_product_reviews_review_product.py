# Generated by Django 5.2 on 2025-04-13 09:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_remove_product_reviews_product_reviews'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='reviews',
        ),
        migrations.AddField(
            model_name='review',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='shop.product'),
        ),
    ]
