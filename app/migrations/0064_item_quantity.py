# Generated by Django 3.2.9 on 2022-08-06 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0063_rename_pdf_template_customer_pdf_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='quantity',
            field=models.CharField(blank=True, default=True, max_length=1024, null=True),
        ),
    ]
