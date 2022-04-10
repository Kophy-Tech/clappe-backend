# Generated by Django 3.2.9 on 2022-04-10 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_auto_20220410_1717'),
    ]

    operations = [
        migrations.AlterField(
            model_name='creditnote',
            name='cn_number',
            field=models.CharField(max_length=2048, verbose_name='Credit Note number'),
        ),
        migrations.AlterField(
            model_name='creditnote',
            name='po_number',
            field=models.CharField(max_length=2048, verbose_name='PO number'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='invoice_number',
            field=models.CharField(blank=True, default=1, max_length=2048, null=True, verbose_name='Invoice Number'),
        ),
        migrations.AlterField(
            model_name='deliverynote',
            name='dn_number',
            field=models.CharField(max_length=2048, verbose_name='Delivery Note number'),
        ),
        migrations.AlterField(
            model_name='deliverynote',
            name='po_number',
            field=models.CharField(max_length=2048, verbose_name='PO number'),
        ),
        migrations.AlterField(
            model_name='estimate',
            name='estimate_number',
            field=models.CharField(max_length=2048, verbose_name='Estimate number'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_number',
            field=models.CharField(max_length=2048, verbose_name='Invoice number'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='po_number',
            field=models.CharField(max_length=2048, verbose_name='PO number'),
        ),
        migrations.AlterField(
            model_name='proformainvoice',
            name='invoice_number',
            field=models.CharField(max_length=2048, verbose_name='Invoice number'),
        ),
        migrations.AlterField(
            model_name='proformainvoice',
            name='po_number',
            field=models.CharField(max_length=2048, verbose_name='PO number'),
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='po_number',
            field=models.CharField(max_length=2048, verbose_name='PO number'),
        ),
        migrations.AlterField(
            model_name='quote',
            name='po_number',
            field=models.CharField(max_length=2048, verbose_name='PO number'),
        ),
        migrations.AlterField(
            model_name='quote',
            name='quote_number',
            field=models.CharField(max_length=2048, verbose_name='Quote number'),
        ),
        migrations.AlterField(
            model_name='receipt',
            name='po_number',
            field=models.CharField(max_length=2048, verbose_name='PO number'),
        ),
        migrations.AlterField(
            model_name='receipt',
            name='receipt_number',
            field=models.CharField(max_length=2048, verbose_name='Receipt number'),
        ),
    ]