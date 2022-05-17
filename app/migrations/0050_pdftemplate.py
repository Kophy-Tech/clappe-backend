# Generated by Django 3.2.9 on 2022-05-15 16:19

import cloudinary.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0049_auto_20220507_1330'),
    ]

    operations = [
        migrations.CreateModel(
            name='PDFTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1024, verbose_name='Name')),
                ('photo_path', cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='PDF Photo')),
            ],
        ),
    ]
