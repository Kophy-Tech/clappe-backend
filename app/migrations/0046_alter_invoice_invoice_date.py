# Generated by Django 3.2.9 on 2022-05-01 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0045_alter_invoice_invoice_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='invoice_date',
            field=models.DateField(error_messages={'blank': 'Invoice date is required', 'invalid': 'Invoice date is required'}, verbose_name='Invoice Date'),
        ),
    ]
