from typing import List
from rest_framework import serializers
from drf_tweaks.serializers import ModelSerializer
from .models import CreditNote, Customer, Item, MyUsers, Invoice, PayCreditNote, PayQuote, PayReceipt, ProformaInvoice, \
                    Estimate, PurchaseOrder, PayInvoice, PayEstimate, PayProforma, PayPurchaseOrder, Quote, Receipt









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
                    "invoice_pref", "logo_path", "ship_to", "shipping_address", "billing_address", "notes",
                    "invoice_number", "amount"]



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
        new_customer.logo_path = self.validated_data["logo_path"]
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
        instance.logo_path = validated_data["logo_path"]
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
        fields = ["address", "billing_address", "business_name", "email", "first_name", "invoice_pref", "last_name", "logo_path",
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
        instance.logo_path = validated_data["logo_path"]
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
                    "invoice_pref", "logo_path", "ship_to", "shipping_address", "billing_address", "notes", "status",
                    "invoice_number", "amount"]









############################################### invoice ####################################################################


class InvoiceCreate(ModelSerializer):
    required_error = "{fieldname} is required."
    blank_error = "{fieldname} can not be blank."
    class Meta:
        model = Invoice
        fields = [
            "first_name","last_name","address","email","phone_number","taxable","invoice_pref","logo_path","invoice_number",
            "invoice_date","po_number","due_date","ship_to","shipping_address","bill_to","billing_address","notes","items_json",
            "item_total","tax","add_charges","sub_total","discount_type","discount_amount","grand_total"]


    def save(self, request):

        new_invoice = Invoice()
        new_invoice.first_name = self.validated_data["first_name"]
        new_invoice.last_name = self.validated_data["last_name"]
        new_invoice.address = self.validated_data["address"]
        new_invoice.email = self.validated_data["email"]
        new_invoice.phone_number = self.validated_data["phone_number"]
        new_invoice.taxable = self.validated_data["taxable"]
        new_invoice.invoice_pref = self.validated_data["invoice_pref"]
        new_invoice.logo_path = self.validated_data["logo_path"]
        new_invoice.invoice_number = self.validated_data['invoice_number']
        new_invoice.invoice_date = self.validated_data['invoice_date']
        new_invoice.po_number = self.validated_data['po_number']
        new_invoice.due_date = self.validated_data['due_date']

        new_invoice.ship_to = self.validated_data["ship_to"]
        new_invoice.shipping_address = self.validated_data["shipping_address"]
        new_invoice.bill_to = self.validated_data["bill_to"]
        new_invoice.billing_address = self.validated_data["billing_address"]
        new_invoice.notes = self.validated_data["notes"]

        new_invoice.items_json = self.validated_data['items_json']
        new_invoice.item_total = self.validated_data["item_total"]
        new_invoice.tax = self.validated_data["tax"]
        new_invoice.add_charges = self.validated_data["add_charges"]
        new_invoice.sub_total = self.validated_data["sub_total"]
        new_invoice.discount_type = self.validated_data["discount_type"]
        new_invoice.discount_amount = self.validated_data["discount_amount"]
        new_invoice.grand_total = self.validated_data["grand_total"]
        
        new_invoice.vendor = request.user

        new_invoice.save()

        return new_invoice





class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = [ "id",
            "first_name","last_name","address","email","phone_number","taxable","invoice_pref","logo_path","invoice_number",
            "invoice_date","po_number","due_date","ship_to","shipping_address","bill_to","billing_address","notes","items_json",
            "item_total","tax","add_charges","sub_total","discount_type","discount_amount","grand_total", "status"]







class InvoiceEditSerializer(ModelSerializer):
    required_error = "{fieldname} is required."
    blank_error = "{fieldname} can not be blank."
    class Meta:
        model = Invoice
        fields = [
            "first_name","last_name","address","email","phone_number","taxable","invoice_pref","logo_path","invoice_number",
            "invoice_date","po_number","due_date","ship_to","shipping_address","bill_to", "billing_address", "notes", "items_json",
            "item_total","tax","add_charges","sub_total","discount_type","discount_amount","grand_total", "status"]


    def update(self, instance, validated_data):
        instance.first_name = validated_data["first_name"]
        instance.last_name = validated_data["last_name"]
        instance.address = validated_data["address"]
        instance.email = validated_data["email"]
        instance.phone_number = validated_data["phone_number"]
        instance.taxable = validated_data["taxable"]
        instance.invoice_pref = validated_data["invoice_pref"]
        instance.logo_path = validated_data["logo_path"]
        instance.invoice_number = validated_data['invoice_number']
        instance.invoice_date = validated_data['invoice_date']
        instance.po_number = validated_data['po_number']
        instance.due_date = validated_data['due_date']

        instance.ship_to = validated_data["ship_to"]
        instance.shipping_address = validated_data["shipping_address"]
        instance.bill_to = validated_data["bill_to"]
        instance.billing_address = validated_data["billing_address"]
        instance.notes = validated_data["notes"]

        instance.items_json = validated_data['items_json']
        instance.item_total = validated_data["item_total"]
        instance.tax = validated_data["tax"]
        instance.add_charges = validated_data["add_charges"]
        instance.sub_total = validated_data["sub_total"]
        instance.discount_type = validated_data["discount_type"]
        instance.discount_amount = validated_data["discount_amount"]
        instance.grand_total = validated_data["grand_total"]


        instance.save()

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
    required_error = "{fieldname} is required."
    blank_error = "{fieldname} can not be blank."
    class Meta:
        model = ProformaInvoice
        fields = [
                "first_name", "last_name", "address", "email", "phone_number", "taxable", "invoice_pref", "logo_path", 
                    "invoice_number", "invoice_date", "po_number", "due_date", "notes", "attachment_path", "items_json", 
                    "item_total", "tax", "add_charges", "grand_total"]


    def save(self, request):
        new_proforma = ProformaInvoice()
        new_proforma.first_name = self.validated_data["first_name"]
        new_proforma.last_name = self.validated_data["last_name"]
        new_proforma.address = self.validated_data["address"]
        new_proforma.email = self.validated_data["email"]
        new_proforma.phone_number = self.validated_data["phone_number"]
        new_proforma.taxable = self.validated_data["taxable"]
        new_proforma.invoice_pref = self.validated_data["invoice_pref"]
        new_proforma.logo_path = self.validated_data["logo_path"]
        new_proforma.invoice_number = self.validated_data["invoice_number"]
        new_proforma.invoice_date = self.validated_data["invoice_date"]
        new_proforma.po_number = self.validated_data["po_number"]
        new_proforma.due_date = self.validated_data["due_date"]
        new_proforma.notes = self.validated_data["notes"]
        new_proforma.attachment_path = self.validated_data["attachment_path"]
        new_proforma.items_json = self.validated_data["items_json"]
        new_proforma.item_total = self.validated_data["item_total"]
        new_proforma.tax = self.validated_data["tax"]
        new_proforma.add_charges = self.validated_data["add_charges"]
        new_proforma.grand_total = self.validated_data["grand_total"]

        new_proforma.vendor = request.user

        new_proforma.save()

        return new_proforma



class ProformerInvoiceSerailizer(serializers.ModelSerializer):
    class Meta:
        model = ProformaInvoice
        fields = [
                "id", "first_name", "last_name", "address", "email", "phone_number", "taxable", "invoice_pref", "logo_path", 
                    "invoice_number", "invoice_date", "po_number", "due_date", "notes", "attachment_path", "items_json", 
                    "item_total", "tax", "add_charges", "grand_total", "status"]




class ProformaEditSerializer(ModelSerializer):
    required_error = "{fieldname} is required."
    blank_error = "{fieldname} can not be blank."
    class Meta:
        model = ProformaInvoice
        fields = [
                "first_name", "last_name", "address", "email", "phone_number", "taxable", "invoice_pref", "logo_path", 
                    "invoice_number", "invoice_date", "po_number", "due_date", "notes", "attachment_path", "items_json", 
                    "item_total", "tax", "add_charges", "grand_total", "status"]




    def update(self, instance, validated_data):
        instance.first_name = validated_data["first_name"]
        instance.last_name = validated_data["last_name"]
        instance.address = validated_data["address"]
        instance.email = validated_data["email"]
        instance.phone_number = validated_data["phone_number"]
        instance.taxable = validated_data["taxable"]
        instance.invoice_pref = validated_data["invoice_pref"]
        instance.logo_path = validated_data["logo_path"]
        instance.invoice_number = validated_data["invoice_number"]
        instance.invoice_date = validated_data["invoice_date"]
        instance.po_number = validated_data["po_number"]
        instance.due_date = validated_data["due_date"]
        instance.notes = validated_data["notes"]
        instance.attachment_path = validated_data["attachment_path"]
        instance.items_json = validated_data["items_json"]
        instance.item_total = validated_data["item_total"]
        instance.tax = validated_data["tax"]
        instance.add_charges = validated_data["add_charges"]
        instance.grand_total = validated_data["grand_total"]

        instance.save()

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
    required_error = "{fieldname} is required."
    blank_error = "{fieldname} can not be blank."
    class Meta:
        model = PurchaseOrder
        fields = [
                "first_name", "last_name", "address", "email", "phone_number", "taxable", "po_pref", "logo_path", 
                    "po_number", "po_date", "ship_to", "notes", "shipping_address", "items_json", 
                    "item_total", "tax", "add_charges", "grand_total"]



    def save(self, request):
        new_purchaseorder = PurchaseOrder()
        new_purchaseorder.first_name = self.validated_data["first_name"]
        new_purchaseorder.last_name = self.validated_data["last_name"]
        new_purchaseorder.address = self.validated_data["address"]
        new_purchaseorder.email = self.validated_data["email"]
        new_purchaseorder.phone_number = self.validated_data["phone_number"]
        new_purchaseorder.taxable = self.validated_data["taxable"]
        new_purchaseorder.po_pref = self.validated_data["po_pref"]
        new_purchaseorder.logo_path = self.validated_data["logo_path"]
        new_purchaseorder.po_number = self.validated_data["po_number"]
        new_purchaseorder.po_date = self.validated_data["po_date"]
        new_purchaseorder.ship_to = self.validated_data["ship_to"]
        new_purchaseorder.notes = self.validated_data["notes"]
        new_purchaseorder.shipping_address = self.validated_data["shipping_address"]
        new_purchaseorder.items_json = self.validated_data["items_json"]
        new_purchaseorder.item_total = self.validated_data["item_total"]
        new_purchaseorder.tax = self.validated_data["tax"]
        new_purchaseorder.add_charges = self.validated_data["add_charges"]
        new_purchaseorder.grand_total = self.validated_data["grand_total"]

        new_purchaseorder.vendor = request.user

        new_purchaseorder.save()

        return new_purchaseorder



class PurchaseOrderSerailizer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = [
                "id", "first_name", "last_name", "address", "email", "phone_number", "taxable", "po_pref", "logo_path", 
                    "po_number", "po_date", "ship_to", "notes", "shipping_address", "items_json", 
                    "item_total", "tax", "add_charges", "grand_total",  "status"]




class PurchaseEditSerializer(ModelSerializer):
    required_error = "{fieldname} is required."
    blank_error = "{fieldname} can not be blank."
    class Meta:
        model = PurchaseOrder
        fields = [
                "first_name", "last_name", "address", "email", "phone_number", "taxable", "po_pref", "logo_path", 
                    "po_number", "po_date", "ship_to", "notes", "shipping_address", "items_json", 
                    "item_total", "tax", "add_charges", "grand_total", "status"]




    def update(self, instance, validated_data):
        instance.first_name = validated_data["first_name"]
        instance.last_name = validated_data["last_name"]
        instance.address = validated_data["address"]
        instance.email = validated_data["email"]
        instance.phone_number = validated_data["phone_number"]
        instance.taxable = validated_data["taxable"]
        instance.po_pref = validated_data["po_pref"]
        instance.logo_path = validated_data["logo_path"]
        instance.po_number = validated_data["po_number"]
        instance.po_date = validated_data["po_date"]
        instance.notes = validated_data["notes"]
        instance.items_json = validated_data["items_json"]
        instance.item_total = validated_data["item_total"]
        instance.tax = validated_data["tax"]
        instance.add_charges = validated_data["add_charges"]
        instance.grand_total = validated_data["grand_total"]

        instance.save()

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
    required_error = "{fieldname} is required."
    blank_error = "{fieldname} can not be blank."
    class Meta:
        model = Estimate
        fields = [
                "first_name", "last_name", "address", "email", "phone_number", "taxable", "estimate_pref", "logo_path", 
                    "estimate_number", "estimate_date", "ship_to", "shipping_address", "bill_to", "billing_address",
                    "notes", "items_json", "item_total", "tax", "add_charges", "grand_total"]


    def save(self, request):
        new_estimate = Estimate()
        new_estimate.first_name = self.validated_data["first_name"]
        new_estimate.last_name = self.validated_data["last_name"]
        new_estimate.address = self.validated_data["address"]
        new_estimate.email = self.validated_data["email"]
        new_estimate.phone_number = self.validated_data["phone_number"]
        new_estimate.taxable = self.validated_data["taxable"]
        new_estimate.estimate_pref = self.validated_data["estimate_pref"]
        new_estimate.logo_path = self.validated_data["logo_path"]
        new_estimate.estimate_number = self.validated_data["estimate_number"]
        new_estimate.estimate_date = self.validated_data["estimate_date"]
        new_estimate.ship_to = self.validated_data["ship_to"]
        new_estimate.shipping_address = self.validated_data["shipping_address"]
        new_estimate.bill_to = self.validated_data["bill_to"]
        new_estimate.billing_address = self.validated_data["billing_address"]
        new_estimate.notes = self.validated_data["notes"]
        new_estimate.items_json = self.validated_data["items_json"]
        new_estimate.item_total = self.validated_data["item_total"]
        new_estimate.tax = self.validated_data["tax"]
        new_estimate.add_charges = self.validated_data["add_charges"]
        new_estimate.grand_total = self.validated_data["grand_total"]

        new_estimate.vendor = request.user

        new_estimate.save()

        return new_estimate



class EstimateSerailizer(serializers.ModelSerializer):
    class Meta:
        model = Estimate
        fields = [
                "id", "first_name", "last_name", "address", "email", "phone_number", "taxable", "estimate_pref", "logo_path", 
                    "estimate_number", "estimate_date", "ship_to", "shipping_address", "bill_to", "billing_address",
                    "notes", "items_json", "item_total", "tax", "add_charges", "grand_total", "status"]
        




class EstimateEditSerializer(ModelSerializer):
    required_error = "{fieldname} is required."
    blank_error = "{fieldname} can not be blank."
    class Meta:
        model = Estimate
        fields = [
                "first_name", "last_name", "address", "email", "phone_number", "taxable", "estimate_pref", "logo_path", 
                    "estimate_number", "estimate_date", "ship_to", "shipping_address", "bill_to", "billing_address",
                    "notes", "items_json", "item_total", "tax", "add_charges", "grand_total", "status"]



    def update(self, instance, validated_data):
        instance.first_name = validated_data["first_name"]
        instance.last_name = validated_data["last_name"]
        instance.address = validated_data["address"]
        instance.email = validated_data["email"]
        instance.phone_number = validated_data["phone_number"]
        instance.taxable = validated_data["taxable"]
        instance.estimate_pref = validated_data["estimate_pref"]
        instance.logo_path = validated_data["logo_path"]
        instance.estimate_number = validated_data["estimate_number"]
        instance.estimate_date = validated_data["estimate_date"]
        instance.ship_to = validated_data["ship_to"]
        instance.shipping_address = validated_data["shipping_address"]
        instance.bill_to = validated_data["bill_to"]
        instance.billing_address = validated_data["billing_address"]
        instance.notes = validated_data["notes"]
        instance.items_json = validated_data["items_json"]
        instance.item_total = validated_data["item_total"]
        instance.tax = validated_data["tax"]
        instance.add_charges = validated_data["add_charges"]
        instance.grand_total = validated_data["grand_total"]

        instance.save()

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







############################################################ quote ##############################################################################


class QuoteCreateSerializer(ModelSerializer):
    required_error = "{fieldname} is required."
    blank_error = "{fieldname} can not be blank."
    class Meta:
        model = Quote
        fields = [ "first_name", "last_name", "address", "email", "phone_number", "taxable", "quote_pref", "logo_path", 
                    "quote_number", "quote_date", "po_number", "ship_to", "shipping_address", "bill_to", "billing_address", 
                    "notes", "items_json", "item_total", "tax", "add_charges", "grand_total"]
                        



    def save(self, request):
        new_quote = Quote()
        new_quote.first_name = self.validated_data["first_name"]
        new_quote.last_name = self.validated_data["last_name"]
        new_quote.address = self.validated_data["address"]
        new_quote.email = self.validated_data["email"]
        new_quote.phone_number = self.validated_data["phone_number"]
        new_quote.taxable = self.validated_data["taxable"]
        new_quote.quote_pref = self.validated_data["quote_pref"]
        new_quote.logo_path = self.validated_data["logo_path"]
        new_quote.quote_number = self.validated_data["quote_number"]
        new_quote.quote_date = self.validated_data["quote_date"]
        new_quote.po_number = self.validated_data["po_number"]
        new_quote.ship_to = self.validated_data["ship_to"]
        new_quote.shipping_address = self.validated_data["shipping_address"]
        new_quote.bill_to = self.validated_data["bill_to"]
        new_quote.billing_address = self.validated_data["billing_address"]
        new_quote.notes = self.validated_data["notes"]
        new_quote.items_json = self.validated_data["items_json"]
        new_quote.item_total = self.validated_data["item_total"]
        new_quote.tax = self.validated_data["tax"]
        new_quote.add_charges = self.validated_data["add_charges"]
        new_quote.grand_total = self.validated_data["grand_total"]

        new_quote.vendor = request.user

        new_quote.save()

        return new_quote



class QuoteSerailizer(serializers.ModelSerializer):
    class Meta:
        model = Quote
        fields = [
                "id", "first_name", "last_name", "address", "email", "phone_number", "taxable", "quote_pref", "logo_path", 
                    "quote_number", "quote_date", "po_number", "ship_to", "shipping_address", "bill_to", "billing_address", 
                    "notes", "items_json", "item_total", "tax", "add_charges", "grand_total", "status"]
        




class QuoteEditSerializer(ModelSerializer):
    required_error = "{fieldname} is required."
    blank_error = "{fieldname} can not be blank."
    class Meta:
        model = Quote
        fields = [
                "first_name", "last_name", "address", "email", "phone_number", "taxable", "quote_pref", "logo_path", 
                    "quote_number", "quote_date", "po_number", "ship_to", "shipping_address", "bill_to", "billing_address", 
                    "notes", "items_json", "item_total", "tax", "add_charges", "grand_total", "status"]
        



    def update(self, instance, validated_data):
        instance.first_name = validated_data["first_name"]
        instance.last_name = validated_data["last_name"]
        instance.address = validated_data["address"]
        instance.email = validated_data["email"]
        instance.phone_number = validated_data["phone_number"]
        instance.taxable = validated_data["taxable"]
        instance.quote_pref = validated_data["quote_pref"]
        instance.logo_path = validated_data["logo_path"]
        instance.quote_number = validated_data["quote_number"]
        instance.quote_date = validated_data["quote_date"]
        instance.po_number = validated_data["po_number"]
        instance.ship_to = validated_data["ship_to"]
        instance.shipping_address = validated_data["shipping_address"]
        instance.bill_to = validated_data["bill_to"]
        instance.billing_address = validated_data["billing_address"]
        instance.notes = validated_data["notes"]
        instance.items_json = validated_data["items_json"]
        instance.item_total = validated_data["item_total"]
        instance.tax = validated_data["tax"]
        instance.add_charges = validated_data["add_charges"]
        instance.grand_total = validated_data["grand_total"]

        instance.save()

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
    required_error = "{fieldname} is required."
    blank_error = "{fieldname} can not be blank."
    class Meta:
        model = CreditNote
        fields = [ "first_name", "last_name", "address", "email", "phone_number", "taxable", "cn_pref", "logo_path", 
                    "cn_number", "cn_date", "po_number", "due_date", "ship_to", "shipping_address", "notes", "items_json", 
                    "item_total", "tax", "add_charges", "grand_total"]       

        


    def save(self, request):
        new_credit = CreditNote()
        new_credit.first_name = self.validated_data["first_name"]
        new_credit.last_name = self.validated_data["last_name"]
        new_credit.address = self.validated_data["address"]
        new_credit.email = self.validated_data["email"]
        new_credit.phone_number = self.validated_data["phone_number"]
        new_credit.taxable = self.validated_data["taxable"]
        new_credit.cn_pref = self.validated_data["cn_pref"]
        new_credit.logo_path = self.validated_data["logo_path"]
        new_credit.cn_number = self.validated_data["cn_number"]
        new_credit.cn_date = self.validated_data["cn_date"]
        new_credit.po_number = self.validated_data["po_number"]
        new_credit.due_date = self.validated_data["due_date"]
        new_credit.ship_to = self.validated_data["ship_to"]
        new_credit.shipping_address = self.validated_data["shipping_address"]
        new_credit.notes = self.validated_data["notes"]
        new_credit.items_json = self.validated_data["items_json"]
        new_credit.item_total = self.validated_data["item_total"]
        new_credit.tax = self.validated_data["tax"]
        new_credit.add_charges = self.validated_data["add_charges"]
        new_credit.grand_total = self.validated_data["grand_total"]

        new_credit.vendor = request.user

        new_credit.save()

        return new_credit



class CreditNoteSerailizer(serializers.ModelSerializer):
    class Meta:
        model = CreditNote
        fields = [
                "id", "first_name", "last_name", "address", "email", "phone_number", "taxable", "cn_pref", "logo_path", 
                    "cn_number", "cn_date", "po_number", "due_date", "ship_to", "shipping_address", "notes", "items_json", 
                    "item_total", "tax", "add_charges", "grand_total", "status"]
        




class CNEditSerializer(ModelSerializer):
    required_error = "{fieldname} is required."
    blank_error = "{fieldname} can not be blank."
    class Meta:
        model = CreditNote
        fields = [
                "first_name", "last_name", "address", "email", "phone_number", "taxable", "cn_pref", "logo_path", 
                    "cn_number", "cn_date", "po_number", "due_date", "ship_to", "shipping_address", "notes", "items_json", 
                    "item_total", "tax", "add_charges", "grand_total", "status"]

        



    def update(self, instance, validated_data):
        instance.first_name = validated_data["first_name"]
        instance.last_name = validated_data["last_name"]
        instance.address = validated_data["address"]
        instance.email = validated_data["email"]
        instance.phone_number = validated_data["phone_number"]
        instance.taxable = validated_data["taxable"]
        instance.cn_pref = validated_data["cn_pref"]
        instance.logo_path = validated_data["logo_path"]
        instance.cn_number = validated_data["cn_number"]
        instance.cn_date = validated_data["cn_date"]
        instance.po_number = validated_data["po_number"]
        instance.due_date = validated_data["due_date"]
        instance.ship_to = validated_data["ship_to"]
        instance.shipping_address = validated_data["shipping_address"]
        instance.notes = validated_data["notes"]
        instance.items_json = validated_data["items_json"]
        instance.item_total = validated_data["item_total"]
        instance.tax = validated_data["tax"]
        instance.add_charges = validated_data["add_charges"]
        instance.grand_total = validated_data["grand_total"]

        instance.save()

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
    required_error = "{fieldname} is required."
    blank_error = "{fieldname} can not be blank."
    class Meta:
        model = Receipt
        fields = [ "first_name", "last_name", "address", "email", "phone_number", "taxable", "receipt_pref", "logo_path", 
                    "receipt_number", "receipt_date", "po_number", "due_date", "ship_to", "shipping_address", "bill_to", "billing_address", 
                    "notes", "items_json", "item_total", "tax", "add_charges", "grand_total"]
        
        


    def save(self, request):
        new_receipt = Receipt()
        new_receipt.first_name = self.validated_data["first_name"]
        new_receipt.last_name = self.validated_data["last_name"]
        new_receipt.address = self.validated_data["address"]
        new_receipt.email = self.validated_data["email"]
        new_receipt.phone_number = self.validated_data["phone_number"]
        new_receipt.taxable = self.validated_data["taxable"]
        new_receipt.receipt_pref = self.validated_data["receipt_pref"]
        new_receipt.logo_path = self.validated_data["logo_path"]
        new_receipt.receipt_number = self.validated_data["receipt_number"]
        new_receipt.receipt_date = self.validated_data["receipt_date"]
        new_receipt.po_number = self.validated_data["po_number"]
        new_receipt.due_date = self.validated_data["due_date"]
        new_receipt.ship_to = self.validated_data["ship_to"]
        new_receipt.shipping_address = self.validated_data["shipping_address"]
        new_receipt.bill_to = self.validated_data["bill_to"]
        new_receipt.billing_address = self.validated_data["billing_address"]
        new_receipt.notes = self.validated_data["notes"]
        new_receipt.items_json = self.validated_data["items_json"]
        new_receipt.item_total = self.validated_data["item_total"]
        new_receipt.tax = self.validated_data["tax"]
        new_receipt.add_charges = self.validated_data["add_charges"]
        new_receipt.grand_total = self.validated_data["grand_total"]

        new_receipt.vendor = request.user

        new_receipt.save()

        return new_receipt



class ReceiptSerailizer(serializers.ModelSerializer):
    class Meta:
        model = Receipt
        fields = [
                "id", "first_name", "last_name", "address", "email", "phone_number", "taxable", "receipt_pref", "logo_path", 
                    "receipt_number", "receipt_date", "po_number", "due_date", "ship_to", "shipping_address", "bill_to", "billing_address", 
                    "notes", "items_json", "item_total", "tax", "add_charges", "grand_total", "status"]
        




class ReceiptEditSerializer(ModelSerializer):
    required_error = "{fieldname} is required."
    blank_error = "{fieldname} can not be blank."
    class Meta:
        model = Receipt
        fields = [
                "first_name", "last_name", "address", "email", "phone_number", "taxable", "receipt_pref", "logo_path", 
                    "receipt_number", "receipt_date", "po_number", "due_date", "ship_to", "shipping_address", "bill_to", "billing_address", 
                    "notes", "items_json", "item_total", "tax", "add_charges", "grand_total", "status"]

        



    def update(self, instance, validated_data):
        instance.first_name = validated_data["first_name"]
        instance.last_name = validated_data["last_name"]
        instance.address = validated_data["address"]
        instance.email = validated_data["email"]
        instance.phone_number = validated_data["phone_number"]
        instance.taxable = validated_data["taxable"]
        instance.receipt_pref = validated_data["receipt_pref"]
        instance.logo_path = validated_data["logo_path"]
        instance.receipt_number = validated_data["receipt_number"]
        instance.receipt_date = validated_data["receipt_date"]
        instance.po_number = validated_data["po_number"]
        instance.due_date = validated_data["due_date"]
        instance.ship_to = validated_data["ship_to"]
        instance.shipping_address = validated_data["shipping_address"]
        instance.bill_to = validated_data["bill_to"]
        instance.billing_address = validated_data["billing_address"]
        instance.notes = validated_data["notes"]
        instance.items_json = validated_data["items_json"]
        instance.item_total = validated_data["item_total"]
        instance.tax = validated_data["tax"]
        instance.add_charges = validated_data["add_charges"]
        instance.grand_total = validated_data["grand_total"]

        instance.save()

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
