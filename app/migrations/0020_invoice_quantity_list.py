# Generated by Django 3.2.9 on 2022-04-12 19:12

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_auto_20220412_1820'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='quantity_list',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.PositiveIntegerField(blank=True), default=list, size=None),
        ),
    ]
