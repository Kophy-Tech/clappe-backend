# Generated by Django 3.2.9 on 2022-05-28 08:45

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0054_alter_proformainvoice_po_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorder',
            name='due_date',
            field=models.DateField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='Due Date'),
        ),
    ]
