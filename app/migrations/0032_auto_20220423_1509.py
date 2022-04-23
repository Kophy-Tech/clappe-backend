# Generated by Django 3.2.9 on 2022-04-23 14:09

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0031_auto_20220423_1309'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='creditnote',
            name='cn_pref',
        ),
        migrations.RemoveField(
            model_name='creditnote',
            name='taxable',
        ),
        migrations.RemoveField(
            model_name='deliverynote',
            name='dn_pref',
        ),
        migrations.RemoveField(
            model_name='deliverynote',
            name='taxable',
        ),
        migrations.RemoveField(
            model_name='estimate',
            name='estimate_pref',
        ),
        migrations.RemoveField(
            model_name='estimate',
            name='taxable',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='invoice_pref',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='taxable',
        ),
        migrations.RemoveField(
            model_name='proformainvoice',
            name='invoice_pref',
        ),
        migrations.RemoveField(
            model_name='proformainvoice',
            name='taxable',
        ),
        migrations.RemoveField(
            model_name='purchaseorder',
            name='po_pref',
        ),
        migrations.RemoveField(
            model_name='purchaseorder',
            name='taxable',
        ),
        migrations.RemoveField(
            model_name='quote',
            name='quote_pref',
        ),
        migrations.RemoveField(
            model_name='quote',
            name='taxable',
        ),
        migrations.RemoveField(
            model_name='receipt',
            name='receipt_pref',
        ),
        migrations.RemoveField(
            model_name='receipt',
            name='taxable',
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='due_date',
            field=models.DateField(default=datetime.datetime(2022, 4, 23, 14, 9, 30, 374982, tzinfo=utc), verbose_name='Due Date'),
        ),
        migrations.AlterField(
            model_name='quote',
            name='due_date',
            field=models.DateField(default=datetime.datetime(2022, 4, 23, 14, 9, 30, 374982, tzinfo=utc), verbose_name='Due Date'),
        ),
    ]