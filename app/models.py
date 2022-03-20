from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.




class MyUsers(AbstractUser):
    username = models.CharField("Username", max_length=1024, null=True, unique=False, blank=True)
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








class JWT(models.Model):
    user = models.OneToOneField(MyUsers, on_delete=models.CASCADE)
    access = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-user']

    def __str__(self):
        return self.user.email
