from django.contrib import admin

from .models import Customer, MyUsers, Invoice, ProformaInvoice, Estimate, PurchaseOrder, \
                    PayInvoice, PayEstimate, PayProforma, PayPurchaseOrder, JWT
# Register your models here.


admin.site.register(MyUsers)
admin.site.register(JWT)
admin.site.register(Invoice)
admin.site.register(ProformaInvoice)
admin.site.register(Estimate)
admin.site.register(PurchaseOrder)
admin.site.register(PayInvoice)
admin.site.register(PayEstimate)
admin.site.register(PayProforma)
admin.site.register(PayPurchaseOrder)
admin.site.register(Customer)
