from rest_framework import serializers
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import check_password
from drf_tweaks.serializers import ModelSerializer

from .models import CreditNote, Customer, DeliveryNote, Item, MyUsers, Invoice, PayCreditNote, PayDeliveryNote, PayQuote, PayReceipt, ProformaInvoice, \
                    Estimate, PurchaseOrder, PayInvoice, PayEstimate, PayProforma, PayPurchaseOrder, Quote, Receipt

from .forms import ScheduleForm

import cloudinary, requests





CURRENCY_MAPPING = {
    "Dollar": "$",
    "Pound": "£",
    "Rupees": "₹",
    "Naira": "₦",

}



def get_number(request, num_type):

    # invoice, proforma, pruchase_order, estimate, quote, receipt, credit_note, delivery_note, 

    if num_type == "invoice":
        count = len(Invoice.objects.filter(vendor=request.user.id).all())

    elif num_type == "proforma":
        count = len(ProformaInvoice.objects.filter(vendor=request.user.id).all())

    elif num_type == "purchase_order":
        count = len(PurchaseOrder.objects.filter(vendor=request.user.id).all())

    elif num_type == "estimate":
        count = len(Estimate.objects.filter(vendor=request.user.id).all())

    elif num_type == "quote":
        count = len(Quote.objects.filter(vendor=request.user.id).all())

    elif num_type == "receipt":
        count = len(Receipt.objects.filter(vendor=request.user.id).all())

    elif num_type == "credit_note":
        count = len(CreditNote.objects.filter(vendor=request.user.id).all())

    elif num_type == "delivery_note":
        count = len(DeliveryNote.objects.filter(vendor=request.user.id).all())


    return "00" + str(count)







def process_picture(media, models, type="profile"):
    if type == 'profile':
        file_url = cloudinary.uploader.upload(media, folder="profile_photos", 
                                          public_id = f"{models.email}_picture", 
                                          use_filename=True, unique_filename=False)['url']
    
    elif type=="logo":
        file_url = cloudinary.uploader.upload(media, folder="logos", 
                                            public_id = f"{models.email}_logo",
                                            use_filename=True, unique_filename=False)['url']
    else:
        file_url = cloudinary.uploader.upload(media, folder="signatures", 
                                            public_id = f"{models.email}_signature",
                                            use_filename=True, unique_filename=False)['url']

    return file_url













class SignUpSerializer(ModelSerializer):
    required_error = "{fieldname} is required."
    blank_error = "{fieldname} can not be blank."

    class Meta:
        model = MyUsers
        fields = ['first_name', 'last_name', 'password', 'email', 'phone_number']

    def save(self):

        password = self.validated_data['password']

        new_user = MyUsers.objects.create(email=self.validated_data['email'],
                                            first_name=self.validated_data['first_name'], last_name=self.validated_data['last_name'], 
                                            phone_number=self.validated_data['phone_number'])
        new_user.set_password(password)
        new_user.save()
        
        return new_user






class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()




class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = MyUsers
        fields = ['first_name', 'last_name', 'email', 'phone_number']






############################################### customer #############################################################################


class CustomerCreateSerializer(ModelSerializer):
    required_error = "{fieldname} is required."
    blank_error = "{fieldname} can not be blank."
    class Meta:
        model = Customer
        fields = ["first_name", "last_name", "business_name", "address", "email", "phone_number", "taxable", 
                    "invoice_pref", "ship_to", "shipping_address", "billing_address", "notes",]



    def save(self, request):
        new_customer = Customer()
        new_customer.first_name = self.validated_data["first_name"]
        new_customer.last_name = self.validated_data["last_name"]
        new_customer.business_name = self.validated_data["business_name"]
        new_customer.address = self.validated_data["address"]
        new_customer.email = self.validated_data["email"]
        new_customer.phone_number = self.validated_data["phone_number"]
        new_customer.taxable = self.validated_data["taxable"]
        new_customer.invoice_pref = self.validated_data["invoice_pref"]
        # new_customer.logo_path = self.validated_data["logo_path"]
        new_customer.ship_to = self.validated_data["ship_to"]
        new_customer.shipping_address = self.validated_data["shipping_address"]
        new_customer.billing_address = self.validated_data["billing_address"]
        new_customer.notes = self.validated_data["notes"]
        
        new_customer.vendor = request.user

        new_customer.save()

        return new_customer



    def update(self, instance, validated_data):
        instance.first_name = validated_data["first_name"]
        instance.last_name = validated_data["last_name"]
        instance.business_name = validated_data["business_name"]
        instance.address = validated_data["address"]
        instance.email = validated_data["email"]
        instance.phone_number = validated_data["phone_number"]
        instance.taxable = validated_data["taxable"]
        instance.invoice_pref = validated_data["invoice_pref"]
        # instance.logo_path = validated_data["logo_path"]
        instance.ship_to = validated_data["ship_to"]
        instance.shipping_address = validated_data["shipping_address"]
        instance.billing_address = validated_data["billing_address"]
        instance.notes = validated_data["notes"]
        instance.status = validated_data["status"]
        instance.invoice_number = validated_data["invoice_number"]
        instance.amount = validated_data["amount"]

        instance.save()

        return instance





class CustomerEditSerializer(ModelSerializer):
    required_error = "{fieldname} is required."
    blank_error = "{fieldname} can not be blank."
    class Meta:
        model = Customer
        fields = ["address", "billing_address", "business_name", "email", "first_name", "invoice_pref", "last_name",
                "notes", "phone_number", "ship_to", "shipping_address", "taxable"]



    def update(self, instance, validated_data):
        instance.first_name = validated_data["first_name"]
        instance.last_name = validated_data["last_name"]
        instance.business_name = validated_data["business_name"]
        instance.address = validated_data["address"]
        instance.email = validated_data["email"]
        instance.phone_number = validated_data["phone_number"]
        instance.taxable = validated_data["taxable"]
        instance.invoice_pref = validated_data["invoice_pref"]
        # instance.logo_path = validated_data["logo_path"]
        instance.ship_to = validated_data["ship_to"]
        instance.shipping_address = validated_data["shipping_address"]
        instance.billing_address = validated_data["billing_address"]
        instance.notes = validated_data["notes"]

        instance.save()

        return instance







class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ["id", "first_name", "last_name", "business_name", "address", "email", "phone_number", "taxable", 
                    "invoice_pref", "ship_to", "shipping_address", "billing_address", "notes", "status"]









###################################################### items ########################################################

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ["id", "name", "description", "cost_price", "sales_price", "sales_tax"]







class CreateItemSerializer(ModelSerializer):
    required_error = "{fieldname} is required."
    blank_error = "{fieldname} can not be blank."
    class Meta:
        model = Item
        fields = ["name", "description", "cost_price", "sales_price", "sales_tax"]
        


    
    def save(self, request):
        new_item = Item()
        new_item.name = self.validated_data['name']
        new_item.description = self.validated_data['description']
        new_item.cost_price = self.validated_data['cost_price']
        new_item.sales_price = self.validated_data['sales_price']
        new_item.sales_tax = self.validated_data['sales_tax']

        new_item.vendor = request.user

        new_item.save()

        return new_item


    def update(self, instance):
        instance.name = self.validated_data['name']
        instance.description = self.validated_data['description']
        instance.cost_price = self.validated_data['cost_price']
        instance.sales_price = self.validated_data['sales_price']
        instance.sales_tax = self.validated_data['sales_tax']

        instance.save()

        return instance



def pdf_item_serializer(items, quantities):
    total_list = []
    for id in range(len(items)):
        single_item = Item.objects.get(pk=items[id])
        serialized_items = ItemSerializer(single_item)

        item_data = {**serialized_items.data, "quantity": quantities[id]}
        item_data['amount'] = item_data['sales_price'] * quantities[id]
        item_data.pop("cost_price")
        item_data.pop("description")

        total_list.append(item_data)


    return total_list











############################################### invoice ####################################################################


class InvoiceCreate(ModelSerializer):
    item_list = serializers.ListField(required=True)
    send_email = serializers.BooleanField(required=True)
    download = serializers.BooleanField(required=True)
    customer_id= serializers.IntegerField(required=True)

    required_error = "{fieldname} is required."
    blank_error = "{fieldname} can not be blank."
    # invalid_error = "{fieldname} is not valid"
    class Meta:
        model = Invoice
        fields = [
            "customer_id",
            "invoice_date","po_number","due_date","ship_to","shipping_address","bill_to","billing_address","notes","item_list",
            "item_total","tax","add_charges","sub_total","discount_type","discount_amount","grand_total", "send_email", "download", "terms"]


    def save(self, request):

        new_invoice = Invoice()
        new_invoice.customer = Customer.objects.get(id=self.validated_data['customer_id'])

        # new_invoice.taxable = self.validated_data["taxable"]
        # new_invoice.invoice_pref = self.validated_data["invoice_pref"]
        # new_invoice.logo_path = self.validated_data["logo_path"]
        new_invoice.invoice_number = get_number(request, 'invoice')
        new_invoice.invoice_date = self.validated_data['invoice_date']
        new_invoice.po_number = self.validated_data['po_number']
        new_invoice.due_date = self.validated_data['due_date']

        new_invoice.ship_to = self.validated_data["ship_to"]
        new_invoice.shipping_address = self.validated_data["shipping_address"]
        new_invoice.bill_to = self.validated_data["bill_to"]
        new_invoice.billing_address = self.validated_data["billing_address"]
        new_invoice.notes = self.validated_data["notes"]
        new_invoice.terms = self.validated_data["terms"]


        item_list = self.validated_data['item_list']
        ids = [int(i['id']) for i in item_list]
        quantities = [int(i['quantity']) for i in item_list]

        new_invoice.item_list = ids
        new_invoice.quantity_list = quantities

        new_invoice.item_total = self.validated_data["item_total"]
        new_invoice.tax = self.validated_data["tax"]
        new_invoice.add_charges = self.validated_data["add_charges"]
        new_invoice.sub_total = self.validated_data["sub_total"]
        new_invoice.discount_type = self.validated_data["discount_type"]
        new_invoice.discount_amount = self.validated_data["discount_amount"]
        new_invoice.grand_total = self.validated_data["grand_total"]
        new_invoice.status = "Unpaid"
        
        new_invoice.vendor = request.user

        new_invoice.save()


        # if self.validated_data['send_email']:
        #     # for sending email when creating a new document
        #     invoice_ser = InvoiceSerializer(new_invoice).data
        #     invoice_ser['item_list'] = pdf_item_serializer(new_invoice.item_list, new_invoice.quantity_list)
        #     file_name = get_report(invoice_ser, self.validated_data, CURRENCY_MAPPING[request.user.currency], "invoice", request)
        #     body = "Attached to the email is the receipt of your transaction on https://www.clappe.com"
        #     subject = "Transaction Receipt"
        #     send_my_email(new_invoice.email, body, subject, file_name)
        
        # elif self.validated_data['download']:
        #     invoice_ser = InvoiceSerializer(new_invoice).data
        #     invoice_ser['item_list'] = pdf_item_serializer(new_invoice.item_list, new_invoice.quantity_list)
        #     file_name = get_report(invoice_ser, CURRENCY_MAPPING[request.user.currency], "invoice", request, self.validated_data['terms'])

        
            
        # date, docuemnt_type, document_id, task_type [one time or periodic], email
        schedule_details = {
            "date": new_invoice.due_date,
            "document_type": "invoice",
            "document_id": new_invoice.id,
            "task_type": "one_time",
            "email": new_invoice.customer.email
        }

        new_schedule = ScheduleForm(schedule_details)
        if new_schedule.is_valid():
            _, _ = new_schedule.save()


        return new_invoice





class InvoiceSerializer(serializers.ModelSerializer):
    # customer = CustomerSerializer(read_only=True)
    class Meta:
        model = Invoice
        fields = [ "id", "customer_id","invoice_number",
            "invoice_date","po_number","due_date","ship_to","shipping_address","bill_to","billing_address","notes", "quantity_list",
            "item_total","tax","add_charges","sub_total","discount_type","discount_amount","grand_total", "status", "item_list", "notes", "terms"]







class InvoiceEditSerializer(ModelSerializer):
    customer_id = serializers.IntegerField(required=True)
    item_list = serializers.ListField(required=True)
    send_email = serializers.BooleanField(required=True)
    download = serializers.BooleanField(required=True)

    required_error = "{fieldname} is required."
    blank_error = "{fieldname} can not be blank."
    class Meta:
        model = Invoice
        fields = [
            "customer_id",
            "invoice_date","po_number","due_date","ship_to","shipping_address","bill_to", "billing_address", "notes", "item_list",
            "item_total","tax","add_charges","sub_total","discount_type","discount_amount","grand_total", "status", "send_email", "download", "terms"]


    def update(self, instance, validated_data, request):
        # instance.first_name = validated_data["first_name"]
        # instance.last_name = validated_data["last_name"]
        # instance.address = validated_data["address"]
        # instance.email = validated_data["email"]
        # instance.phone_number = validated_data["phone_number"]
        instance.customer = Customer.objects.get(id=validated_data['customer_id'])

        # instance.taxable = validated_data["taxable"]
        # instance.invoice_pref = validated_data["invoice_pref"]
        # instance.logo_path = validated_data["logo_path"]
        instance.invoice_date = validated_data['invoice_date']
        instance.po_number = validated_data['po_number']
        instance.due_date = validated_data['due_date']

        instance.ship_to = validated_data["ship_to"]
        instance.shipping_address = validated_data["shipping_address"]
        instance.bill_to = validated_data["bill_to"]
        instance.billing_address = validated_data["billing_address"]
        instance.notes = validated_data["notes"]
        instance.terms = validated_data["terms"]

        item_list = validated_data['item_list']
        ids = [int(i['id']) for i in item_list]
        quantities = [int(i['quantity']) for i in item_list]

        instance.item_list = ids
        instance.quantity_list = quantities


        instance.item_total = validated_data["item_total"]
        instance.tax = validated_data["tax"]
        instance.add_charges = validated_data["add_charges"]
        instance.sub_total = validated_data["sub_total"]
        instance.discount_type = validated_data["discount_type"]
        instance.discount_amount = validated_data["discount_amount"]
        instance.grand_total = validated_data["grand_total"]


        instance.save()


        # if self.validated_data['send_email']:
        #     # for sending email when creating a new document
        #     invoice_ser = InvoiceSerializer(instance).data
        #     invoice_ser['item_list'] = pdf_item_serializer(instance.item_list, instance.quantity_list)
        #     file_name = get_report(invoice_ser, self.validated_data, CURRENCY_MAPPING[request.user.currency], "invoice", request)
        #     body = "Attached to the email is the receipt of your transaction on https://www.clappe.com"
        #     subject = "Transaction Receipt"
        #     send_my_email(instance.email, body, subject, file_name)
            
        # date, docuemnt_type, document_id, task_type [one time or periodic], email
        schedule_details = {
            "date": instance.due_date,
            "document_type": "invoice",
            "document_id": instance.id,
            "task_type": "one_time",
            "email": instance.customer.email
        }
        new_schedule = ScheduleForm(schedule_details)
        if new_schedule.is_valid():
            _ = new_schedule.update()

        return instance



class PayInvoiceSerializer(ModelSerializer):
    invoice_id = serializers.IntegerField()
    required_error = "{fieldname} is required."
    blank_error = "{fieldname} can not be blank."
    class Meta:
        model = PayInvoice
        fields = ["payment_type", "paid_date", "paid_amount", "payment_method", "reference", "invoice_id"]


    def save(self):

        try:
            invoice = Invoice.objects.get(id=self.validated_data['invoice_id'])
        except Exception as e:
            print(e)
            return None
        pay_invoice = PayInvoice()
        pay_invoice.payment_type = self.validated_data["payment_type"]
        pay_invoice.paid_date = self.validated_data["paid_date"]
        pay_invoice.paid_amount = self.validated_data["paid_amount"]
        pay_invoice.payment_method = self.validated_data["payment_method"]
        pay_invoice.reference = self.validated_data["reference"]

        invoice.status = "Paid"
        invoice.save()
        pay_invoice.invoice = invoice
        

        pay_invoice.save()

        return pay_invoice










######################################### proforma invoice #########################################################################

class ProformaCreateSerializer(ModelSerializer):
    item_list = serializers.ListField(required=True)
    send_email = serializers.BooleanField(required=True)
    download = serializers.BooleanField(required=True)
    customer_id = serializers.IntegerField(required=True)


    required_error = "{fieldname} is required."
    blank_error = "{fieldname} can not be blank."
    class Meta:
        model = ProformaInvoice
        fields = [
                "customer_id", 
                "invoice_date", "po_number", "due_date", "notes", "item_list", 
                    "item_total", "tax", "add_charges", "grand_total", "send_email", "download", "terms"]


    def save(self, request):
        new_proforma = ProformaInvoice()
        # new_proforma.first_name = self.validated_data["first_name"]
        # new_proforma.last_name = self.validated_data["last_name"]
        # new_proforma.address = self.validated_data["address"]
        # new_proforma.email = self.validated_data["email"]
        # new_proforma.phone_number = self.validated_data["phone_number"]

        new_proforma.customer = Customer.objects.get(id=self.validated_data['customer_id'])

        # new_proforma.taxable = self.validated_data["taxable"]
        # new_proforma.invoice_pref = self.validated_data["invoice_pref"]
        # new_proforma.logo_path = self.validated_data["logo_path"]
        new_proforma.invoice_number = get_number(request, 'proforma')
        new_proforma.invoice_date = self.validated_data["invoice_date"]
        new_proforma.po_number = self.validated_data["po_number"]
        new_proforma.due_date = self.validated_data["due_date"]
        new_proforma.notes = self.validated_data["notes"]
        new_proforma.terms = self.validated_data["terms"]
        
        item_list = self.validated_data['item_list']
        ids = [int(i['id']) for i in item_list]
        quantities = [int(i['quantity']) for i in item_list]

        new_proforma.item_list = ids
        new_proforma.quantity_list = quantities


        new_proforma.item_total = self.validated_data["item_total"]
        new_proforma.tax = self.validated_data["tax"]
        new_proforma.add_charges = self.validated_data["add_charges"]
        new_proforma.grand_total = self.validated_data["grand_total"]

        new_proforma.vendor = request.user

        new_proforma.save()


        # if self.validated_data['send_email']:
        #     # for sending email when creating a new document
        #     file_name = f"Proforma Invoice for {new_proforma.email}.pdf"
        #     get_report(file_name)
        #     body = "Attached to the email is the receipt of your transaction on https://www.clappe.com"
        #     subject = "Transaction Receipt"
        #     send_my_email(new_proforma.email, body, subject, file_name)
            
        # date, docuemnt_type, document_id, task_type [one time or periodic], email
        schedule_details = {
            "date": new_proforma.due_date,
            "document_type": "proforma",
            "document_id": new_proforma.id,
            "task_type": "one_time",
            "email": new_proforma.customer.email
        }

        new_schedule = ScheduleForm(schedule_details)
        if new_schedule.is_valid():
            _, _ = new_schedule.save()

        return new_proforma



class ProformerInvoiceSerailizer(serializers.ModelSerializer):
    # customer = CustomerSerializer(read_only=True)
    class Meta:
        model = ProformaInvoice
        fields = [
                "id", "customer_id", 
                    "invoice_number", "invoice_date", "po_number", "due_date", "notes", "item_list", "quantity_list",
                    "item_total", "tax", "add_charges", "grand_total", "status", "terms"]




class ProformaEditSerializer(ModelSerializer):
    item_list = serializers.ListField(required=True)
    send_email = serializers.BooleanField(required=True)
    download = serializers.BooleanField(required=True)
    customer_id = serializers.IntegerField(required=True)

    required_error = "{fieldname} is required."
    blank_error = "{fieldname} can not be blank."
    class Meta:
        model = ProformaInvoice
        fields = [
                "customer_id", 
                    "invoice_date", "po_number", "due_date", "notes", "item_list", 
                    "item_total", "tax", "add_charges", "grand_total", "status", "send_email", "download", "terms"]




    def update(self, instance, validated_data):
        # instance.first_name = validated_data["first_name"]
        # instance.last_name = validated_data["last_name"]
        # instance.address = validated_data["address"]
        # instance.email = validated_data["email"]
        # instance.phone_number = validated_data["phone_number"]

        instance.customer = Customer.objects.get(id=validated_data['customer_id'])

        # instance.taxable = validated_data["taxable"]
        # instance.invoice_pref = validated_data["invoice_pref"]
        # instance.logo_path = validated_data["logo_path"]
        instance.invoice_date = validated_data["invoice_date"]
        instance.po_number = validated_data["po_number"]
        instance.due_date = validated_data["due_date"]
        instance.notes = validated_data["notes"]
        instance.terms = validated_data["terms"]
        
        item_list = self.validated_data['item_list']
        ids = [int(i['id']) for i in item_list]
        quantities = [int(i['quantity']) for i in item_list]

        instance.item_list = ids
        instance.quantity_list = quantities


        instance.item_total = validated_data["item_total"]
        instance.tax = validated_data["tax"]
        instance.add_charges = validated_data["add_charges"]
        instance.grand_total = validated_data["grand_total"]

        instance.save()

        # if self.validated_data['send_email']:
        #     # for sending email when creating a new document
        #     file_name = f"Proforma Invoice for {instance.email}.pdf"
        #     get_report(file_name)
        #     body = "Attached to the email is the receipt of your transaction on https://www.clappe.com"
        #     subject = "Transaction Receipt"
        #     send_my_email(instance.email, body, subject, file_name)
            
        # date, docuemnt_type, document_id, task_type [one time or periodic], email
        schedule_details = {
            "date": instance.due_date,
            "document_type": "proforma",
            "document_id": instance.id,
            "task_type": "one_time",
            "email": instance.customer.email
        }
        new_schedule = ScheduleForm(schedule_details)
        if new_schedule.is_valid():
            _ = new_schedule.update()

        return instance






class PayProformaSerializer(ModelSerializer):
    proforma_id = serializers.IntegerField()
    required_error = "{fieldname} is required."
    blank_error = "{fieldname} can not be blank."
    class Meta:
        model = PayProforma
        fields = ["payment_type", "paid_date", "paid_amount", "payment_method", "reference", "proforma_id"]


    def save(self):

        try:
            proforma = ProformaInvoice.objects.get(id=self.validated_data['proforma_id'])
        except Exception as e:
            print(e)
            return None

        pay_proforma = PayProforma()
        pay_proforma.payment_type = self.validated_data["payment_type"]
        pay_proforma.paid_date = self.validated_data["paid_date"]
        pay_proforma.paid_amount = self.validated_data["paid_amount"]
        pay_proforma.payment_method = self.validated_data["payment_method"]
        pay_proforma.reference = self.validated_data["reference"]

        proforma.status = "Paid"
        proforma.save()
        pay_proforma.proforma = proforma
        

        pay_proforma.save()

        return pay_proforma












############################################## purchase order ########################################################################

class PurchaseCreateSerializer(ModelSerializer):
    item_list = serializers.ListField(required=True)
    send_email = serializers.BooleanField(required=True)
    download = serializers.BooleanField(required=True)
    customer_id = serializers.IntegerField(required=True)


    required_error = "{fieldname} is required."
    blank_error = "{fieldname} can not be blank."
    class Meta:
        model = PurchaseOrder
        fields = [
                "customer_id", 
                    "po_date", "ship_to", "notes", "shipping_address", "item_list", "due_date",
                    "item_total", "tax", "add_charges", "grand_total", "send_email", "download", "terms"]



    def save(self, request):
        new_purchaseorder = PurchaseOrder()
        # new_purchaseorder.first_name = self.validated_data["first_name"]
        # new_purchaseorder.last_name = self.validated_data["last_name"]
        # new_purchaseorder.address = self.validated_data["address"]
        # new_purchaseorder.email = self.validated_data["email"]
        # new_purchaseorder.phone_number = self.validated_data["phone_number"]
        new_purchaseorder.customer = Customer.objects.get(id=self.validated_data['customer_id'])

        # new_purchaseorder.taxable = self.validated_data["taxable"]
        # new_purchaseorder.po_pref = self.validated_data["po_pref"]
        # new_purchaseorder.logo_path = self.validated_data["logo_path"]
        new_purchaseorder.po_number = get_number(request, 'purchase_order')
        new_purchaseorder.po_date = self.validated_data["po_date"]
        new_purchaseorder.due_date = self.validated_data["due_date"]
        new_purchaseorder.ship_to = self.validated_data["ship_to"]
        new_purchaseorder.notes = self.validated_data["notes"]
        new_purchaseorder.shipping_address = self.validated_data["shipping_address"]
        new_purchaseorder.terms = self.validated_data["terms"]
        
        item_list = self.validated_data['item_list']
        ids = [int(i['id']) for i in item_list]
        quantities = [int(i['quantity']) for i in item_list]

        new_purchaseorder.item_list = ids
        new_purchaseorder.quantity_list = quantities


        new_purchaseorder.item_total = self.validated_data["item_total"]
        new_purchaseorder.tax = self.validated_data["tax"]
        new_purchaseorder.add_charges = self.validated_data["add_charges"]
        new_purchaseorder.grand_total = self.validated_data["grand_total"]

        new_purchaseorder.vendor = request.user

        new_purchaseorder.save()

        # if self.validated_data['send_email']:
        #     # for sending email when creating a new document
        #     file_name = f"Purchase Order for {new_purchaseorder.email}.pdf"
        #     get_report(file_name)
        #     body = "Attached to the email is the receipt of your transaction on https://www.clappe.com"
        #     subject = "Transaction Receipt"
        #     send_my_email(new_purchaseorder.email, body, subject, file_name)
            
        # date, docuemnt_type, document_id, task_type [one time or periodic], email
        schedule_details = {
            "date": new_purchaseorder.due_date,
            "document_type": "purchase",
            "document_id": new_purchaseorder.id,
            "task_type": "one_time",
            "email": new_purchaseorder.customer.email
        }

        new_schedule = ScheduleForm(schedule_details)
        if new_schedule.is_valid():
            _, _ = new_schedule.save()

        return new_purchaseorder



class PurchaseOrderSerailizer(serializers.ModelSerializer):
    # customer = CustomerSerializer(read_only=True)
    class Meta:
        model = PurchaseOrder
        fields = [
                "id", "customer_id", 
                    "po_number", "po_date", "due_date", "ship_to", "notes", "shipping_address",  "item_list", "quantity_list",
                    "item_total", "tax", "add_charges", "grand_total",  "status", "terms"]




class PurchaseEditSerializer(ModelSerializer):
    item_list = serializers.ListField(required=True)
    send_email = serializers.BooleanField(required=True)
    download = serializers.BooleanField(required=True)
    customer_id = serializers.IntegerField(required=True)



    required_error = "{fieldname} is required."
    blank_error = "{fieldname} can not be blank."
    class Meta:
        model = PurchaseOrder
        fields = [
                "customer_id", 
                    "po_date", "due_date", "ship_to", "notes", "shipping_address", "item_list", 
                    "item_total", "tax", "add_charges", "grand_total", "status", "send_email", "download", "terms"]




    def update(self, instance, validated_data):
        # instance.first_name = validated_data["first_name"]
        # instance.last_name = validated_data["last_name"]
        # instance.address = validated_data["address"]
        # instance.email = validated_data["email"]
        # instance.phone_number = validated_data["phone_number"]
        instance.customer = Customer.objects.get(id=validated_data['customer_id'])
        # instance.taxable = validated_data["taxable"]
        # instance.po_pref = validated_data["po_pref"]
        # instance.logo_path = validated_data["logo_path"]
        instance.po_date = validated_data["po_date"]
        instance.notes = validated_data["notes"]
        instance.terms = validated_data["terms"]
        
        item_list = self.validated_data['item_list']
        ids = [int(i['id']) for i in item_list]
        quantities = [int(i['quantity']) for i in item_list]

        instance.item_list = ids
        instance.quantity_list = quantities


        instance.item_total = validated_data["item_total"]
        instance.tax = validated_data["tax"]
        instance.add_charges = validated_data["add_charges"]
        instance.grand_total = validated_data["grand_total"]

        instance.save()

        # if self.validated_data['send_email']:
        #     # for sending email when creating a new document
        #     file_name = f"Purchase Order for {instance.email}.pdf"
        #     get_report(file_name)
        #     body = "Attached to the email is the receipt of your transaction on https://www.clappe.com"
        #     subject = "Transaction Receipt"
        #     send_my_email(instance.email, body, subject, file_name)
            
        # date, docuemnt_type, document_id, task_type [one time or periodic], email
        schedule_details = {
            "date": instance.due_date,
            "document_type": "purchase",
            "document_id": instance.id,
            "task_type": "one_time",
            "email": instance.customer.email
        }
        new_schedule = ScheduleForm(schedule_details)
        if new_schedule.is_valid():
            _ = new_schedule.update()

        return instance






class PayPurchaseSerializer(ModelSerializer):
    purchase_id = serializers.IntegerField()
    required_error = "{fieldname} is required."
    blank_error = "{fieldname} can not be blank."
    class Meta:
        model = PayPurchaseOrder
        fields = ["payment_type", "paid_date", "paid_amount", "payment_method", "reference", "purchase_id"]


    def save(self):

        try:
            purchase_order = PurchaseOrder.objects.get(id=self.validated_data['purchase_id'])
        except Exception as e:
            print(e)
            return None

        pay_purchase = PayPurchaseOrder()
        pay_purchase.payment_type = self.validated_data["payment_type"]
        pay_purchase.paid_date = self.validated_data["paid_date"]
        pay_purchase.paid_amount = self.validated_data["paid_amount"]
        pay_purchase.payment_method = self.validated_data["payment_method"]
        pay_purchase.reference = self.validated_data["reference"]

        purchase_order.status = "Paid"
        purchase_order.save()
        pay_purchase.purchase_order = purchase_order
        

        pay_purchase.save()

        return pay_purchase







############################################ estimate ########################################################################

class EstimateCreateSerializer(ModelSerializer):
    item_list = serializers.ListField(required=True)
    send_email = serializers.BooleanField(required=True)
    download = serializers.BooleanField(required=True)
    customer_id = serializers.IntegerField(required=True)


    required_error = "{fieldname} is required."
    blank_error = "{fieldname} can not be blank."
    class Meta:
        model = Estimate
        fields = [
                "customer_id", "due_date", "po_number",
                    "estimate_date", "ship_to", "shipping_address", "bill_to", "billing_address",
                    "notes", "item_list", "item_total", "tax", "add_charges", "grand_total", "send_email", "download", "terms"]


    def save(self, request):
        new_estimate = Estimate()
        # new_estimate.first_name = self.validated_data["first_name"]
        # new_estimate.last_name = self.validated_data["last_name"]
        # new_estimate.address = self.validated_data["address"]
        # new_estimate.email = self.validated_data["email"]
        # new_estimate.phone_number = self.validated_data["phone_number"]
        new_estimate.customer = Customer.objects.get(id=self.validated_data['customer_id'])
        # new_estimate.taxable = self.validated_data["taxable"]
        # new_estimate.estimate_pref = self.validated_data["estimate_pref"]
        # new_estimate.logo_path = self.validated_data["logo_path"]
        new_estimate.estimate_number = get_number(request, 'estimate')
        new_estimate.estimate_date = self.validated_data["estimate_date"]
        new_estimate.po_number = self.validated_data["po_number"]
        new_estimate.due_date = self.validated_data["due_date"]
        new_estimate.ship_to = self.validated_data["ship_to"]
        new_estimate.shipping_address = self.validated_data["shipping_address"]
        new_estimate.bill_to = self.validated_data["bill_to"]
        new_estimate.billing_address = self.validated_data["billing_address"]
        new_estimate.notes = self.validated_data["notes"]
        new_estimate.terms = self.validated_data["terms"]
        
        item_list = self.validated_data['item_list']
        ids = [int(i['id']) for i in item_list]
        quantities = [int(i['quantity']) for i in item_list]

        new_estimate.item_list = ids
        new_estimate.quantity_list = quantities


        new_estimate.item_total = self.validated_data["item_total"]
        new_estimate.tax = self.validated_data["tax"]
        new_estimate.add_charges = self.validated_data["add_charges"]
        new_estimate.grand_total = self.validated_data["grand_total"]

        new_estimate.vendor = request.user

        new_estimate.save()

        # if self.validated_data['send_email']:
        #     # for sending email when creating a new document
        #     file_name = f"Estimate for {new_estimate.email}.pdf"
        #     get_report(file_name)
        #     body = "Attached to the email is the receipt of your transaction on https://www.clappe.com"
        #     subject = "Transaction Receipt"
        #     send_my_email(new_estimate.email, body, subject, file_name)
            
        # date, docuemnt_type, document_id, task_type [one time or periodic], email
        schedule_details = {
            "date": new_estimate.due_date,
            "document_type": "estimate",
            "document_id": new_estimate.id,
            "task_type": "one_time",
            "email": new_estimate.customer.email
        }

        new_schedule = ScheduleForm(schedule_details)
        if new_schedule.is_valid():
            _, _ = new_schedule.save()

        return new_estimate



class EstimateSerailizer(serializers.ModelSerializer):
    # customer = CustomerSerializer(read_only=True)
    class Meta:
        model = Estimate
        fields = [
                "id", "customer_id", "po_number", "due_date",
                    "estimate_number", "estimate_date", "ship_to", "shipping_address", "bill_to", "billing_address",
                    "notes", "item_list", "quantity_list", "item_total", "tax", "add_charges", "grand_total", "status", "terms"]
        




class EstimateEditSerializer(ModelSerializer):
    item_list = serializers.ListField(required=True)
    send_email = serializers.BooleanField(required=True)
    download = serializers.BooleanField(required=True)
    customer_id = serializers.IntegerField(required=True)


    required_error = "{fieldname} is required."
    blank_error = "{fieldname} can not be blank."
    class Meta:
        model = Estimate
        fields = [
                "customer_id", "po_number", "due_date",
                    "estimate_date", "ship_to", "shipping_address", "bill_to", "billing_address",
                    "notes", "item_list", "item_total", "tax", "add_charges", "grand_total", "status", "send_email", "download", "terms"]



    def update(self, instance, validated_data):
        # instance.first_name = validated_data["first_name"]
        # instance.last_name = validated_data["last_name"]
        # instance.address = validated_data["address"]
        # instance.email = validated_data["email"]
        # instance.phone_number = validated_data["phone_number"]
        instance.customer = Customer.objects.get(id=validated_data['customer_id'])
        # instance.taxable = validated_data["taxable"]
        # instance.estimate_pref = validated_data["estimate_pref"]
        # instance.logo_path = validated_data["logo_path"]
        instance.estimate_date = validated_data["estimate_date"]
        instance.due_date = validated_data["due_date"]
        instance.po_number = validated_data["po_number"]
        instance.ship_to = validated_data["ship_to"]
        instance.shipping_address = validated_data["shipping_address"]
        instance.bill_to = validated_data["bill_to"]
        instance.billing_address = validated_data["billing_address"]
        instance.notes = validated_data["notes"]
        instance.terms = validated_data["terms"]
        
        item_list = self.validated_data['item_list']
        ids = [int(i['id']) for i in item_list]
        quantities = [int(i['quantity']) for i in item_list]

        instance.item_list = ids
        instance.quantity_list = quantities


        instance.item_total = validated_data["item_total"]
        instance.tax = validated_data["tax"]
        instance.add_charges = validated_data["add_charges"]
        instance.grand_total = validated_data["grand_total"]

        instance.save()

        # if self.validated_data['send_email']:
        #     # for sending email when creating a new document
        #     file_name = f"Estimate for {instance.email}.pdf"
        #     get_report(file_name)
        #     body = "Attached to the email is the receipt of your transaction on https://www.clappe.com"
        #     subject = "Transaction Receipt"
        #     send_my_email(instance.email, body, subject, file_name)
            
        # date, docuemnt_type, document_id, task_type [one time or periodic], email
        schedule_details = {
            "date": instance.due_date,
            "document_type": "estimate",
            "document_id": instance.id,
            "task_type": "one_time",
            "email": instance.customer.email
        }
        new_schedule = ScheduleForm(schedule_details)
        if new_schedule.is_valid():
            _ = new_schedule.update()

        return instance






class PayEstimateSerializer(ModelSerializer):
    estimate_id = serializers.IntegerField()
    required_error = "{fieldname} is required."
    blank_error = "{fieldname} can not be blank."
    class Meta:
        model = PayEstimate
        fields = ["payment_type", "paid_date", "paid_amount", "payment_method", "reference", "estimate_id"]


    def save(self):

        try:
            estimate = Estimate.objects.get(id=self.validated_data['estimate_id'])
        except Exception as e:
            print(e)
            return None

        pay_estimate = PayEstimate()
        pay_estimate.payment_type = self.validated_data["payment_type"]
        pay_estimate.paid_date = self.validated_data["paid_date"]
        pay_estimate.paid_amount = self.validated_data["paid_amount"]
        pay_estimate.payment_method = self.validated_data["payment_method"]
        pay_estimate.reference = self.validated_data["reference"]

        estimate.status = "Paid"
        estimate.save()
        pay_estimate.estimate = estimate
        

        pay_estimate.save()

        return pay_estimate








############################################################ quote ##############################################################################


class QuoteCreateSerializer(ModelSerializer):
    item_list = serializers.ListField(required=True)
    send_email = serializers.BooleanField(required=True)
    download = serializers.BooleanField(required=True)
    customer_id = serializers.IntegerField(required=True)


    required_error = "{fieldname} is required."
    blank_error = "{fieldname} can not be blank."
    class Meta:
        model = Quote
        fields = [ "customer_id", "due_date",
                    "quote_date", "po_number", "ship_to", "shipping_address", "bill_to", "billing_address", 
                    "notes",  "item_list", "item_total", "tax", "add_charges", "grand_total", "send_email", "download", "terms"]
                        



    def save(self, request):
        new_quote = Quote()
        # new_quote.first_name = self.validated_data["first_name"]
        # new_quote.last_name = self.validated_data["last_name"]
        # new_quote.address = self.validated_data["address"]
        # new_quote.email = self.validated_data["email"]
        # new_quote.phone_number = self.validated_data["phone_number"]
        new_quote.customer = Customer.objects.get(id=self.validated_data['customer_id'])
        # new_quote.taxable = self.validated_data["taxable"]
        # new_quote.quote_pref = self.validated_data["quote_pref"]
        # new_quote.logo_path = self.validated_data["logo_path"]
        new_quote.quote_number = get_number(request, 'quote')
        new_quote.quote_date = self.validated_data["quote_date"]
        new_quote.due_date = self.validated_data["due_date"]
        new_quote.po_number = self.validated_data["po_number"]
        new_quote.ship_to = self.validated_data["ship_to"]
        new_quote.shipping_address = self.validated_data["shipping_address"]
        new_quote.bill_to = self.validated_data["bill_to"]
        new_quote.billing_address = self.validated_data["billing_address"]
        new_quote.notes = self.validated_data["notes"]
        new_quote.terms = self.validated_data["terms"]
        
        item_list = self.validated_data['item_list']
        ids = [int(i['id']) for i in item_list]
        quantities = [int(i['quantity']) for i in item_list]

        new_quote.item_list = ids
        new_quote.quantity_list = quantities


        new_quote.item_total = self.validated_data["item_total"]
        new_quote.tax = self.validated_data["tax"]
        new_quote.add_charges = self.validated_data["add_charges"]
        new_quote.grand_total = self.validated_data["grand_total"]

        new_quote.vendor = request.user

        new_quote.save()


        # if self.validated_data['send_email']:
        #     # for sending email when creating a new document
        #     file_name = f"Quote for {new_quote.email}.pdf"
        #     get_report(file_name)
        #     body = "Attached to the email is the receipt of your transaction on https://www.clappe.com"
        #     subject = "Transaction Receipt"
        #     send_my_email(Invoice.email, body, subject, file_name)
            
        # date, docuemnt_type, document_id, task_type [one time or periodic], email
        schedule_details = {
            "date": new_quote.due_date,
            "document_type": "quote",
            "document_id": new_quote.id,
            "task_type": "one_time",
            "email": new_quote.customer.email
        }

        new_schedule = ScheduleForm(schedule_details)
        if new_schedule.is_valid():
            _, _ = new_schedule.save()

        return new_quote



class QuoteSerailizer(serializers.ModelSerializer):
    # customer = CustomerSerializer(read_only=True)
    class Meta:
        model = Quote
        fields = [
                "id", "customer_id", 
                    "quote_number", "quote_date", "po_number", "ship_to", "shipping_address", "bill_to", "billing_address", 
                    "notes", "item_list", "quantity_list", "item_total", "tax", "add_charges", "grand_total", "status", "terms"]
        




class QuoteEditSerializer(ModelSerializer):
    item_list = serializers.ListField(required=True)
    send_email = serializers.BooleanField(required=True)
    download = serializers.BooleanField(required=True)
    customer_id = serializers.IntegerField(required=True)


    required_error = "{fieldname} is required."
    blank_error = "{fieldname} can not be blank."
    class Meta:
        model = Quote
        fields = [
               "customer_id", "due_date",
                    "quote_date", "po_number", "ship_to", "shipping_address", "bill_to", "billing_address", 
                    "notes", "item_list", "item_total", "tax", "add_charges", "grand_total", "status", "send_email", "download", "terms"]
        



    def update(self, instance, validated_data):
        # instance.first_name = validated_data["first_name"]
        # instance.last_name = validated_data["last_name"]
        # instance.address = validated_data["address"]
        # instance.email = validated_data["email"]
        # instance.phone_number = validated_data["phone_number"]
        instance.customer = Customer.objects.get(id=validated_data['customer_id'])
        # instance.taxable = validated_data["taxable"]
        # instance.quote_pref = validated_data["quote_pref"]
        # instance.logo_path = validated_data["logo_path"]
        instance.quote_date = validated_data["quote_date"]
        instance.due_date = validated_data["due_date"]
        instance.po_number = validated_data["po_number"]
        instance.ship_to = validated_data["ship_to"]
        instance.shipping_address = validated_data["shipping_address"]
        instance.bill_to = validated_data["bill_to"]
        instance.billing_address = validated_data["billing_address"]
        instance.notes = validated_data["notes"]
        instance.terms = validated_data["terms"]
        
        item_list = self.validated_data['item_list']
        ids = [int(i['id']) for i in item_list]
        quantities = [int(i['quantity']) for i in item_list]

        instance.item_list = ids
        instance.quantity_list = quantities


        instance.item_total = validated_data["item_total"]
        instance.tax = validated_data["tax"]
        instance.add_charges = validated_data["add_charges"]
        instance.grand_total = validated_data["grand_total"]

        instance.save()

        # if self.validated_data['send_email']:
        #     # for sending email when creating a new document
        #     file_name = f"Quote for {instance.email}.pdf"
        #     get_report(file_name)
        #     body = "Attached to the email is the receipt of your transaction on https://www.clappe.com"
        #     subject = "Transaction Receipt"
        #     send_my_email(Invoice.email, body, subject, file_name)
            
        # date, docuemnt_type, document_id, task_type [one time or periodic], email
        schedule_details = {
            "date": instance.due_date,
            "document_type": "quote",
            "document_id": instance.id,
            "task_type": "one_time",
            "email": instance.customer.email
        }
        new_schedule = ScheduleForm(schedule_details)
        if new_schedule.is_valid():
            _ = new_schedule.update()

        return instance






class PayQuoteSerializer(ModelSerializer):
    quote_id = serializers.IntegerField()
    required_error = "{fieldname} is required."
    blank_error = "{fieldname} can not be blank."
    class Meta:
        model = PayQuote
        fields = ["payment_type", "paid_date", "paid_amount", "payment_method", "reference", "quote_id"]
        


    def save(self):

        try:
            quote = Quote.objects.get(id=self.validated_data['quote_id'])
        except Exception as e:
            print(e)
            return None

        pay_quote = PayQuote()
        pay_quote.payment_type = self.validated_data["payment_type"]
        pay_quote.paid_date = self.validated_data["paid_date"]
        pay_quote.paid_amount = self.validated_data["paid_amount"]
        pay_quote.payment_method = self.validated_data["payment_method"]
        pay_quote.reference = self.validated_data["reference"]

        quote.status = "Paid"
        quote.save()
        pay_quote.quote = quote
        

        pay_quote.save()

        return pay_quote










############################################################ credit note ##############################################################################


class CNCreateSerializer(ModelSerializer):
    item_list = serializers.ListField(required=True)
    send_email = serializers.BooleanField(required=True)
    download = serializers.BooleanField(required=True)
    customer_id = serializers.IntegerField(required=True)


    required_error = "{fieldname} is required."
    blank_error = "{fieldname} can not be blank."
    class Meta:
        model = CreditNote
        fields = [ "customer_id", 
                    "cn_date", "po_number", "due_date", "ship_to", "shipping_address", "notes", "item_list", 
                    "item_total", "tax", "add_charges", "grand_total", "send_email", "download", "terms"]       

        


    def save(self, request):
        new_credit = CreditNote()
        # new_credit.first_name = self.validated_data["first_name"]
        # new_credit.last_name = self.validated_data["last_name"]
        # new_credit.address = self.validated_data["address"]
        # new_credit.email = self.validated_data["email"]
        # new_credit.phone_number = self.validated_data["phone_number"]
        new_credit.customer = Customer.objects.get(id=self.validated_data['customer_id'])

        # new_credit.taxable = self.validated_data["taxable"]
        # new_credit.cn_pref = self.validated_data["cn_pref"]
        # new_credit.logo_path = self.validated_data["logo_path"]
        new_credit.cn_number = get_number(request, 'credit_note')
        new_credit.cn_date = self.validated_data["cn_date"]
        new_credit.po_number = self.validated_data["po_number"]
        new_credit.due_date = self.validated_data["due_date"]
        new_credit.ship_to = self.validated_data["ship_to"]
        new_credit.shipping_address = self.validated_data["shipping_address"]
        new_credit.notes = self.validated_data["notes"]
        new_credit.terms = self.validated_data["terms"]
        
        item_list = self.validated_data['item_list']
        ids = [int(i['id']) for i in item_list]
        quantities = [int(i['quantity']) for i in item_list]

        new_credit.item_list = ids
        new_credit.quantity_list = quantities


        new_credit.item_total = self.validated_data["item_total"]
        new_credit.tax = self.validated_data["tax"]
        new_credit.add_charges = self.validated_data["add_charges"]
        new_credit.grand_total = self.validated_data["grand_total"]

        new_credit.vendor = request.user

        new_credit.save()

        # if self.validated_data['send_email']:
        #     # for sending email when creating a new document
        #     file_name = f"Credit Note for {new_credit.email}.pdf"
        #     get_report(file_name)
        #     body = "Attached to the email is the receipt of your transaction on https://www.clappe.com"
        #     subject = "Transaction Receipt"
        #     send_my_email(Invoice.email, body, subject, file_name)
            
        # date, docuemnt_type, document_id, task_type [one time or periodic], email
        schedule_details = {
            "date": new_credit.due_date,
            "document_type": "credit_note",
            "document_id": new_credit.id,
            "task_type": "one_time",
            "email": new_credit.customer.email
        }

        new_schedule = ScheduleForm(schedule_details)
        if new_schedule.is_valid():
            _, _ = new_schedule.save()

        return new_credit



class CreditNoteSerailizer(serializers.ModelSerializer):
    # customer = CustomerSerializer(read_only=True)
    class Meta:
        model = CreditNote
        fields = [
                "id", "customer_id", 
                    "cn_number", "cn_date", "po_number", "due_date", "ship_to", "shipping_address", "notes",  "item_list", "quantity_list", 
                    "item_total", "tax", "add_charges", "grand_total", "status", "terms"]
        




class CNEditSerializer(ModelSerializer):
    item_list = serializers.ListField(required=True)
    send_email = serializers.BooleanField(required=True)
    download = serializers.BooleanField(required=True)
    customer_id = serializers.IntegerField(required=True)


    required_error = "{fieldname} is required."
    blank_error = "{fieldname} can not be blank."
    class Meta:
        model = CreditNote
        fields = [
                "customer_id", 
                    "cn_date", "po_number", "due_date", "ship_to", "shipping_address", "notes", "item_list", 
                    "item_total", "tax", "add_charges", "grand_total", "status", "send_email", "download", "terms"]

        



    def update(self, instance, validated_data):
        # instance.first_name = validated_data["first_name"]
        # instance.last_name = validated_data["last_name"]
        # instance.address = validated_data["address"]
        # instance.email = validated_data["email"]
        # instance.phone_number = validated_data["phone_number"]
        instance.customer = Customer.objects.get(id=validated_data['customer_id'])
        # instance.taxable = validated_data["taxable"]
        # instance.cn_pref = validated_data["cn_pref"]
        # instance.logo_path = validated_data["logo_path"]
        instance.cn_date = validated_data["cn_date"]
        instance.po_number = validated_data["po_number"]
        instance.due_date = validated_data["due_date"]
        instance.ship_to = validated_data["ship_to"]
        instance.shipping_address = validated_data["shipping_address"]
        instance.notes = validated_data["notes"]
        instance.terms = validated_data["terms"]
        
        item_list = self.validated_data['item_list']
        ids = [int(i['id']) for i in item_list]
        quantities = [int(i['quantity']) for i in item_list]

        instance.item_list = ids
        instance.quantity_list = quantities


        instance.item_total = validated_data["item_total"]
        instance.tax = validated_data["tax"]
        instance.add_charges = validated_data["add_charges"]
        instance.grand_total = validated_data["grand_total"]

        instance.save()

        # if self.validated_data['send_email']:
        #     # for sending email when creating a new document
        #     file_name = f"Credit Note for {instance.email}.pdf"
        #     get_report(file_name)
        #     body = "Attached to the email is the receipt of your transaction on https://www.clappe.com"
        #     subject = "Transaction Receipt"
        #     send_my_email(Invoice.email, body, subject, file_name)
            
        # date, docuemnt_type, document_id, task_type [one time or periodic], email
        schedule_details = {
            "date": instance.due_date,
            "document_type": "credit_note",
            "document_id": instance.id,
            "task_type": "one_time",
            "email": instance.customer.email
        }
        new_schedule = ScheduleForm(schedule_details)
        if new_schedule.is_valid():
            _ = new_schedule.update()

        return instance






class PayCNSerializer(ModelSerializer):
    credit_id = serializers.IntegerField()
    required_error = "{fieldname} is required."
    blank_error = "{fieldname} can not be blank."
    class Meta:
        model = PayCreditNote
        fields = ["payment_type", "paid_date", "paid_amount", "payment_method", "reference", "credit_id"]
        


    def save(self):

        try:
            credit = CreditNote.objects.get(id=self.validated_data['credit_id'])
        except Exception as e:
            print(e)
            return None

        pay_credit = PayCreditNote()
        pay_credit.payment_type = self.validated_data["payment_type"]
        pay_credit.paid_date = self.validated_data["paid_date"]
        pay_credit.paid_amount = self.validated_data["paid_amount"]
        pay_credit.payment_method = self.validated_data["payment_method"]
        pay_credit.reference = self.validated_data["reference"]

        credit.status = "Paid"
        credit.save()
        pay_credit.credit_note = credit
        

        pay_credit.save()

        return pay_credit














############################################################ receipt ##############################################################################


class REceiptCreateSerializer(ModelSerializer):
    item_list = serializers.ListField(required=True)
    send_email = serializers.BooleanField(required=True)
    download = serializers.BooleanField(required=True)
    customer_id = serializers.IntegerField(required=True)


    required_error = "{fieldname} is required."
    blank_error = "{fieldname} can not be blank."
    class Meta:
        model = Receipt
        fields = [ "customer_id", 
                    "receipt_date", "po_number", "due_date", "ship_to", "shipping_address", "bill_to", "billing_address", 
                    "notes", "item_list", "item_total", "tax", "add_charges", "grand_total", "send_email", "download", "terms"]
        
        


    def save(self, request):
        new_receipt = Receipt()
        # new_receipt.first_name = self.validated_data["first_name"]
        # new_receipt.last_name = self.validated_data["last_name"]
        # new_receipt.address = self.validated_data["address"]
        # new_receipt.email = self.validated_data["email"]
        # new_receipt.phone_number = self.validated_data["phone_number"]
        new_receipt.customer = Customer.objects.get(id=self.validated_data['customer_id'])
        # new_receipt.taxable = self.validated_data["taxable"]
        # new_receipt.receipt_pref = self.validated_data["receipt_pref"]
        # new_receipt.logo_path = self.validated_data["logo_path"]
        new_receipt.receipt_number = get_number(request, 'receipt')
        new_receipt.receipt_date = self.validated_data["receipt_date"]
        new_receipt.po_number = self.validated_data["po_number"]
        new_receipt.due_date = self.validated_data["due_date"]
        new_receipt.ship_to = self.validated_data["ship_to"]
        new_receipt.shipping_address = self.validated_data["shipping_address"]
        new_receipt.bill_to = self.validated_data["bill_to"]
        new_receipt.billing_address = self.validated_data["billing_address"]
        new_receipt.notes = self.validated_data["notes"]
        new_receipt.terms = self.validated_data["terms"]
        
        item_list = self.validated_data['item_list']
        ids = [int(i['id']) for i in item_list]
        quantities = [int(i['quantity']) for i in item_list]

        new_receipt.item_list = ids
        new_receipt.quantity_list = quantities


        new_receipt.item_total = self.validated_data["item_total"]
        new_receipt.tax = self.validated_data["tax"]
        new_receipt.add_charges = self.validated_data["add_charges"]
        new_receipt.grand_total = self.validated_data["grand_total"]

        new_receipt.vendor = request.user

        new_receipt.save()

        # if self.validated_data['send_email']:
        #     # for sending email when creating a new document
        #     file_name = f"Receipt for {new_receipt.email}.pdf"
        #     get_report(file_name)
        #     body = "Attached to the email is the receipt of your transaction on https://www.clappe.com"
        #     subject = "Transaction Receipt"
        #     send_my_email(Invoice.email, body, subject, file_name)
            
        # date, docuemnt_type, document_id, task_type [one time or periodic], email
        schedule_details = {
            "date": new_receipt.due_date,
            "document_type": "receipt",
            "document_id": new_receipt.id,
            "task_type": "one_time",
            "email": new_receipt.customer.email
        }

        new_schedule = ScheduleForm(schedule_details)
        if new_schedule.is_valid():
            _, _ = new_schedule.save()

        return new_receipt



class ReceiptSerailizer(serializers.ModelSerializer):
    # customer = CustomerSerializer(read_only=True)
    class Meta:
        model = Receipt
        fields = [
                "id", "customer_id", 
                    "receipt_number", "receipt_date", "po_number", "due_date", "ship_to", "shipping_address", "bill_to", "billing_address", 
                    "notes", "item_list", "quantity_list", "item_total", "tax", "add_charges", "grand_total", "status", "terms"]
        




class ReceiptEditSerializer(ModelSerializer):
    item_list = serializers.ListField(required=True)
    send_email = serializers.BooleanField(required=True)
    download = serializers.BooleanField(required=True)
    customer_id = serializers.IntegerField(required=True)


    required_error = "{fieldname} is required."
    blank_error = "{fieldname} can not be blank."
    class Meta:
        model = Receipt
        fields = [
                "customer_id", 
                    "receipt_date", "po_number", "due_date", "ship_to", "shipping_address", "bill_to", "billing_address", 
                    "notes", "item_list", "item_total", "tax", "add_charges", "grand_total", "status", "send_email", "download", "terms"]

        



    def update(self, instance, validated_data):
        # instance.first_name = validated_data["first_name"]
        # instance.last_name = validated_data["last_name"]
        # instance.address = validated_data["address"]
        # instance.email = validated_data["email"]
        # instance.phone_number = validated_data["phone_number"]
        instance.customer = Customer.objects.get(id=validated_data['customer_id'])
        # instance.taxable = validated_data["taxable"]
        # instance.receipt_pref = validated_data["receipt_pref"]
        # instance.logo_path = validated_data["logo_path"]
        instance.receipt_date = validated_data["receipt_date"]
        instance.po_number = validated_data["po_number"]
        instance.due_date = validated_data["due_date"]
        instance.ship_to = validated_data["ship_to"]
        instance.shipping_address = validated_data["shipping_address"]
        instance.bill_to = validated_data["bill_to"]
        instance.billing_address = validated_data["billing_address"]
        instance.notes = validated_data["notes"]
        instance.terms = validated_data["terms"]
        
        item_list = self.validated_data['item_list']
        ids = [int(i['id']) for i in item_list]
        quantities = [int(i['quantity']) for i in item_list]

        instance.item_list = ids
        instance.quantity_list = quantities


        instance.item_total = validated_data["item_total"]
        instance.tax = validated_data["tax"]
        instance.add_charges = validated_data["add_charges"]
        instance.grand_total = validated_data["grand_total"]

        instance.save()

        # if self.validated_data['send_email']:
        #     # for sending email when creating a new document
        #     file_name = f"Receipt for {instance.email}.pdf"
        #     get_report(file_name)
        #     body = "Attached to the email is the receipt of your transaction on https://www.clappe.com"
        #     subject = "Transaction Receipt"
        #     send_my_email(Invoice.email, body, subject, file_name)
            
        # date, docuemnt_type, document_id, task_type [one time or periodic], email
        schedule_details = {
            "date": instance.due_date,
            "document_type": "receipt",
            "document_id": instance.id,
            "task_type": "one_time",
            "email": instance.customer.email
        }
        new_schedule = ScheduleForm(schedule_details)
        if new_schedule.is_valid():
            _ = new_schedule.update()

        return instance






class PayReceiptSerializer(ModelSerializer):
    receipt_id = serializers.IntegerField()
    required_error = "{fieldname} is required."
    blank_error = "{fieldname} can not be blank."
    class Meta:
        model = PayReceipt
        fields = ["payment_type", "paid_date", "paid_amount", "payment_method", "reference", "receipt_id"]
        


    def save(self):

        try:
            receipt = Receipt.objects.get(id=self.validated_data['receipt_id'])
        except Exception as e:
            print(e)
            return None

        pay_receipt = PayReceipt()
        pay_receipt.payment_type = self.validated_data["payment_type"]
        pay_receipt.paid_date = self.validated_data["paid_date"]
        pay_receipt.paid_amount = self.validated_data["paid_amount"]
        pay_receipt.payment_method = self.validated_data["payment_method"]
        pay_receipt.reference = self.validated_data["reference"]

        receipt.status = "Paid"
        receipt.save()
        pay_receipt.receipt = receipt
        

        pay_receipt.save()

        return pay_receipt













################################################# delivery note ############################################################################

class DNCreateSerializer(ModelSerializer):
    item_list = serializers.ListField(required=True)
    send_email = serializers.BooleanField(required=True)
    download = serializers.BooleanField(required=True)
    customer_id = serializers.IntegerField(required=True)


    required_error = "{fieldname} is required."
    blank_error = "{fieldname} can not be blank."
    class Meta:
        model = DeliveryNote
        fields = [ "customer_id",
                    "dn_date", "po_number", "due_date", "ship_to", "shipping_address", 
                    "notes", "item_list", "item_total", "tax", "add_charges", "grand_total", "send_email", "download", "terms"]
        
        


    def save(self, request):
        new_delivery = DeliveryNote()
        # new_delivery.first_name = self.validated_data["first_name"]
        # new_delivery.last_name = self.validated_data["last_name"]
        # new_delivery.address = self.validated_data["address"]
        # new_delivery.email = self.validated_data["email"]
        # new_delivery.phone_number = self.validated_data["phone_number"]
        new_delivery.customer = Customer.objects.get(id=self.validated_data['customer_id'])
        # new_delivery.taxable = self.validated_data["taxable"]
        # new_delivery.dn_pref = self.validated_data["dn_pref"]
        # new_delivery.logo_path = self.validated_data["logo_path"]
        new_delivery.dn_number = get_number(request, 'delivery_note')
        new_delivery.dn_date = self.validated_data["dn_date"]
        new_delivery.po_number = self.validated_data["po_number"]
        new_delivery.due_date = self.validated_data["due_date"]
        new_delivery.ship_to = self.validated_data["ship_to"]
        new_delivery.shipping_address = self.validated_data["shipping_address"]
        new_delivery.notes = self.validated_data["notes"]
        new_delivery.terms = self.validated_data["terms"]
        
        item_list = self.validated_data['item_list']
        ids = [int(i['id']) for i in item_list]
        quantities = [int(i['quantity']) for i in item_list]

        new_delivery.item_list = ids
        new_delivery.quantity_list = quantities


        new_delivery.item_total = self.validated_data["item_total"]
        new_delivery.tax = self.validated_data["tax"]
        new_delivery.add_charges = self.validated_data["add_charges"]
        new_delivery.grand_total = self.validated_data["grand_total"]

        new_delivery.vendor = request.user

        new_delivery.save()

        # if self.validated_data['send_email']:
        #     # for sending email when creating a new document
        #     file_name = f"Delivery Note for {new_delivery.email}.pdf"
        #     get_report(file_name)
        #     body = "Attached to the email is the receipt of your transaction on https://www.clappe.com"
        #     subject = "Transaction Receipt"
        #     send_my_email(Invoice.email, body, subject, file_name)
            
        # date, docuemnt_type, document_id, task_type [one time or periodic], email
        schedule_details = {
            "date": new_delivery.due_date,
            "document_type": "delivery_note",
            "document_id": new_delivery.id,
            "task_type": "one_time",
            "email": new_delivery.customer.email
        }

        new_schedule = ScheduleForm(schedule_details)
        if new_schedule.is_valid():
            _, _ = new_schedule.save()

        return new_delivery



class DNSerailizer(serializers.ModelSerializer):
    # customer = CustomerSerializer(read_only=True)
    class Meta:
        model = DeliveryNote
        fields = [
                "id", "customer_id",
                    "dn_number", "dn_date", "po_number", "due_date", "ship_to", "shipping_address", 
                    "notes", "item_list", "quantity_list", "item_total", "tax", "add_charges", "grand_total", "status", "terms"]
        




class DNEditSerializer(ModelSerializer):
    item_list = serializers.ListField(required=True)
    send_email = serializers.BooleanField(required=True)
    download = serializers.BooleanField(required=True)
    customer_id = serializers.IntegerField(required=True)


    required_error = "{fieldname} is required."
    blank_error = "{fieldname} can not be blank."
    class Meta:
        model = DeliveryNote
        fields = [
                "customer_id",
                    "dn_date", "po_number", "due_date", "ship_to", "shipping_address", 
                    "notes", "item_list", "item_total", "tax", "add_charges", "grand_total", "status", "send_email", "download", "terms"]

        



    def update(self, instance, validated_data):
        # instance.first_name = validated_data["first_name"]
        # instance.last_name = validated_data["last_name"]
        # instance.address = validated_data["address"]
        # instance.email = validated_data["email"]
        # instance.phone_number = validated_data["phone_number"]
        instance.customer = Customer.objects.get(id=validated_data['customer_id'])
        # instance.taxable = validated_data["taxable"]
        # instance.dn_pref = validated_data["dn_pref"]
        # instance.logo_path = validated_data["logo_path"]
        instance.dn_date = validated_data["dn_date"]
        instance.po_number = validated_data["po_number"]
        instance.due_date = validated_data["due_date"]
        instance.ship_to = validated_data["ship_to"]
        instance.shipping_address = validated_data["shipping_address"]
        instance.notes = validated_data["notes"]
        instance.terms = validated_data["terms"]
        
        item_list = self.validated_data['item_list']
        ids = [int(i['id']) for i in item_list]
        quantities = [int(i['quantity']) for i in item_list]

        instance.item_list = ids
        instance.quantity_list = quantities


        instance.item_total = validated_data["item_total"]
        instance.tax = validated_data["tax"]
        instance.add_charges = validated_data["add_charges"]
        instance.grand_total = validated_data["grand_total"]

        instance.save()

        # if self.validated_data['send_email']:
        #     # for sending email when creating a new document
        #     file_name = f"Delivery Note for {instance.email}.pdf"
        #     get_report(file_name)
        #     body = "Attached to the email is the receipt of your transaction on https://www.clappe.com"
        #     subject = "Transaction Receipt"
        #     send_my_email(Invoice.email, body, subject, file_name)
            
        # date, docuemnt_type, document_id, task_type [one time or periodic], email
        schedule_details = {
            "date": instance.due_date,
            "document_type": "delivery_note",
            "document_id": instance.id,
            "task_type": "one_time",
            "email": instance.customer.email
        }
        new_schedule = ScheduleForm(schedule_details)
        if new_schedule.is_valid():
            _ = new_schedule.update()

        return instance






class PayDNSerializer(ModelSerializer):
    delivery_id = serializers.IntegerField()
    required_error = "{fieldname} is required."
    blank_error = "{fieldname} can not be blank."
    class Meta:
        model = PayDeliveryNote
        fields = ["payment_type", "paid_date", "paid_amount", "payment_method", "reference", "delivery_id"]
        


    def save(self):

        try:
            delivery = DeliveryNote.objects.get(id=self.validated_data['delivery_id'])
        except Exception as e:
            print(e)
            return None

        pay_delivery = PayDeliveryNote()
        pay_delivery.payment_type = self.validated_data["payment_type"]
        pay_delivery.paid_date = self.validated_data["paid_date"]
        pay_delivery.paid_amount = self.validated_data["paid_amount"]
        pay_delivery.payment_method = self.validated_data["payment_method"]
        pay_delivery.reference = self.validated_data["reference"]

        delivery.status = "Paid"
        delivery.save()
        pay_delivery.delivery_note = delivery
        

        pay_delivery.save()

        return pay_delivery







#################################################### others #####################################################################################

class ProfileSerializer(serializers.Serializer):
    photo_path = serializers.ImageField(required=False)
    logo_path = serializers.ImageField(required=False)
    signature = serializers.ImageField(required=False)
    business_name = serializers.CharField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    address = serializers.CharField(required=False)
    email = serializers.CharField(required=False)
    phone_number = serializers.CharField(required=False)
    phone_number_type = serializers.CharField(required=False)
    other_phone_number = serializers.CharField(required=False)
    fax = serializers.CharField(required=False)
    business_number = serializers.CharField(required=False)
    tax_type = serializers.CharField(required=False)
    tax_rate = serializers.CharField(required=False)

    
    def validate(self, data):
        if "email" in data:
            if MyUsers.objects.filter(email=data['email']).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError("Email Already Exists")

        return data


    def update(self, instance, validated_data):


        instance.business_name = validated_data.get('business_name', instance.business_name)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.address = validated_data.get('address', instance.address)
        instance.email = validated_data.get('email', instance.email)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.phone_number_type = validated_data.get('phone_number_type', instance.phone_number_type)
        instance.other_phone_number = validated_data.get('other_phone_number', instance.other_phone_number)
        instance.fax = validated_data.get('fax', instance.fax)
        instance.business_number = validated_data.get('business_number', instance.business_number)
        instance.tax_type = validated_data.get('tax_type', instance.tax_type)
        instance.tax_rate = validated_data.get('tax_rate', instance.tax_rate)
        
        if "photo_path" in validated_data:
            instance.photo_path = process_picture(validated_data['photo_path'], instance)

        if "logo_path" in validated_data:
            instance.logo_path = process_picture(validated_data['logo_path'], instance, "logo")

        if "signature" in validated_data:
            instance.signature = process_picture(validated_data['signature'], instance, "signature")


        instance.save()

        return instance








class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)
    

    def save(self, request):
        old_password = self.validated_data['old_password']
        new_password = self.validated_data['new_password']
        confirm_password = self.validated_data['confirm_password']

        current_user = MyUsers.objects.get(id=request.user.id)
        if check_password(old_password, current_user.password):
            if new_password == confirm_password:
                current_user.set_password(new_password)
                update_session_auth_hash(request, current_user)
                current_user.save()

                return (200, "Password changed successfully")
            
            else:
                return (400, "New password and confirm password does not match")
        
        else:
            return (404, "Old password is incorrect, check and try again")
        




class PreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUsers
        fields = ["lang_pref", "region", "email_report", "currency"]


    
    def update(self, instance):

        instance.lang_pref = self.validated_data.get("lang_pref", instance.lang_pref)
        instance.region = self.validated_data.get("region", instance.region)
        instance.email_report = self.validated_data.get("email_report", instance.email_report)
        instance.currency = self.validated_data.get("currency", instance.currency)

        instance.save()

        return instance




class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUsers
        fields = ["paypal", "bank_transfer", "e_transfer", "other_payment"]



    def update(self, request):
        current_user = MyUsers.objects.get(id=request.user.id)

        current_user.paypal = self.validated_data.get("paypal", None)
        current_user.bank_transfer = self.validated_data.get("bank_transfer", None)
        current_user.e_transfer = self.validated_data.get("e_transfer", None)
        current_user.other_payment = self.validated_data.get("other_payment", None)


        current_user.save()

        return current_user






def custom_item_serializer(items, quantities):
    total_list = [{"id": a, "quantity": b} for a,b in zip(items, quantities)]
    return total_list



