# Generated by Django 2.2.6 on 2019-11-29 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clothes', '0011_product_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='thumbnail',
            field=models.TextField(blank=True, null=True),
        ),
    ]
