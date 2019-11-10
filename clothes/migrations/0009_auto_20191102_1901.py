# Generated by Django 2.2.6 on 2019-11-02 19:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crawling', '0001_initial'),
        ('clothes', '0008_auto_20191102_1758'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='feature',
        ),
        migrations.AddField(
            model_name='product',
            name='feature',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='crawling.Category'),
        ),
    ]