# Generated by Django 3.2.9 on 2022-05-21 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0052_auto_20220521_1531'),
    ]

    operations = [
        migrations.AddField(
            model_name='creditnote',
            name='bill_to',
            field=models.CharField(blank=True, default='', max_length=2048, null=True, verbose_name='Bill To'),
        ),
        migrations.AddField(
            model_name='creditnote',
            name='billing_address',
            field=models.CharField(blank=True, default='', max_length=500, null=True, verbose_name='Billing Address'),
        ),
        migrations.AddField(
            model_name='deliverynote',
            name='bill_to',
            field=models.CharField(blank=True, default='', max_length=2048, null=True, verbose_name='Bill To'),
        ),
        migrations.AddField(
            model_name='deliverynote',
            name='billing_address',
            field=models.CharField(blank=True, default='', max_length=500, null=True, verbose_name='Billing Address'),
        ),
        migrations.AddField(
            model_name='proformainvoice',
            name='bill_to',
            field=models.CharField(blank=True, default='', max_length=2048, null=True, verbose_name='Bill To'),
        ),
        migrations.AddField(
            model_name='proformainvoice',
            name='billing_address',
            field=models.CharField(blank=True, default='', max_length=500, null=True, verbose_name='Billing Address'),
        ),
        migrations.AddField(
            model_name='proformainvoice',
            name='ship_to',
            field=models.CharField(blank=True, default='', max_length=500, null=True, verbose_name='Ship to'),
        ),
        migrations.AddField(
            model_name='proformainvoice',
            name='shipping_address',
            field=models.CharField(blank=True, default='', max_length=500, null=True, verbose_name='Shipping Address'),
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='bill_to',
            field=models.CharField(blank=True, default='', max_length=2048, null=True, verbose_name='Bill To'),
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='billing_address',
            field=models.CharField(blank=True, default='', max_length=500, null=True, verbose_name='Billing Address'),
        ),
        migrations.AlterField(
            model_name='creditnote',
            name='ship_to',
            field=models.CharField(blank=True, default='', max_length=500, null=True, verbose_name='Ship to'),
        ),
        migrations.AlterField(
            model_name='creditnote',
            name='shipping_address',
            field=models.CharField(blank=True, default='', max_length=500, null=True, verbose_name='Shipping Address'),
        ),
        migrations.AlterField(
            model_name='deliverynote',
            name='ship_to',
            field=models.CharField(blank=True, default='', max_length=500, null=True, verbose_name='Ship to'),
        ),
        migrations.AlterField(
            model_name='deliverynote',
            name='shipping_address',
            field=models.CharField(blank=True, default='', max_length=500, null=True, verbose_name='Shipping Address'),
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='ship_to',
            field=models.CharField(blank=True, default='', max_length=500, null=True, verbose_name='Ship to'),
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='shipping_address',
            field=models.CharField(blank=True, default='', max_length=500, null=True, verbose_name='Shipping Address'),
        ),
    ]
