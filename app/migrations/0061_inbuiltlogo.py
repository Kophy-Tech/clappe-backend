# Generated by Django 3.2.9 on 2022-06-07 15:52

import cloudinary.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0060_auto_20220602_1541'),
    ]

    operations = [
        migrations.CreateModel(
            name='InbuiltLogo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1024, unique=True, verbose_name='Name')),
                ('photo_path', cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='Photo')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
    ]
