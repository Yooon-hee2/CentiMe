# Generated by Django 2.2.6 on 2019-11-02 07:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clothes', '0004_auto_20191102_0731'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['-id']},
        ),
    ]