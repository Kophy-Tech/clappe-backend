from django.utils import timezone
from django.db import models
from django.utils.safestring import mark_safe
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from cloudinary.models import CloudinaryField


# Create your models here.




class MyUsers(AbstractUser):
    username = models.CharField("Username", max_length=1024, null=True, unique=False, blank=True)
    photo_path = CloudinaryField("Profile Photo", null=True, blank=True)
    logo_path = CloudinaryField("Logo Image", null=True,blank=True)
    signature = CloudinaryField("Signature", null=True, blank=True)
    email = models.EmailField("Email", max_length=100, unique=True)
    address = models.CharField("Address", max_length=2048, null=True, blank=True, default="None")
    phone_number = models.CharField("Phone number", max_length=24, null=True, blank=True)
    phone_number_type = models.CharField("Type of phone number", max_length=24, null=False, blank=False, default="Mobile")
    business_name = models.CharField("Name of business", max_length=500, null=True, blank=True)
    other_phone_number = models.CharField("Other phone number", max_length=24, null=True, blank=True)
    fax = models.CharField("Fax", max_length=24, null=True, blank=True)
    business_number = models.CharField("Business Number", max_length=50, null=True, blank=True)
    tax_type = models.CharField("Tax Type", max_length=24, null=False, blank=False, default="On Total")
    tax_rate = models.FloatField("Tax Rate", null=False, blank=False, default=0.0)
    lang_pref = models.CharField("Language Preference", max_length=50, null=True, blank=True, default="English")
    region = models.CharField("Region", max_length=100, null=True, blank=True, default="US")
    email_report = models.CharField("Email Reports", max_length=100, blank=True, null=True, default="Monthly")
    currency = models.CharField("Currency", max_length=24, null=True, blank=True, default="Dollar")
    paypal = models.CharField("PayPal", max_length=100, null=True, blank=True)
    bank_transfer = models.CharField("Bank Transfer", max_length=100, null=True, blank=True)
    e_transfer = models.CharField("E-Transfer", max_length=100, null=True, blank=True)
    other_payment = models.CharField("Other Payment", max_length=100, null=True, blank=True)

    password_recovery = models.CharField(max_length=15, null=True, blank=True)
    password_recovery_time = models.DateTimeField(null=True, blank=True)



    # USERNAME_FIELD = "email"


    def __str__(self):
        return self.first_name + ' ' + self.last_name + '-' 





class Customer(models.Model):
    first_name = models.CharField("First Name", max_length=50, blank=False, null=False)
    last_name = models.CharField("Last Name", max_length=50, blank=False, null=False)
    business_name = models.CharField("Business Name", max_length=70, null=True, blank=True)
    address = models.CharField("Address", max_length=500, null=False, blank=False)
    email = models.EmailField("Email", max_length=50, null=True, blank=True)
    phone_number = models.CharField("Phone Number", max_length=15, null=False, blank=False)
    taxable = models.BooleanField("Taxable", default=False, null=False, blank=False)
    invoice_pref = models.CharField("Invoice Preference", max_length=15, blank=False, null=False)
    logo_path = CloudinaryField("Logo photo", null=True, blank=True)
    ship_to = models.CharField("Ship to", max_length=500, null=False, blank=False)
    shipping_address = models.CharField("Shipping Address", max_length=500, null=False, blank=False)
    billing_address = models.CharField("Billing Address", max_length=500, null=False, blank=False)
    notes = models.CharField("Notes", max_length=1024, null=True, blank=True)
    status = models.CharField("Status", max_length=20, null=True, blank=True, default="New")

    vendor = models.ForeignKey(MyUsers, on_delete=models.CASCADE)

    date_created = models.DateTimeField("Date created", auto_now_add=True)
    date_modified = models.DateTimeField("Date modified", auto_now=True)


    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.vendor.business_name}"






class Invoice(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, default=1)
    emailed = models.BooleanField(default=False)
    emailed_date = models.CharField(max_length=64, blank=True, null=True)
    recurring = models.BooleanField(default=False)
    recurring_date = models.DateField(blank=True, null=True)
    recurring_data = models.JSONField(default=dict)
    


    invoice_number = models.CharField("Invoice number", blank=False, null=False, max_length=2048)
    invoice_date = models.DateField("Invoice Date", blank=False, null=False)
    po_number = models.CharField("PO number", blank=True, null=True, max_length=2048)
    due_date = models.DateField("Due Date", blank=False, null=False)
    ship_to = models.CharField("Ship to", max_length=500, null=True, blank=True)
    shipping_address = models.CharField("Shipping Address", max_length=500, null=True, blank=True)
    bill_to = models.CharField("Bill To", max_length=2048, blank=True, null=True)
    billing_address = models.CharField("Billing Address", max_length=500, null=True, blank=True)
    notes = models.CharField("Notes", max_length=1024, null=True, blank=True)
    
    item_list = ArrayField(models.PositiveIntegerField(blank=True), default=list)
    quantity_list = ArrayField(models.PositiveIntegerField(blank=True), default=list)
    item_total = models.FloatField("Item Total", blank=False, null=False)
    tax = models.CharField("Tax", blank=True, null=True, max_length=64, default="0")
    add_charges = models.CharField("Additional Charges", blank=True, null=True, max_length=64, default="0")
    sub_total = models.FloatField("Sub-Total", blank=False, null=False)
    discount_type = models.CharField("Discount Type", max_length=1024, blank=False, null=False)
    discount_amount = models.FloatField("Discount Amount", blank=False, null=False)
    grand_total = models.FloatField("Grand Total", blank=False, null=False)

    status = models.CharField("Status", max_length=20, blank=True, null=True, default='New')

    vendor = models.ForeignKey(MyUsers, on_delete=models.CASCADE)

    terms = models.CharField(max_length=5000, default="", blank=True, null=True)
    date_created = models.DateTimeField("Date created", auto_now_add=True)
    date_modified = models.DateTimeField("Date modified", auto_now=True)


    def __str__(self):
        return f"{self.customer.first_name} {self.customer.last_name} - {self.vendor.business_name}"    






class ProformaInvoice(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, default=1)
    emailed = models.BooleanField(default=False)
    emailed_date = models.CharField(max_length=64, blank=True, null=True)
    recurring = models.BooleanField(default=False)
    recurring_date = models.DateField(blank=True, null=True)
    recurring_data = models.JSONField(default=dict)
    invoice_number = models.CharField("Invoice number", blank=True, null=True, max_length=2048)
    invoice_date = models.DateField("Invoice Date", blank=False, null=False)
    po_number = models.CharField("PO number", blank=False, null=False, max_length=2048)
    due_date = models.DateField("Due Date", blank=False, null=False)
    notes = models.CharField("Notes", max_length=1024, null=True, blank=True)
    attachment_path = models.CharField("Attachment Path", max_length=2048, blank=True, null=True)
    
    item_list = ArrayField(models.PositiveIntegerField(blank=True), default=list)
    quantity_list = ArrayField(models.PositiveIntegerField(blank=True), default=list)
    item_total = models.FloatField("Item Total", blank=False, null=False)
    tax = models.CharField("Tax", blank=True, null=True, max_length=64, default="0")
    add_charges = models.CharField("Additional Charges", blank=True, null=True, max_length=64, default="0")
    grand_total = models.FloatField("Grand Total", blank=False, null=False)

    ship_to = models.CharField("Ship to", max_length=500, null=True, blank=True, default="")
    shipping_address = models.CharField("Shipping Address", max_length=500, null=True, blank=True, default="")
    bill_to = models.CharField("Bill To", max_length=2048, blank=True, null=True, default="")
    billing_address = models.CharField("Billing Address", max_length=500, null=True, blank=True, default="")

    status = models.CharField("Status", max_length=20, blank=True, null=True, default='New')
    vendor = models.ForeignKey(MyUsers, on_delete=models.CASCADE)
    terms = models.CharField(max_length=5000, default="", blank=True, null=True)
    date_created = models.DateTimeField("Date created", auto_now_add=True)
    date_modified = models.DateTimeField("Date modified", auto_now=True)


    def __str__(self):
        return f"{self.customer.first_name} {self.customer.last_name} - {self.vendor.business_name}"  







class PurchaseOrder(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, default=1)
    emailed = models.BooleanField(default=False)
    emailed_date = models.CharField(max_length=64, blank=True, null=True)
    recurring = models.BooleanField(default=False)
    recurring_date = models.DateField(blank=True, null=True)
    recurring_data = models.JSONField(default=dict)

    po_number = models.CharField("PO number", blank=True, null=True, max_length=2048)
    po_date = models.DateField("Purchase Order Date", blank=False, null=False)
    due_date = models.DateField("Due Date", blank=False, null=False, default=timezone.now)
    ship_to = models.CharField("Ship to", max_length=500, null=True, blank=True, default="")
    shipping_address = models.CharField("Shipping Address", max_length=500, null=True, blank=True, default="")
    bill_to = models.CharField("Bill To", max_length=2048, blank=True, null=True, default="")
    billing_address = models.CharField("Billing Address", max_length=500, null=True, blank=True, default="")
    notes = models.CharField("Notes", max_length=1024, null=True, blank=True)

    
    item_list = ArrayField(models.PositiveIntegerField(blank=True), default=list)
    quantity_list = ArrayField(models.PositiveIntegerField(blank=True), default=list)
    item_total = models.FloatField("Item Total", blank=False, null=False)
    tax = models.CharField("Tax", blank=True, null=True, max_length=64, default="0")
    add_charges = models.CharField("Additional Charges", blank=True, null=True, max_length=64, default="0")
    grand_total = models.FloatField("Grand Total", blank=False, null=False)

    status = models.CharField("Status", max_length=20, blank=True, null=True, default='New')
    vendor = models.ForeignKey(MyUsers, on_delete=models.CASCADE)
    terms = models.CharField(max_length=5000, default="", blank=True, null=True)
    date_created = models.DateTimeField("Date created", auto_now_add=True)
    date_modified = models.DateTimeField("Date modified", auto_now=True)


    def __str__(self):
        return f"{self.customer.first_name} {self.customer.last_name} - {self.vendor.business_name}"






class Estimate(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, default=1)
    emailed = models.BooleanField(default=False)
    emailed_date = models.CharField(max_length=64, blank=True, null=True)
    recurring = models.BooleanField(default=False)
    recurring_date = models.DateField(blank=True, null=True)
    recurring_data = models.JSONField(default=dict)    

    estimate_number = models.CharField("Estimate number", blank=False, null=False, max_length=2048)
    estimate_date = models.DateField("Estimate Date", blank=False, null=False)
    po_number = models.CharField("PO Number", blank=True, null=True, max_length=1024, default=1)
    due_date = models.DateField("Due Date", blank=False, null=False)

    ship_to = models.CharField("Ship to", max_length=500, null=True, blank=True)
    shipping_address = models.CharField("Shipping Address", max_length=500, null=True, blank=True)
    bill_to = models.CharField("Bill To", max_length=2048, blank=True, null=True)
    billing_address = models.CharField("Billing Address", max_length=500, null=True, blank=True)
    notes = models.CharField("Notes", max_length=1024, null=True, blank=True)
    
    item_list = ArrayField(models.PositiveIntegerField(blank=True), default=list)
    quantity_list = ArrayField(models.PositiveIntegerField(blank=True), default=list)
    item_total = models.FloatField("Item Total", blank=False, null=False)
    tax = models.CharField("Tax", blank=True, null=True, max_length=64, default="0")
    add_charges = models.CharField("Additional Charges", blank=True, null=True, max_length=64, default="0")
    grand_total = models.FloatField("Grand Total", blank=False, null=False)

    status = models.CharField("Status", max_length=20, blank=True, null=True, default='New')
    vendor = models.ForeignKey(MyUsers, on_delete=models.CASCADE)
    terms = models.CharField(max_length=5000, default="", blank=True, null=True)
    date_created = models.DateTimeField("Date created", auto_now_add=True)
    date_modified = models.DateTimeField("Date modified", auto_now=True)


    def __str__(self):
        return f"{self.customer.first_name} {self.customer.last_name} - {self.vendor.business_name}"








class Quote(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, default=1)
    emailed = models.BooleanField(default=False)
    emailed_date = models.CharField(max_length=64, blank=True, null=True)
    recurring = models.BooleanField(default=False)
    recurring_date = models.DateField(blank=True, null=True)
    recurring_data = models.JSONField(default=dict)

    quote_number = models.CharField("Quote number", blank=False, null=False, max_length=2048)
    quote_date = models.DateField("Quote Date", blank=False, null=False)
    due_date = models.DateField("Due Date", blank=False, null=False, default=timezone.now)
    po_number = models.CharField("PO number", blank=True, null=True, max_length=2048)
    ship_to = models.CharField("Ship to", max_length=500, null=True, blank=True)
    shipping_address = models.CharField("Shipping Address", max_length=500, null=True, blank=True)
    bill_to = models.CharField("Bill To", max_length=2048, blank=True, null=True)
    billing_address = models.CharField("Billing Address", max_length=500, null=True, blank=True)
    notes = models.CharField("Notes", max_length=1024, null=True, blank=True)
    
    item_list = ArrayField(models.PositiveIntegerField(blank=True), default=list)
    quantity_list = ArrayField(models.PositiveIntegerField(blank=True), default=list)
    item_total = models.FloatField("Item Total", blank=False, null=False)
    tax = models.CharField("Tax", blank=True, null=True, max_length=64, default="0")
    add_charges = models.CharField("Additional Charges", blank=True, null=True, max_length=64, default="0")
    grand_total = models.FloatField("Grand Total", blank=False, null=False)

    status = models.CharField("Status", max_length=20, blank=True, null=True, default='New')
    vendor = models.ForeignKey(MyUsers, on_delete=models.CASCADE)
    terms = models.CharField(max_length=5000, default="", blank=True, null=True)
    date_created = models.DateTimeField("Date created", auto_now_add=True)
    date_modified = models.DateTimeField("Date modified", auto_now=True)


    def __str__(self):
        return f"{self.customer.first_name} {self.customer.last_name} - {self.vendor.business_name}"









class Receipt(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, default=1)
    emailed = models.BooleanField(default=False)
    emailed_date = models.CharField(max_length=64, blank=True, null=True)
    recurring = models.BooleanField(default=False)
    recurring_date = models.DateField(blank=True, null=True)
    recurring_data = models.JSONField(default=dict)


    receipt_number = models.CharField("Receipt number", blank=False, null=False, max_length=2048)
    receipt_date = models.DateField("Receipt Date", blank=False, null=False)
    po_number = models.CharField("PO number", blank=True, null=True, max_length=2048)
    due_date = models.DateField("Due Date", blank=False, null=False)
    ship_to = models.CharField("Ship to", max_length=500, null=True, blank=True)
    shipping_address = models.CharField("Shipping Address", max_length=500, null=True, blank=True)
    bill_to = models.CharField("Bill To", max_length=2048, blank=True, null=True)
    billing_address = models.CharField("Billing Address", max_length=500, null=True, blank=True)
    notes = models.CharField("Notes", max_length=1024, null=True, blank=True)

    item_list = ArrayField(models.PositiveIntegerField(blank=True), default=list)
    quantity_list = ArrayField(models.PositiveIntegerField(blank=True), default=list)
    item_total = models.FloatField("Item Total", blank=False, null=False)
    tax = models.CharField("Tax", blank=True, null=True, max_length=64, default="0")
    add_charges = models.CharField("Additional Charges", blank=True, null=True, max_length=64, default="0")
    grand_total = models.FloatField("Grand Total", blank=False, null=False)

    status = models.CharField("Status", max_length=20, blank=True, null=True, default='New')
    vendor = models.ForeignKey(MyUsers, on_delete=models.CASCADE)
    terms = models.CharField(max_length=5000, default="", blank=True, null=True)
    date_created = models.DateTimeField("Date created", auto_now_add=True)
    date_modified = models.DateTimeField("Date modified", auto_now=True)


    def __str__(self):
        return f"{self.customer.first_name} {self.customer.last_name} - {self.vendor.business_name}"










class CreditNote(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, default=1)
    emailed = models.BooleanField(default=False)
    emailed_date = models.CharField(max_length=64, blank=True, null=True)
    recurring = models.BooleanField(default=False)
    recurring_date = models.DateField(blank=True, null=True)
    recurring_data = models.JSONField(default=dict)

    cn_number = models.CharField("Credit Note number", blank=False, null=False, max_length=2048)
    cn_date = models.DateField("Credit Note Date", blank=False, null=False)
    po_number = models.CharField("PO number", blank=True, null=True, max_length=2048)
    due_date = models.DateField("Due Date", blank=False, null=False)
    ship_to = models.CharField("Ship to", max_length=500, null=True, blank=True, default="")
    shipping_address = models.CharField("Shipping Address", max_length=500, null=True, blank=True, default="")
    bill_to = models.CharField("Bill To", max_length=2048, blank=True, null=True, default="")
    billing_address = models.CharField("Billing Address", max_length=500, null=True, blank=True, default="")
    notes = models.CharField("Notes", max_length=1024, null=True, blank=True)

    item_list = ArrayField(models.PositiveIntegerField(blank=True), default=list)
    quantity_list = ArrayField(models.PositiveIntegerField(blank=True), default=list)
    item_total = models.FloatField("Item Total", blank=False, null=False)
    tax = models.CharField("Tax", blank=True, null=True, max_length=64, default="0")
    add_charges = models.CharField("Additional Charges", blank=True, null=True, max_length=64, default="0")
    grand_total = models.FloatField("Grand Total", blank=False, null=False)

    status = models.CharField("Status", max_length=20, blank=True, null=True, default='New')
    vendor = models.ForeignKey(MyUsers, on_delete=models.CASCADE)
    terms = models.CharField(max_length=5000, default="", blank=True, null=True)
    date_created = models.DateTimeField("Date created", auto_now_add=True)
    date_modified = models.DateTimeField("Date modified", auto_now=True)


    def __str__(self):
        return f"{self.customer.first_name} {self.customer.last_name} - {self.vendor.business_name}"













class DeliveryNote(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, default=1)
    emailed = models.BooleanField(default=False)
    emailed_date = models.CharField(max_length=64, blank=True, null=True)
    recurring = models.BooleanField(default=False)
    recurring_date = models.DateField(blank=True, null=True)
    recurring_data = models.JSONField(default=dict)

    dn_number = models.CharField("Delivery Note number", blank=False, null=False, max_length=2048)
    dn_date = models.DateField("Delivery Note Date", blank=False, null=False)
    po_number = models.CharField("PO number", blank=True, null=True, max_length=2048)
    due_date = models.DateField("Due Date", blank=False, null=False)
    ship_to = models.CharField("Ship to", max_length=500, null=True, blank=True, default="")
    shipping_address = models.CharField("Shipping Address", max_length=500, null=True, blank=True, default="")
    bill_to = models.CharField("Bill To", max_length=2048, blank=True, null=True, default="")
    billing_address = models.CharField("Billing Address", max_length=500, null=True, blank=True, default="")
    notes = models.CharField("Notes", max_length=1024, null=True, blank=True)
    
    item_list = ArrayField(models.PositiveIntegerField(blank=True), default=list)
    quantity_list = ArrayField(models.PositiveIntegerField(blank=True), default=list)
    item_total = models.FloatField("Item Total", blank=False, null=False)
    tax = models.CharField("Tax", blank=True, null=True, max_length=64, default="0")
    add_charges = models.CharField("Additional Charges", blank=True, null=True, max_length=64, default="0")
    grand_total = models.FloatField("Grand Total", blank=False, null=False)

    status = models.CharField("Status", max_length=20, blank=True, null=True, default='New')
    vendor = models.ForeignKey(MyUsers, on_delete=models.CASCADE)
    terms = models.CharField(max_length=5000, default="", blank=True, null=True)
    date_created = models.DateTimeField("Date created", auto_now_add=True)
    date_modified = models.DateTimeField("Date modified", auto_now=True)


    def __str__(self):
        return f"{self.customer.first_name} {self.customer.last_name} - {self.vendor.business_name}"













class PayInvoice(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    payment_type = models.CharField("Payment Type", max_length=1024, blank=False, null=False)
    paid_date = models.DateField("Paid Date", blank=False, null=False)
    paid_amount = models.FloatField("Paid Amount", blank=False, null=False)
    payment_method = models.CharField("Payment Method", max_length=1024, blank=False, null=False)
    reference = models.CharField("Reference", max_length=1024, blank=False, null=False)
    date_created = models.DateTimeField("Date created", auto_now_add=True)
    date_modified = models.DateTimeField("Date modified", auto_now=True)


    def __str__(self):
        return self.invoice.first_name + self.invoice.last_name



class PayProforma(models.Model):
    proforma = models.ForeignKey(ProformaInvoice, on_delete=models.CASCADE)
    payment_type = models.CharField("Payment Type", max_length=1024, blank=False, null=False)
    paid_date = models.DateField("Paid Date", blank=False, null=False)
    paid_amount = models.FloatField("Paid Amount", blank=False, null=False)
    payment_method = models.CharField("Payment Method", max_length=1024, blank=False, null=False)
    reference = models.CharField("Reference", max_length=1024, blank=False, null=False)
    date_created = models.DateTimeField("Date created", auto_now_add=True)
    date_modified = models.DateTimeField("Date modified", auto_now=True)


    def __str__(self):
        return self.proforma.first_name + self.proforma.last_name



class PayPurchaseOrder(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    payment_type = models.CharField("Payment Type", max_length=1024, blank=False, null=False)
    paid_date = models.DateField("Paid Date", blank=False, null=False)
    paid_amount = models.FloatField("Paid Amount", blank=False, null=False)
    payment_method = models.CharField("Payment Method", max_length=1024, blank=False, null=False)
    reference = models.CharField("Reference", max_length=1024, blank=False, null=False)
    date_created = models.DateTimeField("Date created", auto_now_add=True)
    date_modified = models.DateTimeField("Date modified", auto_now=True)


    def __str__(self):
        return self.purchase_order.first_name + self.purchase_order.last_name



class PayEstimate(models.Model):
    estimate = models.ForeignKey(Estimate, on_delete=models.CASCADE)
    payment_type = models.CharField("Payment Type", max_length=1024, blank=False, null=False)
    paid_date = models.DateField("Paid Date", blank=False, null=False)
    paid_amount = models.FloatField("Paid Amount", blank=False, null=False)
    payment_method = models.CharField("Payment Method", max_length=1024, blank=False, null=False)
    reference = models.CharField("Reference", max_length=1024, blank=False, null=False)
    date_created = models.DateTimeField("Date created", auto_now_add=True)
    date_modified = models.DateTimeField("Date modified", auto_now=True)


    def __str__(self):
        return self.estimate.first_name + self.estimate.last_name






class PayQuote(models.Model):
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE)
    payment_type = models.CharField("Payment Type", max_length=1024, blank=False, null=False)
    paid_date = models.DateField("Paid Date", blank=False, null=False)
    paid_amount = models.FloatField("Paid Amount", blank=False, null=False)
    payment_method = models.CharField("Payment Method", max_length=1024, blank=False, null=False)
    reference = models.CharField("Reference", max_length=1024, blank=False, null=False)
    date_created = models.DateTimeField("Date created", auto_now_add=True)
    date_modified = models.DateTimeField("Date modified", auto_now=True)


    def __str__(self):
        return self.quote.first_name + self.quote.last_name








class PayReceipt(models.Model):
    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE)
    payment_type = models.CharField("Payment Type", max_length=1024, blank=False, null=False)
    paid_date = models.DateField("Paid Date", blank=False, null=False)
    paid_amount = models.FloatField("Paid Amount", blank=False, null=False)
    payment_method = models.CharField("Payment Method", max_length=1024, blank=False, null=False)
    reference = models.CharField("Reference", max_length=1024, blank=False, null=False)
    date_created = models.DateTimeField("Date created", auto_now_add=True)
    date_modified = models.DateTimeField("Date modified", auto_now=True)


    def __str__(self):
        return self.receipt.first_name + self.receipt.last_name







class PayCreditNote(models.Model):
    credit_note = models.ForeignKey(CreditNote, on_delete=models.CASCADE)
    payment_type = models.CharField("Payment Type", max_length=1024, blank=False, null=False)
    paid_date = models.DateField("Paid Date", blank=False, null=False)
    paid_amount = models.FloatField("Paid Amount", blank=False, null=False)
    payment_method = models.CharField("Payment Method", max_length=1024, blank=False, null=False)
    reference = models.CharField("Reference", max_length=1024, blank=False, null=False)
    date_created = models.DateTimeField("Date created", auto_now_add=True)
    date_modified = models.DateTimeField("Date modified", auto_now=True)


    def __str__(self):
        return self.credit_note.first_name + self.credit_note.last_name






class PayDeliveryNote(models.Model):
    delivery_note = models.ForeignKey(DeliveryNote, on_delete=models.CASCADE)
    payment_type = models.CharField("Payment Type", max_length=1024, blank=False, null=False)
    paid_date = models.DateField("Paid Date", blank=False, null=False)
    paid_amount = models.FloatField("Paid Amount", blank=False, null=False)
    payment_method = models.CharField("Payment Method", max_length=1024, blank=False, null=False)
    reference = models.CharField("Reference", max_length=1024, blank=False, null=False)
    date_created = models.DateTimeField("Date created", auto_now_add=True)
    date_modified = models.DateTimeField("Date modified", auto_now=True)


    def __str__(self):
        return self.credit_note.first_name + self.credit_note.last_name









class Item(models.Model):
    name = models.CharField("Name", max_length=1024, blank=False, null=False, unique=False)
    description = models.CharField("Item Description", max_length=2048, blank=True, null=True)
    cost_price = models.FloatField("Cost Price", blank=False, null=False)
    sales_price = models.FloatField("Sales Price", blank=False, null=False)
    sales_tax = models.FloatField("Sales Tax", blank=True, null=True, default=0.0)
    date_created = models.DateTimeField("Date created", auto_now_add=True)
    date_modified = models.DateTimeField("Date modified", auto_now=True)
    sku = models.CharField("SKU", max_length=15, blank=True, null=True, unique=True)

    vendor = models.ForeignKey(MyUsers, on_delete=models.CASCADE)


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




class PDFTemplate(models.Model):
    name = models.CharField("Name", max_length=1024, unique=True)
    photo_path = CloudinaryField("PDF Photo", null=True, blank=True)

    def image_preview(self):
        if self.photo_path:
            return mark_safe('<img src="{}" width="150" height="150" />'.format(self.photo_path.url))
        else:
            return '(No image)'

    image_preview.short_description = "Image Preview"


    def __str__(self):
        return self.name