# Generated by Django 2.2.6 on 2019-11-02 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawling', '0001_initial'),
        ('clothes', '0005_auto_20191102_0740'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='feature',
        ),
        migrations.AddField(
            model_name='product',
            name='feature',
            field=models.ManyToManyField(to='crawling.Category'),
        ),
    ]
