from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from cloudinary.models import CloudinaryField


# Create your models here.




class MyUsers(AbstractUser):
    username = models.CharField("Username", max_length=1024, null=True, unique=False, blank=True)
    # photo_path = models.CharField("Profile Photo Path", max_length=2048, null=True, blank=True)
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
    # logo_path = models.CharField("Logo Path", max_length=2048, blank=True, null=True)
    tax_type = models.CharField("Tax Type", max_length=24, null=False, blank=False, default="On Total")
    tax_rate = models.FloatField("Tax Rate", null=False, blank=False, default=0.0)
    lang_pref = models.CharField("Language Preference", max_length=50, null=False, blank=False, default="English")
    region = models.CharField("Region", max_length=100, null=False, blank=False, default="US")
    email_report = models.CharField("Email Reports", max_length=100, blank=False, null=False, default="Monthly")
    currency = models.CharField("Currency", max_length=24, null=False, blank=False, default="Dollar")
    paypal = models.CharField("PayPal", max_length=100, null=True, blank=True)
    bank_transfer = models.CharField("Bank Transfer", max_length=100, null=True, blank=True)
    e_transfer = models.CharField("E-Transfer", max_length=100, null=True, blank=True)
    other_payment = models.CharField("Other Payment", max_length=100, null=True, blank=True)


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
    # logo_path = models.CharField("Logo Path", max_length=150, null=False, blank=False)
    logo_path = CloudinaryField("Logo photo", null=True, blank=True)
    ship_to = models.CharField("Ship to", max_length=500, null=False, blank=False)
    shipping_address = models.CharField("Shipping Address", max_length=500, null=False, blank=False)
    billing_address = models.CharField("Billing Address", max_length=500, null=False, blank=False)
    notes = models.CharField("Notes", max_length=1024, null=True, blank=True)
    status = models.CharField("Status", max_length=20, null=True, blank=True, default="New")
    invoice_number = models.CharField("Invoice Number", null=True, blank=True, default=1, max_length=2048)
    amount = models.FloatField("Amount", null=True, blank=True, default=0.00)

    vendor = models.ForeignKey(MyUsers, on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.customer.first_name} {self.customer.last_name} - {self.vendor.business_name}"






class Invoice(models.Model):
    # first_name = models.CharField("First Name", max_length=50, blank=True, null=True)
    # last_name = models.CharField("Last Name", max_length=50, blank=True, null=True)
    # address = models.CharField("Address", max_length=500, null=True, blank=True)
    # email = models.EmailField("Email", max_length=50, null=True, blank=True)
    # phone_number = models.CharField("Phone Number", max_length=15, null=True, blank=True)

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, default=1)

    
    taxable = models.BooleanField("Taxable", default=False, null=False, blank=False)
    invoice_pref = models.CharField("Invoice Preference", max_length=15, blank=False, null=False)
    # logo_path = models.CharField("Logo Path", max_length=150, null=False, blank=False)
    # logo_path = CloudinaryField("Logo photo", null=True, blank=True)
    invoice_number = models.CharField("Invoice number", blank=False, null=False, max_length=2048)
    invoice_date = models.DateField("Invoice Date", blank=False, null=False)
    po_number = models.CharField("PO number", blank=False, null=False, max_length=2048)
    due_date = models.DateField("Due Date", blank=False, null=False)
    ship_to = models.CharField("Ship to", max_length=500, null=False, blank=False)
    shipping_address = models.CharField("Shipping Address", max_length=500, null=False, blank=False)
    bill_to = models.CharField("Bill To", max_length=2048, blank=False, null=False)
    billing_address = models.CharField("Billing Address", max_length=500, null=False, blank=False)
    notes = models.CharField("Notes", max_length=1024, null=True, blank=True)
    
    item_list = ArrayField(models.PositiveIntegerField(blank=True), default=list)
    quantity_list = ArrayField(models.PositiveIntegerField(blank=True), default=list)
    item_total = models.FloatField("Item Total", blank=False, null=False)
    tax = models.FloatField("Tax", blank=True, null=True)
    add_charges = models.FloatField("Additional Charges", blank=True, null=True)
    sub_total = models.FloatField("Sub-Total", blank=False, null=False)
    discount_type = models.CharField("Discount Type", max_length=1024, blank=False, null=False)
    discount_amount = models.FloatField("Discount Amount", blank=False, null=False)
    grand_total = models.FloatField("Grand Total", blank=False, null=False)

    status = models.CharField("Status", max_length=20, blank=True, null=True, default='New')

    vendor = models.ForeignKey(MyUsers, on_delete=models.CASCADE)

    terms = models.CharField(max_length=5000, default="", blank=True, null=True)


    def __str__(self):
        return f"{self.customer.first_name} {self.customer.last_name} - {self.vendor.business_name}"    






class ProformaInvoice(models.Model):
    # first_name = models.CharField("First Name", max_length=50, blank=True, null=True)
    # last_name = models.CharField("Last Name", max_length=50, blank=True, null=True)
    # address = models.CharField("Address", max_length=500, null=True, blank=True)
    # email = models.EmailField("Email", max_length=50, null=True, blank=True)
    # phone_number = models.CharField("Phone Number", max_length=15, null=True, blank=True)

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, default=1)

    taxable = models.BooleanField("Taxable", default=False, null=False, blank=False)
    invoice_pref = models.CharField("Invoice Preference", max_length=15, blank=False, null=False)
    # logo_path = models.CharField("Logo Path", max_length=150, null=False, blank=False)
    # logo_path = CloudinaryField("Logo photo", null=True, blank=True)
    invoice_number = models.CharField("Invoice number", blank=False, null=False, max_length=2048)
    invoice_date = models.DateField("Invoice Date", blank=False, null=False)
    po_number = models.CharField("PO number", blank=False, null=False, max_length=2048)
    due_date = models.DateField("Due Date", blank=False, null=False)
    notes = models.CharField("Notes", max_length=1024, null=True, blank=True)
    attachment_path = models.CharField("Attachment Path", max_length=2048, blank=True, null=True)
    
    item_list = ArrayField(models.PositiveIntegerField(blank=True), default=list)
    quantity_list = ArrayField(models.PositiveIntegerField(blank=True), default=list)
    item_total = models.FloatField("Item Total", blank=False, null=False)
    tax = models.FloatField("Tax", blank=True, null=True)
    add_charges = models.FloatField("Additional Charges", blank=True, null=True)
    grand_total = models.FloatField("Grand Total", blank=False, null=False)

    status = models.CharField("Status", max_length=20, blank=True, null=True, default='New')
    vendor = models.ForeignKey(MyUsers, on_delete=models.CASCADE)
    terms = models.CharField(max_length=5000, default="", blank=True, null=True)


    def __str__(self):
        return f"{self.customer.first_name} {self.customer.last_name} - {self.vendor.business_name}"  







class PurchaseOrder(models.Model):
    # first_name = models.CharField("First Name", max_length=50, blank=True, null=True)
    # last_name = models.CharField("Last Name", max_length=50, blank=True, null=True)
    # address = models.CharField("Address", max_length=500, null=True, blank=True)
    # email = models.EmailField("Email", max_length=50, null=True, blank=True)
    # phone_number = models.CharField("Phone Number", max_length=15, null=True, blank=True)

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, default=1)

    taxable = models.BooleanField("Taxable", default=False, null=False, blank=False)
    po_pref = models.CharField("Purchase Order Preference", max_length=15, blank=False, null=False)
    # logo_path = models.CharField("Logo Path", max_length=150, null=False, blank=False)
    # logo_path = CloudinaryField("Logo photo", null=True, blank=True)

    po_number = models.CharField("PO number", blank=False, null=False, max_length=2048)
    po_date = models.DateField("Purchase Order Date", blank=False, null=False)
    due_date = models.DateField("Due Date", blank=False, null=False, default=timezone.now())
    ship_to = models.CharField("Ship to", max_length=500, null=False, blank=False)
    shipping_address = models.CharField("Shipping Address", max_length=500, null=False, blank=False)
    notes = models.CharField("Notes", max_length=1024, null=True, blank=True)

    
    item_list = ArrayField(models.PositiveIntegerField(blank=True), default=list)
    quantity_list = ArrayField(models.PositiveIntegerField(blank=True), default=list)
    item_total = models.FloatField("Item Total", blank=False, null=False)
    tax = models.FloatField("Tax", blank=True, null=True)
    add_charges = models.FloatField("Additional Charges", blank=True, null=True)
    grand_total = models.FloatField("Grand Total", blank=False, null=False)

    status = models.CharField("Status", max_length=20, blank=True, null=True, default='New')
    vendor = models.ForeignKey(MyUsers, on_delete=models.CASCADE)
    terms = models.CharField(max_length=5000, default="", blank=True, null=True)


    def __str__(self):
        return f"{self.customer.first_name} {self.customer.last_name} - {self.vendor.business_name}"






class Estimate(models.Model):
    # first_name = models.CharField("First Name", max_length=50, blank=True, null=True)
    # last_name = models.CharField("Last Name", max_length=50, blank=True, null=True)
    # address = models.CharField("Address", max_length=500, null=True, blank=True)
    # email = models.EmailField("Email", max_length=50, null=True, blank=True)
    # phone_number = models.CharField("Phone Number", max_length=15, null=True, blank=True)

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, default=1)

    taxable = models.BooleanField("Taxable", default=False, null=False, blank=False)
    estimate_pref = models.CharField("Estimate Preference", max_length=15, blank=False, null=False, default="a")
    # logo_path = models.CharField("Logo Path", max_length=150, null=False, blank=False)
    # logo_path = CloudinaryField("Logo photo", null=True, blank=True)

    estimate_number = models.CharField("Estimate number", blank=False, null=False, max_length=2048)
    estimate_date = models.DateField("Estimate Date", blank=False, null=False)
    po_number = models.CharField("PO Number", blank=False, null=False, max_length=1024, default=1)
    due_date = models.DateField("Due Date", blank=False, null=False)

    ship_to = models.CharField("Ship to", max_length=500, null=False, blank=False)
    shipping_address = models.CharField("Shipping Address", max_length=500, null=False, blank=False)
    bill_to = models.CharField("Bill To", max_length=2048, blank=False, null=False)
    billing_address = models.CharField("Billing Address", max_length=500, null=False, blank=False)
    notes = models.CharField("Notes", max_length=1024, null=True, blank=True)
    
    item_list = ArrayField(models.PositiveIntegerField(blank=True), default=list)
    quantity_list = ArrayField(models.PositiveIntegerField(blank=True), default=list)
    item_total = models.FloatField("Item Total", blank=False, null=False)
    tax = models.FloatField("Tax", blank=True, null=True)
    add_charges = models.FloatField("Additional Charges", blank=True, null=True)
    grand_total = models.FloatField("Grand Total", blank=False, null=False)

    status = models.CharField("Status", max_length=20, blank=True, null=True, default='New')
    vendor = models.ForeignKey(MyUsers, on_delete=models.CASCADE)
    terms = models.CharField(max_length=5000, default="", blank=True, null=True)


    def __str__(self):
        return f"{self.customer.first_name} {self.customer.last_name} - {self.vendor.business_name}"








class Quote(models.Model):
    # first_name = models.CharField("First Name", max_length=50, blank=True, null=True)
    # last_name = models.CharField("Last Name", max_length=50, blank=True, null=True)
    # address = models.CharField("Address", max_length=500, null=True, blank=True)
    # email = models.EmailField("Email", max_length=50, null=True, blank=True)
    # phone_number = models.CharField("Phone Number", max_length=15, null=True, blank=True)

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, default=1)

    taxable = models.BooleanField("Taxable", default=False, null=False, blank=False)
    quote_pref = models.CharField("Quote Preference", max_length=15, blank=False, null=False)
    # logo_path = models.CharField("Logo Path", max_length=150, null=False, blank=False)
    # logo_path = CloudinaryField("Logo photo", null=True, blank=True)

    quote_number = models.CharField("Quote number", blank=False, null=False, max_length=2048)
    quote_date = models.DateField("Quote Date", blank=False, null=False)
    due_date = models.DateField("Due Date", blank=False, null=False, default=timezone.now())
    po_number = models.CharField("PO number", blank=False, null=False, max_length=2048)
    ship_to = models.CharField("Ship to", max_length=500, null=False, blank=False)
    shipping_address = models.CharField("Shipping Address", max_length=500, null=False, blank=False)
    bill_to = models.CharField("Bill To", max_length=2048, blank=False, null=False)
    billing_address = models.CharField("Billing Address", max_length=500, null=False, blank=False)
    notes = models.CharField("Notes", max_length=1024, null=True, blank=True)

    
    item_list = ArrayField(models.PositiveIntegerField(blank=True), default=list)
    quantity_list = ArrayField(models.PositiveIntegerField(blank=True), default=list)
    item_total = models.FloatField("Item Total", blank=False, null=False)
    tax = models.FloatField("Tax", blank=True, null=True)
    add_charges = models.FloatField("Additional Charges", blank=True, null=True)
    grand_total = models.FloatField("Grand Total", blank=False, null=False)

    status = models.CharField("Status", max_length=20, blank=True, null=True, default='New')
    vendor = models.ForeignKey(MyUsers, on_delete=models.CASCADE)
    terms = models.CharField(max_length=5000, default="", blank=True, null=True)


    def __str__(self):
        return f"{self.customer.first_name} {self.customer.last_name} - {self.vendor.business_name}"









class Receipt(models.Model):
    # first_name = models.CharField("First Name", max_length=50, blank=True, null=True)
    # last_name = models.CharField("Last Name", max_length=50, blank=True, null=True)
    # address = models.CharField("Address", max_length=500, null=True, blank=True)
    # email = models.EmailField("Email", max_length=50, null=True, blank=True)
    # phone_number = models.CharField("Phone Number", max_length=15, null=True, blank=True)

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, default=1)

    taxable = models.BooleanField("Taxable", default=False, null=False, blank=False)
    receipt_pref = models.CharField("Receipt Preference", max_length=15, blank=False, null=False)
    # logo_path = models.CharField("Logo Path", max_length=150, null=False, blank=False)
    # logo_path = CloudinaryField("Logo photo", null=True, blank=True)

    receipt_number = models.CharField("Receipt number", blank=False, null=False, max_length=2048)
    receipt_date = models.DateField("Receipt Date", blank=False, null=False)
    po_number = models.CharField("PO number", blank=False, null=False, max_length=2048)
    due_date = models.DateField("Due Date", blank=False, null=False)
    ship_to = models.CharField("Ship to", max_length=500, null=False, blank=False)
    shipping_address = models.CharField("Shipping Address", max_length=500, null=False, blank=False)
    bill_to = models.CharField("Bill To", max_length=2048, blank=False, null=False)
    billing_address = models.CharField("Billing Address", max_length=500, null=False, blank=False)
    notes = models.CharField("Notes", max_length=1024, null=True, blank=True)

    
    item_list = ArrayField(models.PositiveIntegerField(blank=True), default=list)
    quantity_list = ArrayField(models.PositiveIntegerField(blank=True), default=list)
    item_total = models.FloatField("Item Total", blank=False, null=False)
    tax = models.FloatField("Tax", blank=True, null=True)
    add_charges = models.FloatField("Additional Charges", blank=True, null=True)
    grand_total = models.FloatField("Grand Total", blank=False, null=False)

    status = models.CharField("Status", max_length=20, blank=True, null=True, default='New')
    vendor = models.ForeignKey(MyUsers, on_delete=models.CASCADE)
    terms = models.CharField(max_length=5000, default="", blank=True, null=True)


    def __str__(self):
        return f"{self.customer.first_name} {self.customer.last_name} - {self.vendor.business_name}"










class CreditNote(models.Model):
    # first_name = models.CharField("First Name", max_length=50, blank=True, null=True)
    # last_name = models.CharField("Last Name", max_length=50, blank=True, null=True)
    # address = models.CharField("Address", max_length=500, null=True, blank=True)
    # email = models.EmailField("Email", max_length=50, null=True, blank=True)
    # phone_number = models.CharField("Phone Number", max_length=15, null=True, blank=True)

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, default=1)

    taxable = models.BooleanField("Taxable", default=False, null=False, blank=False)
    cn_pref = models.CharField("Credit Note Preference", max_length=15, blank=False, null=False)
    # logo_path = models.CharField("Logo Path", max_length=150, null=False, blank=False)
    # logo_path = CloudinaryField("Logo photo", null=True, blank=True)

    cn_number = models.CharField("Credit Note number", blank=False, null=False, max_length=2048)
    cn_date = models.DateField("Credit Note Date", blank=False, null=False)
    po_number = models.CharField("PO number", blank=False, null=False, max_length=2048)
    due_date = models.DateField("Due Date", blank=False, null=False)
    ship_to = models.CharField("Ship to", max_length=500, null=False, blank=False)
    shipping_address = models.CharField("Shipping Address", max_length=500, null=False, blank=False)
    notes = models.CharField("Notes", max_length=1024, null=True, blank=True)

    
    item_list = ArrayField(models.PositiveIntegerField(blank=True), default=list)
    quantity_list = ArrayField(models.PositiveIntegerField(blank=True), default=list)
    item_total = models.FloatField("Item Total", blank=False, null=False)
    tax = models.FloatField("Tax", blank=True, null=True)
    add_charges = models.FloatField("Additional Charges", blank=True, null=True)
    grand_total = models.FloatField("Grand Total", blank=False, null=False)

    status = models.CharField("Status", max_length=20, blank=True, null=True, default='New')
    vendor = models.ForeignKey(MyUsers, on_delete=models.CASCADE)
    terms = models.CharField(max_length=5000, default="", blank=True, null=True)


    def __str__(self):
        return f"{self.customer.first_name} {self.customer.last_name} - {self.vendor.business_name}"













class DeliveryNote(models.Model):
    # first_name = models.CharField("First Name", max_length=50, blank=True, null=True)
    # last_name = models.CharField("Last Name", max_length=50, blank=True, null=True)
    # address = models.CharField("Address", max_length=500, null=True, blank=True)
    # email = models.EmailField("Email", max_length=50, null=True, blank=True)
    # phone_number = models.CharField("Phone Number", max_length=15, null=True, blank=True)

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, default=1)

    taxable = models.BooleanField("Taxable", default=False, null=False, blank=False)
    dn_pref = models.CharField("Delivery Note Preference", max_length=15, blank=False, null=False)
    # logo_path = models.CharField("Logo Path", max_length=150, null=False, blank=False)
    # logo_path = CloudinaryField("Logo photo", null=True, blank=True)

    dn_number = models.CharField("Delivery Note number", blank=False, null=False, max_length=2048)
    dn_date = models.DateField("Delivery Note Date", blank=False, null=False)
    po_number = models.CharField("PO number", blank=False, null=False, max_length=2048)
    due_date = models.DateField("Due Date", blank=False, null=False)
    ship_to = models.CharField("Ship to", max_length=500, null=False, blank=False)
    shipping_address = models.CharField("Shipping Address", max_length=500, null=False, blank=False)
    notes = models.CharField("Notes", max_length=1024, null=True, blank=True)

    
    item_list = ArrayField(models.PositiveIntegerField(blank=True), default=list)
    quantity_list = ArrayField(models.PositiveIntegerField(blank=True), default=list)
    item_total = models.FloatField("Item Total", blank=False, null=False)
    tax = models.FloatField("Tax", blank=True, null=True)
    add_charges = models.FloatField("Additional Charges", blank=True, null=True)
    grand_total = models.FloatField("Grand Total", blank=False, null=False)

    status = models.CharField("Status", max_length=20, blank=True, null=True, default='New')
    vendor = models.ForeignKey(MyUsers, on_delete=models.CASCADE)
    terms = models.CharField(max_length=5000, default="", blank=True, null=True)


    def __str__(self):
        return f"{self.customer.first_name} {self.customer.last_name} - {self.vendor.business_name}"













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
        return self.estimate.first_name + self.estimate.last_name






class PayQuote(models.Model):
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE)
    payment_type = models.CharField("Payment Type", max_length=1024, blank=False, null=False)
    paid_date = models.DateField("Paid Date", blank=False, null=False)
    paid_amount = models.FloatField("Paid Amount", blank=False, null=False)
    payment_method = models.CharField("Payment Method", max_length=1024, blank=False, null=False)
    reference = models.CharField("Reference", max_length=1024, blank=False, null=False)


    def __str__(self):
        return self.quote.first_name + self.quote.last_name








class PayReceipt(models.Model):
    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE)
    payment_type = models.CharField("Payment Type", max_length=1024, blank=False, null=False)
    paid_date = models.DateField("Paid Date", blank=False, null=False)
    paid_amount = models.FloatField("Paid Amount", blank=False, null=False)
    payment_method = models.CharField("Payment Method", max_length=1024, blank=False, null=False)
    reference = models.CharField("Reference", max_length=1024, blank=False, null=False)


    def __str__(self):
        return self.receipt.first_name + self.receipt.last_name







class PayCreditNote(models.Model):
    credit_note = models.ForeignKey(CreditNote, on_delete=models.CASCADE)
    payment_type = models.CharField("Payment Type", max_length=1024, blank=False, null=False)
    paid_date = models.DateField("Paid Date", blank=False, null=False)
    paid_amount = models.FloatField("Paid Amount", blank=False, null=False)
    payment_method = models.CharField("Payment Method", max_length=1024, blank=False, null=False)
    reference = models.CharField("Reference", max_length=1024, blank=False, null=False)


    def __str__(self):
        return self.credit_note.first_name + self.credit_note.last_name






class PayDeliveryNote(models.Model):
    delivery_note = models.ForeignKey(DeliveryNote, on_delete=models.CASCADE)
    payment_type = models.CharField("Payment Type", max_length=1024, blank=False, null=False)
    paid_date = models.DateField("Paid Date", blank=False, null=False)
    paid_amount = models.FloatField("Paid Amount", blank=False, null=False)
    payment_method = models.CharField("Payment Method", max_length=1024, blank=False, null=False)
    reference = models.CharField("Reference", max_length=1024, blank=False, null=False)


    def __str__(self):
        return self.credit_note.first_name + self.credit_note.last_name









class Item(models.Model):
    name = models.CharField("Name", max_length=1024, blank=False, null=False, unique=False)
    description = models.CharField("Item Description", max_length=2048, blank=True, null=True)
    cost_price = models.FloatField("Cost Price", blank=False, null=False)
    sales_price = models.FloatField("Sales Price", blank=False, null=False)
    sales_tax = models.FloatField("Sales Tax", blank=False, null=False)

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
