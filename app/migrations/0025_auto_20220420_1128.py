# Generated by Django 3.2.9 on 2022-04-20 10:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0024_auto_20220419_1739'),
    ]

    operations = [
        migrations.AddField(
            model_name='estimate',
            name='po_number',
            field=models.CharField(default=1, max_length=1024, verbose_name='PO Number'),
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='due_date',
            field=models.DateField(default=datetime.datetime(2022, 4, 20, 11, 27, 59, 95716), verbose_name='Due Date'),
        ),
    ]