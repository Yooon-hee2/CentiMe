# Generated by Django 2.2.6 on 2019-11-02 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clothes', '0006_auto_20191102_1733'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='user',
        ),
        migrations.AlterField(
            model_name='product',
            name='fit',
            field=models.CharField(default='보통', max_length=5),
        ),
    ]
