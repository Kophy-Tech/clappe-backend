from django.contrib import admin

from .models import CreditNote, Customer, DeliveryNote, Item, MyUsers, Invoice, PayCreditNote, PayDeliveryNote, PayQuote,\
                     PayReceipt, ProformaInvoice, Estimate, PurchaseOrder, PayInvoice, PayEstimate, PayProforma,\
                     PayPurchaseOrder, Quote, Receipt, JWT
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    exclude = ("password_recovery","password_recovery_time")



admin.site.register(MyUsers, UserAdmin)
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
admin.site.register(Item)

admin.site.register(CreditNote)
admin.site.register(DeliveryNote)
admin.site.register(PayCreditNote)
admin.site.register(PayDeliveryNote)
admin.site.register(PayQuote)
admin.site.register(PayReceipt)
admin.site.register(Quote)
admin.site.register(Receipt)