# Generated by Django 3.2.9 on 2022-04-28 22:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0040_auto_20220428_2229'),
    ]

    operations = [
        migrations.AddField(
            model_name='myusers',
            name='password_recovery',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
