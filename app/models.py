from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.




class MyUsers(AbstractUser):
    email = models.EmailField("Email", max_length=100, unique=True)
    phone_number = models.CharField("Phone number", max_length=24, null=True, blank=True)
    name_of_business = models.CharField("Name of business", max_length=500, null=True, blank=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name





class Customer(models.Model):
    first_name = models.CharField("First Name", max_length=50, blank=False, null=False)
    last_name = models.CharField("Last Name", max_length=50, blank=False, null=False)
    business_name = models.CharField("Business Name", max_length=70, null=False, blank=False)
    address = models.CharField("Address", max_length=500, null=False, blank=False)
    email = models.EmailField("Email", max_length=50, null=False, blank=False, unique=True)
    phone_number = models.CharField("Phone Number", max_length=15, null=False, blank=False, unique=True)
    taxable = models.BooleanField("Taxable", default=False, null=False, blank=False)
    invoice_pref = models.CharField("Invoice Preference", max_length=15, blank=False, null=False)
    logo_path = models.CharField("Logo Path", max_length=150, null=False, blank=False)
    ship_to = models.CharField("Ship to", max_length=500, null=False, blank=False)
    shipping_address = models.CharField("Shipping Address", max_length=500, null=False, blank=False)
    billing_address = models.CharField("Billing Address", max_length=500, null=False, blank=False)
    notes = models.CharField("Notes", max_length=1024, null=True, blank=True)
    status = models.CharField("Status", max_length=20, null=True, blank=True, default="New")
    invoice_number = models.PositiveIntegerField("Invoice Number", null=True, blank=True, default=1)
    amount = models.FloatField("Amount", null=True, blank=True, default=0.00)

    vendor = models.ForeignKey(MyUsers, on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.vendor.first_name})"






class Invoice(models.Model):
    first_name = models.CharField("First Name", max_length=50, blank=False, null=False)
    last_name = models.CharField("Last Name", max_length=50, blank=False, null=False)
    address = models.CharField("Address", max_length=500, null=False, blank=False)
    email = models.EmailField("Email", max_length=50, null=False, blank=False)
    phone_number = models.CharField("Phone Number", max_length=15, null=False, blank=False)
    taxable = models.BooleanField("Taxable", default=False, null=False, blank=False)
    invoice_pref = models.CharField("Invoice Preference", max_length=15, blank=False, null=False)
    theme = models.CharField("Logo Path", max_length=150, null=False, blank=False)
    invoice_number = models.PositiveIntegerField("Invoice number", blank=False, null=False)
    invoice_date = models.DateField("Invoice Date", blank=False, null=False)
    po_number = models.PositiveIntegerField("PO number", blank=False, null=False)
    due_date = models.DateField("Due Date", blank=False, null=False)
    ship_to = models.CharField("Ship to", max_length=500, null=False, blank=False)
    shipping_address = models.CharField("Shipping Address", max_length=500, null=False, blank=False)
    bill_to = models.CharField("Bill To", max_length=2048, blank=False, null=False)
    billing_address = models.CharField("Billing Address", max_length=500, null=False, blank=False)
    notes = models.CharField("Notes", max_length=1024, null=True, blank=True)
    
    items_json = models.JSONField("Items Json", blank=False, null=False, default=dict)
    item_total = models.FloatField("Item Total", blank=False, null=False)
    tax = models.FloatField("Tax", blank=True, null=True)
    add_charges = models.FloatField("Additional Charges", blank=True, null=True)
    sub_total = models.FloatField("Sub-Total", blank=False, null=False)
    discount_type = models.CharField("Discount Type", max_length=1024, blank=False, null=False)
    discount_amount = models.FloatField("Discount Amount", blank=False, null=False)
    grand_total = models.FloatField("Grand Total", blank=False, null=False)

    status = models.CharField("Status", max_length=20, blank=True, null=True, default='New')

    vendor = models.ForeignKey(MyUsers, on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.vendor.first_name})"    






class ProformaInvoice(models.Model):
    first_name = models.CharField("First Name", max_length=50, blank=False, null=False)
    last_name = models.CharField("Last Name", max_length=50, blank=False, null=False)
    address = models.CharField("Address", max_length=500, null=False, blank=False)
    email = models.EmailField("Email", max_length=50, null=False, blank=False)
    phone_number = models.CharField("Phone Number", max_length=15, null=False, blank=False)
    taxable = models.BooleanField("Taxable", default=False, null=False, blank=False)
    invoice_pref = models.CharField("Invoice Preference", max_length=15, blank=False, null=False)
    theme = models.CharField("Logo Path", max_length=150, null=False, blank=False)
    invoice_number = models.PositiveIntegerField("Invoice number", blank=False, null=False)
    invoice_date = models.DateField("Invoice Date", blank=False, null=False)
    po_number = models.PositiveIntegerField("PO number", blank=False, null=False)
    due_date = models.DateField("Due Date", blank=False, null=False)
    notes = models.CharField("Notes", max_length=1024, null=True, blank=True)
    attachment_path = models.CharField("Attachment Path", max_length=2048, blank=True, null=True)
    
    items_json = models.JSONField("Items Json", blank=False, null=False, default=dict)
    item_total = models.FloatField("Item Total", blank=False, null=False)
    tax = models.FloatField("Tax", blank=True, null=True)
    add_charges = models.FloatField("Additional Charges", blank=True, null=True)
    grand_total = models.FloatField("Grand Total", blank=False, null=False)

    status = models.CharField("Status", max_length=20, blank=True, null=True, default='New')
    vendor = models.ForeignKey(MyUsers, on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.vendor.first_name})"  







class PurchaseOrder(models.Model):
    first_name = models.CharField("First Name", max_length=50, blank=False, null=False)
    last_name = models.CharField("Last Name", max_length=50, blank=False, null=False)
    address = models.CharField("Address", max_length=500, null=False, blank=False)
    email = models.EmailField("Email", max_length=50, null=False, blank=False)
    phone_number = models.CharField("Phone Number", max_length=15, null=False, blank=False)
    taxable = models.BooleanField("Taxable", default=False, null=False, blank=False)
    po_pref = models.CharField("Invoice Preference", max_length=15, blank=False, null=False)
    theme = models.CharField("Logo Path", max_length=150, null=False, blank=False)

    po_number = models.PositiveIntegerField("PO number", blank=False, null=False)
    po_date = models.DateField("Purchase Order Date", blank=False, null=False)
    ship_to = models.CharField("Ship to", max_length=500, null=False, blank=False)
    shipping_address = models.CharField("Shipping Address", max_length=500, null=False, blank=False)
    notes = models.CharField("Notes", max_length=1024, null=True, blank=True)

    
    items_json = models.JSONField("Items Json", blank=False, null=False, default=dict)
    item_total = models.FloatField("Item Total", blank=False, null=False)
    tax = models.FloatField("Tax", blank=True, null=True)
    add_charges = models.FloatField("Additional Charges", blank=True, null=True)
    grand_total = models.FloatField("Grand Total", blank=False, null=False)

    status = models.CharField("Status", max_length=20, blank=True, null=True, default='New')
    vendor = models.ForeignKey(MyUsers, on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.vendor.first_name})"






class Estimate(models.Model):
    first_name = models.CharField("First Name", max_length=50, blank=False, null=False)
    last_name = models.CharField("Last Name", max_length=50, blank=False, null=False)
    address = models.CharField("Address", max_length=500, null=False, blank=False)
    email = models.EmailField("Email", max_length=50, null=False, blank=False)
    phone_number = models.CharField("Phone Number", max_length=15, null=False, blank=False)
    taxable = models.BooleanField("Taxable", default=False, null=False, blank=False)
    estimate_pref = models.CharField("Estimate Preference", max_length=15, blank=False, null=False, default="a")
    logo_path = models.CharField("Logo Path", max_length=150, null=False, blank=False)

    estimate_number = models.PositiveIntegerField("Estimate number", blank=False, null=False)
    estimate_date = models.DateField("Estimate Date", blank=False, null=False)

    ship_to = models.CharField("Ship to", max_length=500, null=False, blank=False)
    shipping_address = models.CharField("Shipping Address", max_length=500, null=False, blank=False)
    bill_to = models.CharField("Bill To", max_length=2048, blank=False, null=False)
    billing_address = models.CharField("Billing Address", max_length=500, null=False, blank=False)
    notes = models.CharField("Notes", max_length=1024, null=True, blank=True)
    
    items_json = models.JSONField("Items Json", blank=False, null=False, default=dict)
    item_total = models.FloatField("Item Total", blank=False, null=False)
    tax = models.FloatField("Tax", blank=True, null=True)
    add_charges = models.FloatField("Additional Charges", blank=True, null=True)
    grand_total = models.FloatField("Grand Total", blank=False, null=False)

    status = models.CharField("Status", max_length=20, blank=True, null=True, default='New')
    vendor = models.ForeignKey(MyUsers, on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.vendor.first_name})"







class PayInvoice(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    payment_type = models.CharField("Payment Type", max_length=1024, blank=False, null=False)
    paid_date = models.DateField("Paid Date", blank=False, null=False)
    paid_amount = models.FloatField("Paid Amount", blank=False, null=False)
    payment_method = models.CharField("Payment Method", max_length=1024, blank=False, null=False)
    reference = models.CharField("Reference", max_length=1024, blank=False, null=False)


    def __str__(self):
        return self.invoice.first_name + self.invoice.last_name



class PayProforma(models.Model):
    proforma = models.ForeignKey(ProformaInvoice, on_delete=models.CASCADE)
    payment_type = models.CharField("Payment Type", max_length=1024, blank=False, null=False)
    paid_date = models.DateField("Paid Date", blank=False, null=False)
    paid_amount = models.FloatField("Paid Amount", blank=False, null=False)
    payment_method = models.CharField("Payment Method", max_length=1024, blank=False, null=False)
    reference = models.CharField("Reference", max_length=1024, blank=False, null=False)


    def __str__(self):
        return self.proforma.first_name + self.proforma.last_name



class PayPurchaseOrder(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    payment_type = models.CharField("Payment Type", max_length=1024, blank=False, null=False)
    paid_date = models.DateField("Paid Date", blank=False, null=False)
    paid_amount = models.FloatField("Paid Amount", blank=False, null=False)
    payment_method = models.CharField("Payment Method", max_length=1024, blank=False, null=False)
    reference = models.CharField("Reference", max_length=1024, blank=False, null=False)


    def __str__(self):
        return self.purchase_order.first_name + self.purchase_order.last_name



class PayEstimate(models.Model):
    estimate = models.ForeignKey(Estimate, on_delete=models.CASCADE)
    payment_type = models.CharField("Payment Type", max_length=1024, blank=False, null=False)
    paid_date = models.DateField("Paid Date", blank=False, null=False)
    paid_amount = models.FloatField("Paid Amount", blank=False, null=False)
    payment_method = models.CharField("Payment Method", max_length=1024, blank=False, null=False)
    reference = models.CharField("Reference", max_length=1024, blank=False, null=False)


    def __str__(self):
        return self.estimate.first_name + self.proforma.last_name



















class Item(models.Model):
    name = models.CharField("Name", max_length=1024, blank=False, null=False, unique=False)
    description = models.CharField("Item Description", max_length=2048, blank=True, null=True)
    cost_price = models.FloatField("Cost Price", blank=False, null=False)
    sales_price = models.FloatField("Sales Price", blank=False, null=False)
    sales_tex = models.FloatField("Sales Tex", blank=False, null=False)


    def __str__(self):
        return self.name


















class JWT(models.Model):
    user = models.OneToOneField(MyUsers, on_delete=models.CASCADE)
    access = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-user']

    def __str__(self):
        return self.user.email
