# Generated by Django 3.2.9 on 2022-04-26 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0035_auto_20220425_1804'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='sku',
            field=models.CharField(blank=True, max_length=15, null=True, unique=True, verbose_name='SKU'),
        ),
    ]