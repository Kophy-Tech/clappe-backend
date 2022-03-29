# Generated by Django 3.2.9 on 2022-03-29 16:25

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyUsers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(blank=True, max_length=1024, null=True, verbose_name='Username')),
                ('email', models.EmailField(max_length=100, unique=True, verbose_name='Email')),
                ('phone_number', models.CharField(blank=True, max_length=24, null=True, verbose_name='Phone number')),
                ('name_of_business', models.CharField(blank=True, max_length=500, null=True, verbose_name='Name of business')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Estimate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50, verbose_name='First Name')),
                ('last_name', models.CharField(max_length=50, verbose_name='Last Name')),
                ('address', models.CharField(max_length=500, verbose_name='Address')),
                ('email', models.EmailField(max_length=50, verbose_name='Email')),
                ('phone_number', models.CharField(max_length=15, verbose_name='Phone Number')),
                ('taxable', models.BooleanField(default=False, verbose_name='Taxable')),
                ('estimate_pref', models.CharField(default='a', max_length=15, verbose_name='Estimate Preference')),
                ('logo_path', models.CharField(max_length=150, verbose_name='Logo Path')),
                ('estimate_number', models.PositiveIntegerField(verbose_name='Estimate number')),
                ('estimate_date', models.DateField(verbose_name='Estimate Date')),
                ('ship_to', models.CharField(max_length=500, verbose_name='Ship to')),
                ('shipping_address', models.CharField(max_length=500, verbose_name='Shipping Address')),
                ('bill_to', models.CharField(max_length=2048, verbose_name='Bill To')),
                ('billing_address', models.CharField(max_length=500, verbose_name='Billing Address')),
                ('notes', models.CharField(blank=True, max_length=1024, null=True, verbose_name='Notes')),
                ('items_json', models.JSONField(default=dict, verbose_name='Items Json')),
                ('item_total', models.FloatField(verbose_name='Item Total')),
                ('tax', models.FloatField(blank=True, null=True, verbose_name='Tax')),
                ('add_charges', models.FloatField(blank=True, null=True, verbose_name='Additional Charges')),
                ('grand_total', models.FloatField(verbose_name='Grand Total')),
                ('status', models.CharField(blank=True, default='New', max_length=20, null=True, verbose_name='Status')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50, verbose_name='First Name')),
                ('last_name', models.CharField(max_length=50, verbose_name='Last Name')),
                ('address', models.CharField(max_length=500, verbose_name='Address')),
                ('email', models.EmailField(max_length=50, verbose_name='Email')),
                ('phone_number', models.CharField(max_length=15, verbose_name='Phone Number')),
                ('taxable', models.BooleanField(default=False, verbose_name='Taxable')),
                ('invoice_pref', models.CharField(max_length=15, verbose_name='Invoice Preference')),
                ('theme', models.CharField(max_length=150, verbose_name='Logo Path')),
                ('invoice_number', models.PositiveIntegerField(verbose_name='Invoice number')),
                ('invoice_date', models.DateField(verbose_name='Invoice Date')),
                ('po_number', models.PositiveIntegerField(verbose_name='PO number')),
                ('due_date', models.DateField(verbose_name='Due Date')),
                ('ship_to', models.CharField(max_length=500, verbose_name='Ship to')),
                ('shipping_address', models.CharField(max_length=500, verbose_name='Shipping Address')),
                ('bill_to', models.CharField(max_length=2048, verbose_name='Bill To')),
                ('billing_address', models.CharField(max_length=500, verbose_name='Billing Address')),
                ('notes', models.CharField(blank=True, max_length=1024, null=True, verbose_name='Notes')),
                ('items_json', models.JSONField(default=dict, verbose_name='Items Json')),
                ('item_total', models.FloatField(verbose_name='Item Total')),
                ('tax', models.FloatField(blank=True, null=True, verbose_name='Tax')),
                ('add_charges', models.FloatField(blank=True, null=True, verbose_name='Additional Charges')),
                ('sub_total', models.FloatField(verbose_name='Sub-Total')),
                ('discount_type', models.CharField(max_length=1024, verbose_name='Discount Type')),
                ('discount_amount', models.FloatField(verbose_name='Discount Amount')),
                ('grand_total', models.FloatField(verbose_name='Grand Total')),
                ('status', models.CharField(blank=True, default='New', max_length=20, null=True, verbose_name='Status')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1024, verbose_name='Name')),
                ('description', models.CharField(blank=True, max_length=2048, null=True, verbose_name='Item Description')),
                ('cost_price', models.FloatField(verbose_name='Cost Price')),
                ('sales_price', models.FloatField(verbose_name='Sales Price')),
                ('sales_tex', models.FloatField(verbose_name='Sales Tex')),
            ],
        ),
        migrations.CreateModel(
            name='PurchaseOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50, verbose_name='First Name')),
                ('last_name', models.CharField(max_length=50, verbose_name='Last Name')),
                ('address', models.CharField(max_length=500, verbose_name='Address')),
                ('email', models.EmailField(max_length=50, verbose_name='Email')),
                ('phone_number', models.CharField(max_length=15, verbose_name='Phone Number')),
                ('taxable', models.BooleanField(default=False, verbose_name='Taxable')),
                ('po_pref', models.CharField(max_length=15, verbose_name='Invoice Preference')),
                ('theme', models.CharField(max_length=150, verbose_name='Logo Path')),
                ('po_number', models.PositiveIntegerField(verbose_name='PO number')),
                ('po_date', models.DateField(verbose_name='Purchase Order Date')),
                ('ship_to', models.CharField(max_length=500, verbose_name='Ship to')),
                ('shipping_address', models.CharField(max_length=500, verbose_name='Shipping Address')),
                ('notes', models.CharField(blank=True, max_length=1024, null=True, verbose_name='Notes')),
                ('items_json', models.JSONField(default=dict, verbose_name='Items Json')),
                ('item_total', models.FloatField(verbose_name='Item Total')),
                ('tax', models.FloatField(blank=True, null=True, verbose_name='Tax')),
                ('add_charges', models.FloatField(blank=True, null=True, verbose_name='Additional Charges')),
                ('grand_total', models.FloatField(verbose_name='Grand Total')),
                ('status', models.CharField(blank=True, default='New', max_length=20, null=True, verbose_name='Status')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProformaInvoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50, verbose_name='First Name')),
                ('last_name', models.CharField(max_length=50, verbose_name='Last Name')),
                ('address', models.CharField(max_length=500, verbose_name='Address')),
                ('email', models.EmailField(max_length=50, verbose_name='Email')),
                ('phone_number', models.CharField(max_length=15, verbose_name='Phone Number')),
                ('taxable', models.BooleanField(default=False, verbose_name='Taxable')),
                ('invoice_pref', models.CharField(max_length=15, verbose_name='Invoice Preference')),
                ('theme', models.CharField(max_length=150, verbose_name='Logo Path')),
                ('invoice_number', models.PositiveIntegerField(verbose_name='Invoice number')),
                ('invoice_date', models.DateField(verbose_name='Invoice Date')),
                ('po_number', models.PositiveIntegerField(verbose_name='PO number')),
                ('due_date', models.DateField(verbose_name='Due Date')),
                ('notes', models.CharField(blank=True, max_length=1024, null=True, verbose_name='Notes')),
                ('attachment_path', models.CharField(blank=True, max_length=2048, null=True, verbose_name='Attachment Path')),
                ('items_json', models.JSONField(default=dict, verbose_name='Items Json')),
                ('item_total', models.FloatField(verbose_name='Item Total')),
                ('tax', models.FloatField(blank=True, null=True, verbose_name='Tax')),
                ('add_charges', models.FloatField(blank=True, null=True, verbose_name='Additional Charges')),
                ('grand_total', models.FloatField(verbose_name='Grand Total')),
                ('status', models.CharField(blank=True, default='New', max_length=20, null=True, verbose_name='Status')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PayPurchaseOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_type', models.CharField(max_length=1024, verbose_name='Payment Type')),
                ('paid_date', models.DateField(verbose_name='Paid Date')),
                ('paid_amount', models.FloatField(verbose_name='Paid Amount')),
                ('payment_method', models.CharField(max_length=1024, verbose_name='Payment Method')),
                ('reference', models.CharField(max_length=1024, verbose_name='Reference')),
                ('purchase_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.purchaseorder')),
            ],
        ),
        migrations.CreateModel(
            name='PayProforma',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_type', models.CharField(max_length=1024, verbose_name='Payment Type')),
                ('paid_date', models.DateField(verbose_name='Paid Date')),
                ('paid_amount', models.FloatField(verbose_name='Paid Amount')),
                ('payment_method', models.CharField(max_length=1024, verbose_name='Payment Method')),
                ('reference', models.CharField(max_length=1024, verbose_name='Reference')),
                ('proforma', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.proformainvoice')),
            ],
        ),
        migrations.CreateModel(
            name='PayInvoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_type', models.CharField(max_length=1024, verbose_name='Payment Type')),
                ('paid_date', models.DateField(verbose_name='Paid Date')),
                ('paid_amount', models.FloatField(verbose_name='Paid Amount')),
                ('payment_method', models.CharField(max_length=1024, verbose_name='Payment Method')),
                ('reference', models.CharField(max_length=1024, verbose_name='Reference')),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.invoice')),
            ],
        ),
        migrations.CreateModel(
            name='PayEstimate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_type', models.CharField(max_length=1024, verbose_name='Payment Type')),
                ('paid_date', models.DateField(verbose_name='Paid Date')),
                ('paid_amount', models.FloatField(verbose_name='Paid Amount')),
                ('payment_method', models.CharField(max_length=1024, verbose_name='Payment Method')),
                ('reference', models.CharField(max_length=1024, verbose_name='Reference')),
                ('estimate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.estimate')),
            ],
        ),
        migrations.CreateModel(
            name='JWT',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-user'],
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50, verbose_name='First Name')),
                ('last_name', models.CharField(max_length=50, verbose_name='Last Name')),
                ('business_name', models.CharField(max_length=70, verbose_name='Business Name')),
                ('address', models.CharField(max_length=500, verbose_name='Address')),
                ('email', models.EmailField(max_length=50, unique=True, verbose_name='Email')),
                ('phone_number', models.CharField(max_length=15, unique=True, verbose_name='Phone Number')),
                ('taxable', models.BooleanField(default=False, verbose_name='Taxable')),
                ('invoice_pref', models.CharField(max_length=15, verbose_name='Invoice Preference')),
                ('logo_path', models.CharField(max_length=150, verbose_name='Logo Path')),
                ('ship_to', models.CharField(max_length=500, verbose_name='Ship to')),
                ('shipping_address', models.CharField(max_length=500, verbose_name='Shipping Address')),
                ('billing_address', models.CharField(max_length=500, verbose_name='Billing Address')),
                ('notes', models.CharField(blank=True, max_length=1024, null=True, verbose_name='Notes')),
                ('status', models.CharField(blank=True, default='New', max_length=20, null=True, verbose_name='Status')),
                ('invoice_number', models.PositiveIntegerField(blank=True, default=1, null=True, verbose_name='Invoice Number')),
                ('amount', models.FloatField(blank=True, default=0.0, null=True, verbose_name='Amount')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
