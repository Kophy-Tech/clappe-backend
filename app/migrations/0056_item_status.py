# Generated by Django 3.2.9 on 2022-05-28 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0055_auto_20220528_0945'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='status',
            field=models.CharField(blank=True, default='New', max_length=64, null=True, verbose_name='Status'),
        ),
    ]
