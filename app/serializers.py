from rest_framework import serializers
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import check_password
from drf_tweaks.serializers import ModelSerializer

from .models import CreditNote, Customer, DeliveryNote, Item, MyUsers, Invoice, PayCreditNote, PayDeliveryNote,\
                    PayQuote, PayReceipt, ProformaInvoice, Estimate, PurchaseOrder, PayInvoice, PayEstimate, \
                    PayProforma, PayPurchaseOrder, Quote, Receipt, PDFTemplate

from .forms import set_tasks, set_recurring_task
from .utils import delete_tasks, get_sku, upload_pdf_template, validate_add_charges, validate_discount_amount,validate_item_list,\
                    validate_recurring, validate_tax, password_validator, process_picture, get_number
import pycountry




class SignUpSerializer(ModelSerializer):
    password = serializers.CharField(min_length=8, validators=[password_validator])
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

    photo_path = serializers.ImageField(required=False)
    logo_path = serializers.ImageField(required=False)
    signature = serializers.ImageField(required=False)

    class Meta:
        model = MyUsers
        fields = ["photo_path","logo_path","signature","business_name","first_name","last_name","address","email","phone_number",
                    "phone_number_type","other_phone_number","fax","business_number","tax_type","tax_rate","lang_pref","region",
                    "email_report","currency","paypal","bank_transfer","e_transfer","other_payment"]














class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)














############################################### customer #############################################################################


class CustomerSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    business_name = serializers.CharField(required=True)
    address = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)
    phone_number_type = serializers.CharField(required=True)
    taxable = serializers.BooleanField(required=True)
    invoice_pref = serializers.CharField(required=False)
    pdf_template = serializers.CharField(required=False)

    ship_to = serializers.CharField(required=False)
    shipping_address = serializers.CharField(required=False)
    bill_to = serializers.CharField(required=False)
    billing_address = serializers.CharField(required=False)
    notes = serializers.CharField(required=False)
    terms = serializers.CharField(required=False)

    logo = serializers.ImageField(required=False)


    def save(self, request):
        new_customer = Customer()
        new_customer.first_name = self.validated_data["first_name"]
        new_customer.last_name = self.validated_data["last_name"]
        new_customer.business_name = self.validated_data["business_name"]
        new_customer.address = self.validated_data["address"]
        new_customer.email = self.validated_data["email"]
        new_customer.phone_number = self.validated_data["phone_number"]
        new_customer.phone_number_type = self.validated_data["phone_number_type"]
        new_customer.taxable = self.validated_data["taxable"]
        new_customer.invoice_pref = self.validated_data["invoice_pref"]
        new_customer.pdf_template = self.validated_data["pdf_template"]
        
        new_customer.ship_to = self.validated_data["ship_to"]
        new_customer.shipping_address = self.validated_data["shipping_address"]
        new_customer.billing_address = self.validated_data["billing_address"]
        new_customer.bill_to = self.validated_data["bill_to"]
        new_customer.notes = self.validated_data.get("notes", "")
        new_customer.terms = self.validated_data.get("terms", "")

        new_customer.vendor = request.user

        # upload logo
        if "logo" in self.validated_data:
            new_customer.logo = process_picture(self.validated_data['logo'], new_customer, "logo")

        new_customer.save()
        

        return new_customer



    def update(self, instance, validated_data):
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.business_name = validated_data.get("business_name", instance.business_name)
        instance.address = validated_data.get("address", instance.address)
        instance.email = validated_data.get("email", instance.email)
        instance.phone_number = validated_data.get("phone_number", instance.phone_number)
        instance.phone_number_type = validated_data.get("phone_number_type", instance.phone_number_type)
        instance.taxable = validated_data.get("taxable", instance.taxable)
        instance.invoice_pref = validated_data.get("invoice_pref", instance.invoice_pref)
        instance.pdf_template = validated_data.get("pdf_template", instance.pdf_template)
        
        instance.ship_to = validated_data.get("ship_to", instance.ship_to)
        instance.shipping_address = validated_data.get("shipping_address", instance.shipping_address)
        instance.billing_address = validated_data.get("billing_address", instance.billing_address)
        instance.bill_to = validated_data.get("bill_to", instance.bill_to)
        instance.notes = validated_data.get("notes", instance.notes)
        instance.terms = validated_data.get("terms", instance.terms)


        # upload logo
        if "logo" in validated_data:
            instance.logo = process_picture(validated_data['logo'], instance, "logo")

        instance.save()

        return instance





class CustomerDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["id", "first_name", "last_name", "business_name", "address", "email", "phone_number", "phone_number_type", 
                    "taxable", "invoice_pref", "logo", "pdf_template", "ship_to", "shipping_address", "billing_address", 
                    "bill_to", "notes", "terms", "status", "date_created" ]









###################################################### items ########################################################

class ItemSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Item
        fields = ["id", "name", "description", "cost_price", "sales_price", "sales_tax", "sku"]







class CreateItemSerializer(ModelSerializer):
    user_id = serializers.IntegerField()
    cost_price = serializers.CharField(required=True)
    sales_price = serializers.CharField(required=True)
    sales_tax = serializers.CharField(required=False, allow_blank=True, allow_null=True)


    required_error = "{fieldname} is required."
    blank_error = "{fieldname} can not be blank."
    class Meta:
        model = Item
        fields = ["name", "description", "cost_price", "sales_price", "sales_tax", "user_id"]

    
    def validate(self, data):
        name_count = Item.objects.filter(name=data['name']).filter(vendor__id=data['user_id']).count()
        if name_count > 0:
            raise serializers.ValidationError({"name":["Item with this name already exists"]})

        return data

    def validate_cost_price(self, value):
        try:
            return int(value)
        except Exception as e:
            raise serializers.ValidationError("A valid number is required for cost price")

    def validate_sales_price(self, value):
        try:
            return int(value)
        except Exception as e:
            raise serializers.ValidationError("A valid number is required for sales price")
    
    def validate_sales_tax(self, value):
        if len(value) > 0:
            try:
                return float(value)
            except Exception as e:
                raise serializers.ValidationError("A valid decimal number is required for sales tax")
        else:
            return 0.0

    
    def save(self, request):
        new_item = Item()
        new_item.name = self.validated_data['name']
        new_item.description = self.validated_data.get('description', "")
        new_item.cost_price = self.validated_data['cost_price']
        new_item.sales_price = self.validated_data['sales_price']
        new_item.sales_tax = self.validated_data['sales_tax']

        new_item.sku = self.validated_data.get("sku", get_sku())

        new_item.vendor = request.user

        new_item.save()

        return new_item


    def update(self, instance):
        instance.name = self.validated_data.get('name', instance.name)
        instance.description = self.validated_data.get('description', instance.description)
        instance.cost_price = self.validated_data.get('cost_price', instance.cost_price)
        instance.sales_price = self.validated_data.get('sales_price', instance.sales_price)
        instance.sales_tax = self.validated_data.get('sales_tax', instance.sales_tax)

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
    
    item_list = serializers.ListField(required=True, validators=[validate_item_list])
    tax = serializers.CharField(required=False, allow_blank=True, allow_null=True, validators=[validate_tax])
    add_charges = serializers.CharField(required=False, allow_blank=True, allow_null=True,validators=[validate_add_charges])
    discount_amount = serializers.CharField(required=False, allow_blank=True, allow_null=True, validators=[validate_discount_amount])
    recurring = serializers.DictField(validators = [validate_recurring], allow_empty=True, default={})
    pdf_number = serializers.CharField(required=False)
    send_email = serializers.BooleanField(required=True)
    download = serializers.BooleanField(required=True)
    customer_id= serializers.IntegerField(required=True)

    required_error = "{fieldname} is required."
    blank_error = "{fieldname} can not be blank."
    
    class Meta:
        model = Invoice
        fields = [
            "customer_id", "po_number","due_date","ship_to","shipping_address","bill_to","billing_address","notes","item_list",
            "item_total","tax","add_charges","sub_total","discount_type","discount_amount","grand_total", "send_email", "download", "terms",
            "invoice_date", "recurring", "pdf_number"]


    def validate(self, data):
        if not data.get("invoice_date"):
            raise serializers.ValidationError("Invoice date is required")

        download = data['download']
        send_email = data['send_email']
        pdf_number = data.get("pdf_number", None)
        if download or send_email:
            if not pdf_number:
                raise serializers.ValidationError("If you want to download or send email, you have to choose a pdf template")
            else:
                if len(pdf_number) < 8:
                    raise serializers.ValidationError("Pass a valid pdf number")
        
        return data


    def save(self, request):

        new_invoice = Invoice()
        new_invoice.customer = Customer.objects.get(id=self.validated_data['customer_id'])

        new_invoice.invoice_number = get_number(request, 'invoice')
        new_invoice.invoice_date = self.validated_data['invoice_date']
        new_invoice.po_number = self.validated_data.get('po_number', 0)
        new_invoice.due_date = self.validated_data['due_date']

        new_invoice.ship_to = self.validated_data.get("ship_to", "")
        new_invoice.shipping_address = self.validated_data.get("shipping_address", "")
        new_invoice.bill_to = self.validated_data.get("bill_to", "")
        new_invoice.billing_address = self.validated_data.get("billing_address", "")
        new_invoice.notes = self.validated_data.get("notes", "")
        new_invoice.terms = self.validated_data.get("terms", "")


        item_list = self.validated_data['item_list']
        ids = [int(i['id']) for i in item_list]
        quantities = [int(i['quantity']) for i in item_list]

        new_invoice.item_list = ids
        new_invoice.quantity_list = quantities

        new_invoice.item_total = self.validated_data["item_total"]
        tax = self.validated_data.get("tax", 0)
        if tax == '':
            tax = 0
        new_invoice.tax = tax

        add_charges = self.validated_data.get("add_charges", 0)
        if add_charges == '':
            add_charges = 0
        new_invoice.add_charges = add_charges
        
        new_invoice.sub_total = self.validated_data["sub_total"]
        new_invoice.discount_type = self.validated_data["discount_type"]
        new_invoice.discount_amount = self.validated_data.get("discount_amount", 0)
        new_invoice.grand_total = self.validated_data["grand_total"]

        new_invoice.status = "New"
        new_invoice.vendor = request.user
        new_invoice.save()

        set_tasks(new_invoice, "invoice", True)

        recurring_data = self.validated_data['recurring']

        if len(recurring_data) > 0:
            new_invoice.recurring_data = recurring_data
            new_invoice.recurring = True
        else:
            new_invoice.recurring = False

        new_invoice.save()

        if len(recurring_data) > 0:
            set_recurring_task(new_invoice, "invoice", "save")




        return new_invoice





class InvoiceSerializer(DynamicFieldsModelSerializer):
    customer = CustomerDetailsSerializer(read_only=True)
    class Meta:
        model = Invoice
        fields = [ "id", "customer","invoice_number",
            "invoice_date","po_number","due_date","ship_to","shipping_address","bill_to","billing_address","notes", "quantity_list",
            "item_total","tax","add_charges","sub_total","discount_type","discount_amount","grand_total", "status", "item_list", "notes", "terms",
            "recurring", "recurring_data"]






class InvoiceEditSerializer(ModelSerializer):
    customer_id = serializers.IntegerField(required=True)
    send_email = serializers.BooleanField(required=True)
    download = serializers.BooleanField(required=True)

    item_list = serializers.ListField(required=True, validators=[validate_item_list])
    tax = serializers.CharField(required=False, allow_blank=True, allow_null=True, validators=[validate_tax])
    add_charges = serializers.CharField(required=False, allow_blank=True, allow_null=True,validators=[validate_add_charges])
    discount_amount = serializers.CharField(required=False, allow_blank=True, allow_null=True, validators=[validate_discount_amount])
    recurring = serializers.DictField(validators = [validate_recurring], allow_empty=True, default={})
    pdf_number = serializers.CharField(required=False)

    required_error = "{fieldname} is required."
    blank_error = "{fieldname} can not be blank."
    class Meta:
        model = Invoice
        fields = ["customer_id", "invoice_date","po_number","due_date","ship_to","shipping_address","bill_to", "billing_address", "notes", "item_list",
                    "item_total","tax","add_charges","sub_total","discount_type","discount_amount","grand_total", "status", "send_email", "download", "terms",
                    "recurring", "pdf_number"]

    def validate(self, data):
        if not data.get("invoice_date"):
            raise serializers.ValidationError("Invoice date is required")

        download = data['download']
        send_email = data['send_email']
        pdf_number = data.get("pdf_number", None)
        if download or send_email:
            if not pdf_number:
                raise serializers.ValidationError("If you want to download or send email, you have to choose a pdf template")
            else:
                if len(pdf_number) < 8:
                    raise serializers.ValidationError("Pass a valid pdf number")
        return data




    def update(self, instance, validated_data, request):
        instance.customer = Customer.objects.get(id=validated_data['customer_id'])

        instance.invoice_date = validated_data.get('invoice_date', instance.invoice_date)
        instance.po_number = validated_data.get('po_number', instance.po_number)
        instance.due_date = validated_data.get('due_date', instance.due_date)

        instance.ship_to = validated_data.get("ship_to", instance.ship_to)
        instance.shipping_address = validated_data.get("shipping_address", instance.shipping_address)
        instance.bill_to = validated_data.get("bill_to", instance.bill_to)
        instance.billing_address = validated_data.get("billing_address", instance.billing_address)
        instance.notes = validated_data.get("notes", instance.notes)
        instance.terms = validated_data.get("terms", instance.terms)

        item_list = validated_data['item_list']
        ids = [int(i['id']) for i in item_list]
        quantities = [int(i['quantity']) for i in item_list]

        instance.item_list = ids
        instance.quantity_list = quantities


        instance.item_total = validated_data.get("item_total", instance.item_total)
        tax = self.validated_data.get("tax", 0)
        if tax == '':
            tax = instance.tax
        instance.tax = tax
        
        add_charges = self.validated_data.get("add_charges", 0)
        if add_charges == '':
            add_charges = instance.add_charges
        instance.add_charges = add_charges
        
        instance.sub_total = validated_data.get("sub_total", instance.sub_total)
        instance.discount_type = validated_data.get("discount_type", instance.discount_type)
        instance.discount_amount = validated_data.get("discount_amount", instance.discount_amount)
        instance.grand_total = validated_data.get("grand_total", instance.grand_total)


        instance.save()


        set_tasks(instance, "invoice", False)

        recurring_data = self.validated_data['recurring']

        if len(recurring_data) > 0:
            instance.recurring_data = recurring_data
            instance.recurring = True
        else:
            instance.recurring = False

        instance.save()

        if len(recurring_data) > 0:
            set_recurring_task(instance, "invoice", "update")


        return instance

        



class PayInvoiceSerializer(ModelSerializer):
    invoice_id = serializers.IntegerField()
    required_error = "{fieldname} is required."
    blank_error = "{fieldname} can not be blank."
    class Meta:
        model = PayInvoice
        fields = ["payment_type", "paid_date", "paid_amount", "payment_method", "reference", "invoice_id"]


    def save(self, invoice):

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

        delete_tasks(invoice.customer.email, "invoice", invoice.id)

        return pay_invoice










######################################### proforma invoice #########################################################################

class ProformaCreateSerializer(ModelSerializer):
    send_email = serializers.BooleanField(required=True)
    download = serializers.BooleanField(required=True)
    customer_id = serializers.IntegerField(required=True)

    item_list = serializers.ListField(required=True, validators=[validate_item_list])
    tax = serializers.CharField(required=False, allow_blank=True, allow_null=True, validators=[validate_tax])
    add_charges = serializers.CharField(required=False, allow_blank=True, allow_null=True,validators=[validate_add_charges])
    recurring = serializers.DictField(validators = [validate_recurring], allow_empty=True, default={})
    pdf_number = serializers.CharField(required=False)


    required_error = "{fieldname} is required."
    blank_error = "{fieldname} can not be blank."
    class Meta:
        model = ProformaInvoice
        fields = [
                "customer_id", "recurring", "invoice_date", "po_number", "due_date", "notes", "item_list", "item_total", "tax", \
                "add_charges", "grand_total", "send_email", "download", "terms", "pdf_number", "bill_to", "billing_address", \
                "ship_to", "shipping_address"]

    def validate(self, data):
        if not data.get("invoice_date"):
            raise serializers.ValidationError("Invoice date is required")

        download = data['download']
        send_email = data['send_email']
        pdf_number = data.get("pdf_number", None)
        if download or send_email:
            if not pdf_number:
                raise serializers.ValidationError("If you want to download or send email, you have to choose a pdf template")
            else:
                if len(pdf_number) < 8:
                    raise serializers.ValidationError("Pass a valid pdf number")

        return data



    def save(self, request):
        new_proforma = ProformaInvoice()
        new_proforma.customer = Customer.objects.get(id=self.validated_data['customer_id'])
        new_proforma.invoice_number = get_number(request, 'proforma')
        new_proforma.invoice_date = self.validated_data["invoice_date"]
        new_proforma.po_number = self.validated_data.get('po_number', 0)
        new_proforma.due_date = self.validated_data["due_date"]
        new_proforma.notes = self.validated_data.get("notes", "")
        new_proforma.terms = self.validated_data.get("terms", "")

        new_proforma.bill_to = self.validated_data.get("bill_to", "")
        new_proforma.billing_address = self.validated_data.get("billing_address", "")
        new_proforma.ship_to = self.validated_data.get("ship_to", "")
        new_proforma.shipping_address = self.validated_data.get("shipping_address", "")
        
        item_list = self.validated_data['item_list']
        ids = [int(i['id']) for i in item_list]
        quantities = [int(i['quantity']) for i in item_list]

        new_proforma.item_list = ids
        new_proforma.quantity_list = quantities


        new_proforma.item_total = self.validated_data["item_total"]
        tax = self.validated_data.get("tax", 0)
        if tax == '':
            tax = 0
        new_proforma.tax = tax
        
        add_charges = self.validated_data.get("add_charges", 0)
        if add_charges == '':
            add_charges = 0
        new_proforma.add_charges = add_charges
        
        new_proforma.grand_total = self.validated_data["grand_total"]
        
        new_proforma.status = "New"

        new_proforma.vendor = request.user

        new_proforma.save()

        set_tasks(new_proforma, "proforma invoice", True)

        recurring_data = self.validated_data['recurring']

        if len(recurring_data) > 0:
            new_proforma.recurring_data = recurring_data
            new_proforma.recurring = True
        else:
            new_proforma.recurring = False

        new_proforma.save()

        if len(recurring_data) > 0:
            set_recurring_task(new_proforma, "proforma invoice", "save")

        return new_proforma



class ProformerInvoiceSerailizer(DynamicFieldsModelSerializer):
    customer = CustomerDetailsSerializer(read_only=True)
    class Meta:
        model = ProformaInvoice
        fields = [
                "id", "customer", 
                    "invoice_number", "invoice_date", "po_number", "due_date", "notes", "item_list", "quantity_list",
                    "item_total", "tax", "add_charges", "grand_total", "status", "terms", "recurring", "recurring_data",
                    "bill_to", "billing_address", "ship_to", "shipping_address"]




class ProformaEditSerializer(ModelSerializer):
    send_email = serializers.BooleanField(required=True)
    download = serializers.BooleanField(required=True)
    customer_id = serializers.IntegerField(required=True)

    item_list = serializers.ListField(required=True, validators=[validate_item_list])
    tax = serializers.CharField(required=False, allow_blank=True, allow_null=True, validators=[validate_tax])
    add_charges = serializers.CharField(required=False, allow_blank=True, allow_null=True,validators=[validate_add_charges])
    recurring = serializers.DictField(validators = [validate_recurring], allow_empty=True, default={})
    pdf_number = serializers.CharField(required=False)

    required_error = "{fieldname} is required."
    blank_error = "{fieldname} can not be blank."
    class Meta:
        model = ProformaInvoice
        fields = ["customer_id", "invoice_date", "po_number", "due_date", "notes", "item_list", "item_total", "tax", "add_charges",
                    "grand_total", "status", "send_email", "download", "terms", "recurring", "pdf_number", "bill_to", "billing_address", 
                    "ship_to", "shipping_address"]


    def validate(self, data):
        if not data.get("invoice_date"):
            raise serializers.ValidationError("Invoice date is required")

        download = data['download']
        send_email = data['send_email']
        pdf_number = data.get("pdf_number", None)
        if download or send_email:
            if not pdf_number:
                raise serializers.ValidationError("If you want to download or send email, you have to choose a pdf template")
            else:
                if len(pdf_number) < 8:
                    raise serializers.ValidationError("Pass a valid pdf number")
        
        return data


    def update(self, instance, validated_data):
        instance.customer = Customer.objects.get(id=validated_data['customer_id'])
        instance.invoice_date = validated_data.get("invoice_date", instance.invoice_date)
        instance.po_number = validated_data.get("po_number", instance.po_number)
        instance.due_date = validated_data.get("due_date", instance.due_date)
        instance.notes = validated_data.get("notes", instance.notes)
        instance.terms = validated_data.get("terms", instance.terms)

        instance.bill_to = validated_data.get("bill_to", instance.bill_to)
        instance.billing_address = validated_data.get("billing_address", instance.billing_address)
        instance.ship_to = validated_data.get("ship_to", instance.ship_to)
        instance.shipping_address = validated_data.get("shipping_address", instance.shipping_address)
        
        item_list = self.validated_data['item_list']
        ids = [int(i['id']) for i in item_list]
        quantities = [int(i['quantity']) for i in item_list]

        instance.item_list = ids
        instance.quantity_list = quantities


        instance.item_total = validated_data.get("item_total", instance.item_total)
        tax = self.validated_data.get("tax", 0)
        if tax == '':
            tax = instance.tax
        instance.tax = tax
        
        add_charges = self.validated_data.get("add_charges", 0)
        if add_charges == '':
            add_charges = instance.add_charges
        instance.add_charges = add_charges
        
        instance.grand_total = validated_data.get("grand_total", instance.grand_total)

        instance.save()

        set_tasks(instance, "proforma invoice", False)

        recurring_data = self.validated_data['recurring']

        if len(recurring_data) > 0:
            instance.recurring_data = recurring_data
            instance.recurring = True
        else:
            instance.recurring = False

        instance.save()

        if len(recurring_data) > 0:
            set_recurring_task(instance, "proforma invoice", "update")

        return instance






class PayProformaSerializer(ModelSerializer):
    proforma_id = serializers.IntegerField()
    required_error = "{fieldname} is required."
    blank_error = "{fieldname} can not be blank."
    class Meta:
        model = PayProforma
        fields = ["payment_type", "paid_date", "paid_amount", "payment_method", "reference", "proforma_id"]


    def save(self, proforma):

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

        delete_tasks(proforma.customer.email, "proforma invoice", proforma.id)

        return pay_proforma












############################################## purchase order ########################################################################

class PurchaseCreateSerializer(ModelSerializer):
    send_email = serializers.BooleanField(required=True)
    download = serializers.BooleanField(required=True)
    customer_id = serializers.IntegerField(required=True)

    item_list = serializers.ListField(required=True, validators=[validate_item_list])
    tax = serializers.CharField(required=False, allow_blank=True, allow_null=True, validators=[validate_tax])
    add_charges = serializers.CharField(required=False, allow_blank=True, allow_null=True,validators=[validate_add_charges])
    recurring = serializers.DictField(validators = [validate_recurring], allow_empty=True, default={})
    pdf_number = serializers.CharField(required=False)


    required_error = "{fieldname} is required."
    blank_error = "{fieldname} can not be blank."
    class Meta:
        model = PurchaseOrder
        fields = [
                "customer_id", "po_date", "ship_to", "notes", "shipping_address", "bill_to", "billing_address", "item_list", "due_date",
                    "item_total", "tax", "add_charges", "grand_total", "send_email", "download", "terms", "recurring", "pdf_number"]


    def validate(self, data):
        download = data['download']
        send_email = data['send_email']
        pdf_number = data.get("pdf_number", None)
        if download or send_email:
            if not pdf_number:
                raise serializers.ValidationError("If you want to download or send email, you have to choose a pdf template")
            else:
                if len(pdf_number) < 8:
                    raise serializers.ValidationError("Pass a valid pdf number")

        return data


    def save(self, request):
        new_purchaseorder = PurchaseOrder()
        new_purchaseorder.customer = Customer.objects.get(id=self.validated_data['customer_id'])
        new_purchaseorder.po_number = get_number(request, 'purchase_order')
        new_purchaseorder.po_date = self.validated_data["po_date"]
        new_purchaseorder.due_date = self.validated_data["due_date"]
        new_purchaseorder.ship_to = self.validated_data.get("ship_to", "")
        new_purchaseorder.notes = self.validated_data.get("notes", "")
        new_purchaseorder.shipping_address = self.validated_data.get("shipping_address", "")
        new_purchaseorder.terms = self.validated_data.get("terms", "")
        new_purchaseorder.bill_to = self.validated_data.get("bill_to", "")
        new_purchaseorder.billing_address = self.validated_data.get("billing_address", "")
        
        item_list = self.validated_data['item_list']
        ids = [int(i['id']) for i in item_list]
        quantities = [int(i['quantity']) for i in item_list]

        new_purchaseorder.item_list = ids
        new_purchaseorder.quantity_list = quantities


        new_purchaseorder.item_total = self.validated_data["item_total"]
        tax = self.validated_data.get("tax", 0)
        if tax == '':
            tax = 0
        new_purchaseorder.tax = tax
    
        add_charges = self.validated_data.get("add_charges", 0)
        if add_charges == '':
            add_charges = 0
        new_purchaseorder.add_charges = add_charges
    
        new_purchaseorder.grand_total = self.validated_data["grand_total"]
        
        
        new_purchaseorder.status = "New"

        new_purchaseorder.vendor = request.user

        new_purchaseorder.save()


        set_tasks(new_purchaseorder, "purchase order", True)

        recurring_data = self.validated_data['recurring']

        if len(recurring_data) > 0:
            new_purchaseorder.recurring_data = recurring_data
            new_purchaseorder.recurring = True
        else:
            new_purchaseorder.recurring = False

        new_purchaseorder.save()

        if len(recurring_data) > 0:
            set_recurring_task(new_purchaseorder, "purchase order", "save")

        return new_purchaseorder



class PurchaseOrderSerailizer(DynamicFieldsModelSerializer):
    customer = CustomerDetailsSerializer(read_only=True)
    class Meta:
        model = PurchaseOrder
        fields = [
                "id", "customer", 
                    "po_number", "po_date", "due_date", "ship_to", "notes", "shipping_address", "bill_to", "billing_address",
                    "item_list", "quantity_list",
                    "item_total", "tax", "add_charges", "grand_total",  "status", "terms", "recurring", "recurring_data"]







class PurchaseEditSerializer(ModelSerializer):
    send_email = serializers.BooleanField(required=True)
    download = serializers.BooleanField(required=True)
    customer_id = serializers.IntegerField(required=True)

    item_list = serializers.ListField(required=True, validators=[validate_item_list])
    tax = serializers.CharField(required=False, allow_blank=True, allow_null=True, validators=[validate_tax])
    add_charges = serializers.CharField(required=False, allow_blank=True, allow_null=True,validators=[validate_add_charges])
    recurring = serializers.DictField(validators = [validate_recurring], allow_empty=True, default={})
    pdf_number = serializers.CharField(required=False)



    required_error = "{fieldname} is required."
    blank_error = "{fieldname} can not be blank."
    class Meta:
        model = PurchaseOrder
        fields = ["customer_id", "po_date", "due_date", "ship_to", "notes", "shipping_address", "bill_to", "billing_address",
                     "item_list", 
                    "item_total", "tax", "add_charges", "grand_total", "status", "send_email", "download", "terms",
                    "recurring", "pdf_number"]
    
    def validate(self, data):
        download = data['download']
        send_email = data['send_email']
        pdf_number = data.get("pdf_number", None)
        if download or send_email:
            if not pdf_number:
                raise serializers.ValidationError("If you want to download or send email, you have to choose a pdf template")
            else:
                if len(pdf_number) < 8:
                    raise serializers.ValidationError("Pass a valid pdf number")
        return data



    def update(self, instance, validated_data):
        instance.customer = Customer.objects.get(id=validated_data['customer_id'])
        instance.po_date = validated_data.get("po_date", instance.po_date)
        instance.notes = validated_data.get("notes", instance.notes)
        instance.terms = validated_data.get("terms", instance.terms)
        instance.ship_to = validated_data.get("ship_to", instance.ship_to)
        instance.shipping_address = validated_data.get("shipping_address", instance.shipping_address)
        instance.bill_to = validated_data.get("bill_to", instance.bill_to)
        instance.billing_address = validated_data.get("billing_address", instance.billing_address)
        
        item_list = self.validated_data['item_list']
        ids = [int(i['id']) for i in item_list]
        quantities = [int(i['quantity']) for i in item_list]

        instance.item_list = ids
        instance.quantity_list = quantities


        instance.item_total = validated_data.get("item_total", instance.item_total)
        tax = self.validated_data.get("tax", 0)
        if tax == '':
            tax = instance.tax
        instance.tax = tax
        
        add_charges = self.validated_data.get("add_charges", 0)
        if add_charges == '':
            add_charges = instance.add_charges
        instance.add_charges = add_charges
        
        instance.grand_total = validated_data.get("grand_total", instance.grand_total)

        instance.save()

        set_tasks(instance, "purchase order", False)

        recurring_data = self.validated_data['recurring']

        if len(recurring_data) > 0:
            instance.recurring_data = recurring_data
            instance.recurring = True
        else:
            instance.recurring = False

        instance.save()

        if len(recurring_data) > 0:
            print("trying to get recurring")
            set_recurring_task(instance, "purchase order", "update")

        return instance






class PayPurchaseSerializer(ModelSerializer):
    purchase_id = serializers.IntegerField()
    required_error = "{fieldname} is required."
    blank_error = "{fieldname} can not be blank."
    class Meta:
        model = PayPurchaseOrder
        fields = ["payment_type", "paid_date", "paid_amount", "payment_method", "reference", "purchase_id"]


    def save(self, purchase_order):

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

        delete_tasks(purchase_order.customer.email, "purchase order", purchase_order.id)

        return pay_purchase







############################################ estimate ########################################################################

class EstimateCreateSerializer(ModelSerializer):
    send_email = serializers.BooleanField(required=True)
    download = serializers.BooleanField(required=True)
    customer_id = serializers.IntegerField(required=True)

    item_list = serializers.ListField(required=True, validators=[validate_item_list])
    tax = serializers.CharField(required=False, allow_blank=True, allow_null=True, validators=[validate_tax])
    add_charges = serializers.CharField(required=False, allow_blank=True, allow_null=True,validators=[validate_add_charges])
    recurring = serializers.DictField(validators = [validate_recurring], allow_empty=True, default={})
    pdf_number = serializers.CharField(required=False)


    required_error = "{fieldname} is required."
    blank_error = "{fieldname} can not be blank."
    class Meta:
        model = Estimate
        fields = [
                "customer_id", "due_date", "po_number", "recurring",
                    "estimate_date", "ship_to", "shipping_address", "bill_to", "billing_address", "pdf_number",
                    "notes", "item_list", "item_total", "tax", "add_charges", "grand_total", "send_email", "download", "terms"]
    
    def validate(self, data):
        download = data['download']
        send_email = data['send_email']
        pdf_number = data.get("pdf_number", None)
        if download or send_email:
            if not pdf_number:
                raise serializers.ValidationError("If you want to download or send email, you have to choose a pdf template")
            else:
                if len(pdf_number) < 8:
                    raise serializers.ValidationError("Pass a valid pdf number")

        return data

    def save(self, request):
        new_estimate = Estimate()
        new_estimate.customer = Customer.objects.get(id=self.validated_data['customer_id'])
        new_estimate.estimate_number = get_number(request, 'estimate')
        new_estimate.estimate_date = self.validated_data["estimate_date"]
        new_estimate.po_number = self.validated_data.get("po_number", 0)
        new_estimate.due_date = self.validated_data["due_date"]
        new_estimate.ship_to = self.validated_data.get("ship_to", "")
        new_estimate.shipping_address = self.validated_data.get("shipping_address", "")
        new_estimate.bill_to = self.validated_data.get("bill_to", "")
        new_estimate.billing_address = self.validated_data.get("billing_address", "")
        new_estimate.notes = self.validated_data.get("notes", "")
        new_estimate.terms = self.validated_data.get("terms", "")
        
        item_list = self.validated_data['item_list']
        print(item_list)
        ids = [int(i['id']) for i in item_list]
        quantities = [int(i['quantity']) for i in item_list]

        new_estimate.item_list = ids
        new_estimate.quantity_list = quantities


        new_estimate.item_total = self.validated_data["item_total"]
        tax = self.validated_data.get("tax", 0)
        if tax == '':
            tax = 0
        new_estimate.tax = tax

        add_charges = self.validated_data.get("add_charges", 0)
        if add_charges == '':
            add_charges = 0
        new_estimate.add_charges = add_charges

        new_estimate.grand_total = self.validated_data["grand_total"]

        
        new_estimate.status = "Pending"

        new_estimate.vendor = request.user

        new_estimate.save()

        recurring_data = self.validated_data['recurring']

        if len(recurring_data) > 0:
            new_estimate.recurring_data = recurring_data
            new_estimate.recurring = True
        else:
            new_estimate.recurring = False

        new_estimate.save()

        if len(recurring_data) > 0:
            set_recurring_task(new_estimate, "estimate", "save")

        set_tasks(new_estimate, "estimate", True)

        return new_estimate






class EstimateSerailizer(DynamicFieldsModelSerializer):
    customer = CustomerDetailsSerializer(read_only=True)
    class Meta:
        model = Estimate
        fields = [
                "id", "customer", "po_number", "due_date", "recurring", "recurring_data",
                    "estimate_number", "estimate_date", "ship_to", "shipping_address", "bill_to", "billing_address",
                    "notes", "item_list", "quantity_list", "item_total", "tax", "add_charges", "grand_total", "status", "terms"]
        


    







class EstimateEditSerializer(ModelSerializer):
    send_email = serializers.BooleanField(required=True)
    download = serializers.BooleanField(required=True)
    customer_id = serializers.IntegerField(required=True)

    item_list = serializers.ListField(required=True, validators=[validate_item_list])
    tax = serializers.CharField(required=False, allow_blank=True, allow_null=True, validators=[validate_tax])
    add_charges = serializers.CharField(required=False, allow_blank=True, allow_null=True,validators=[validate_add_charges])
    recurring = serializers.DictField(validators = [validate_recurring], allow_empty=True, default={})
    pdf_number = serializers.CharField(required=False)


    required_error = "{fieldname} is required."
    blank_error = "{fieldname} can not be blank."
    class Meta:
        model = Estimate
        fields = ["customer_id", "po_number", "due_date", "estimate_date", "ship_to", "shipping_address", "bill_to", "billing_address",
                    "notes", "item_list", "item_total", "tax", "add_charges", "grand_total", "status", "send_email", "download", "terms",
                    "recurring", "pdf_number"]

    def validate(self, data):
        download = data['download']
        send_email = data['send_email']
        pdf_number = data.get("pdf_number", None)
        if download or send_email:
            if not pdf_number:
                raise serializers.ValidationError("If you want to download or send email, you have to choose a pdf template")
            else:
                if len(pdf_number) < 8:
                    raise serializers.ValidationError("Pass a valid pdf number")
        return data


    def update(self, instance, validated_data):
        instance.customer = Customer.objects.get(id=validated_data['customer_id'])
        instance.estimate_date = validated_data.get("estimate_date", instance.estimate_date)
        instance.due_date = validated_data.get("due_date", instance.due_date)
        instance.po_number = validated_data.get("po_number", instance.po_number)
        instance.ship_to = validated_data.get("ship_to", instance.ship_to)
        instance.shipping_address = validated_data.get("shipping_address", instance.shipping_address)
        instance.bill_to = validated_data.get("bill_to", instance.bill_to)
        instance.billing_address = validated_data.get("billing_address", instance.billing_address)
        instance.notes = validated_data.get("notes", instance.notes)
        instance.terms = validated_data.get("terms", instance.terms)
        
        item_list = self.validated_data['item_list']
        ids = [int(i['id']) for i in item_list]
        quantities = [int(i['quantity']) for i in item_list]

        instance.item_list = ids
        instance.quantity_list = quantities


        instance.item_total = validated_data.get("item_total", instance.item_total)
        tax = self.validated_data.get("tax", 0)
        if tax == '':
            tax = instance.tax
        instance.tax = tax

        add_charges = self.validated_data.get("add_charges", 0)
        if add_charges == '':
            add_charges = instance.add_charges
        instance.add_charges = add_charges

        instance.grand_total = validated_data.get("grand_total", instance.grand_total)

        instance.status = "Pending"

        instance.save()

        set_tasks(instance, "estimate", False)

        recurring_data = self.validated_data['recurring']

        if len(recurring_data) > 0:
            instance.recurring_data = recurring_data
            instance.recurring = True
        else:
            instance.recurring = False

        instance.save()

        if len(recurring_data) > 0:
            set_recurring_task(instance, "estimate", "update")

        return instance






class PayEstimateSerializer(ModelSerializer):
    estimate_id = serializers.IntegerField()
    required_error = "{fieldname} is required."
    blank_error = "{fieldname} can not be blank."
    class Meta:
        model = PayEstimate
        fields = ["payment_type", "paid_date", "paid_amount", "payment_method", "reference", "estimate_id"]


    def save(self, estimate):

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

        delete_tasks(estimate.customer.email, "estimate", estimate.id)

        return pay_estimate








############################################################ quote ##############################################################################


class QuoteCreateSerializer(ModelSerializer):
    send_email = serializers.BooleanField(required=True)
    download = serializers.BooleanField(required=True)
    customer_id = serializers.IntegerField(required=True)

    item_list = serializers.ListField(required=True, validators=[validate_item_list])
    tax = serializers.CharField(required=False, allow_blank=True, allow_null=True, validators=[validate_tax])
    add_charges = serializers.CharField(required=False, allow_blank=True, allow_null=True,validators=[validate_add_charges])
    recurring = serializers.DictField(validators = [validate_recurring], allow_empty=True, default={})
    pdf_number = serializers.CharField(required=False)


    required_error = "{fieldname} is required."
    blank_error = "{fieldname} can not be blank."
    class Meta:
        model = Quote
        fields = [ "customer_id", "due_date", "recurring", "pdf_number",
                    "quote_date", "po_number", "ship_to", "shipping_address", "bill_to", "billing_address", 
                    "notes",  "item_list", "item_total", "tax", "add_charges", "grand_total", "send_email", "download", "terms"]


    def validate(self, data):
        download = data['download']
        send_email = data['send_email']
        pdf_number = data.get("pdf_number", None)
        if download or send_email:
            if not pdf_number:
                raise serializers.ValidationError("If you want to download or send email, you have to choose a pdf template")
            else:
                if len(pdf_number) < 8:
                    raise serializers.ValidationError("Pass a valid pdf number")
        return data


    def save(self, request):
        new_quote = Quote()
        new_quote.customer = Customer.objects.get(id=self.validated_data['customer_id'])
        new_quote.quote_number = get_number(request, 'quote')
        new_quote.quote_date = self.validated_data["quote_date"]
        new_quote.due_date = self.validated_data["due_date"]
        new_quote.po_number = self.validated_data.get('po_number', 0)
        new_quote.ship_to = self.validated_data.get("ship_to", "")
        new_quote.shipping_address = self.validated_data.get("shipping_address", "")
        new_quote.bill_to = self.validated_data.get("bill_to", "")
        new_quote.billing_address = self.validated_data.get("billing_address", "")
        new_quote.notes = self.validated_data.get("notes", "")
        new_quote.terms = self.validated_data.get("terms", "")
        
        item_list = self.validated_data['item_list']
        ids = [int(i['id']) for i in item_list]
        quantities = [int(i['quantity']) for i in item_list]

        new_quote.item_list = ids
        new_quote.quantity_list = quantities


        new_quote.item_total = self.validated_data["item_total"]
        tax = self.validated_data.get("tax", 0)
        if tax == '':
            tax = 0
        new_quote.tax = tax

        add_charges = self.validated_data.get("add_charges", 0)
        if add_charges == '':
            add_charges = 0
        new_quote.add_charges = add_charges

        new_quote.grand_total = self.validated_data["grand_total"]

        
        new_quote.status = "New"

        new_quote.vendor = request.user

        new_quote.save()


        set_tasks(new_quote, "quote", True)

        recurring_data = self.validated_data['recurring']

        if len(recurring_data) > 0:
            new_quote.recurring_data = recurring_data
            new_quote.recurring = True
        else:
            new_quote.recurring = False

        new_quote.save()

        if len(recurring_data) > 0:
            set_recurring_task(new_quote, "quote", "save")

        return new_quote



class QuoteSerailizer(DynamicFieldsModelSerializer):
    customer = CustomerDetailsSerializer(read_only=True)
    class Meta:
        model = Quote
        fields = [
                "id", "customer", "recurring", "recurring_data", "due_date",
                    "quote_number", "quote_date", "po_number", "ship_to", "shipping_address", "bill_to", "billing_address", 
                    "notes", "item_list", "quantity_list", "item_total", "tax", "add_charges", "grand_total", "status", "terms"]







class QuoteEditSerializer(ModelSerializer):
    send_email = serializers.BooleanField(required=True)
    download = serializers.BooleanField(required=True)
    customer_id = serializers.IntegerField(required=True)

    item_list = serializers.ListField(required=True, validators=[validate_item_list])
    tax = serializers.CharField(required=False, allow_blank=True, allow_null=True, validators=[validate_tax])
    add_charges = serializers.CharField(required=False, allow_blank=True, allow_null=True,validators=[validate_add_charges])
    recurring = serializers.DictField(validators = [validate_recurring], allow_empty=True, default={})
    pdf_number = serializers.CharField(required=False)


    required_error = "{fieldname} is required."
    blank_error = "{fieldname} can not be blank."
    class Meta:
        model = Quote
        fields = ["customer_id", "due_date", "quote_date", "po_number", "ship_to", "shipping_address", "bill_to", "billing_address", 
                    "notes", "item_list", "item_total", "tax", "add_charges", "grand_total", "status", "send_email", "download", "terms",
                    "recurring", "pdf_number"]


    def validate(self, data):
        download = data['download']
        send_email = data['send_email']
        pdf_number = data.get("pdf_number", None)
        if download or send_email:
            if not pdf_number:
                raise serializers.ValidationError("If you want to download or send email, you have to choose a pdf template")
            else:
                if len(pdf_number) < 8:
                    raise serializers.ValidationError("Pass a valid pdf number")
        return data


    def update(self, instance, validated_data):
        instance.customer = Customer.objects.get(id=validated_data['customer_id'])
        instance.quote_date = validated_data.get("quote_date", instance.quote_date)
        instance.due_date = validated_data.get("due_date", instance.due_date)
        instance.po_number = validated_data.get("po_number", instance.po_number)
        instance.ship_to = validated_data.get("ship_to", instance.ship_to)
        instance.shipping_address = validated_data.get("shipping_address", instance.shipping_address)
        instance.bill_to = validated_data.get("bill_to", instance.bill_to)
        instance.billing_address = validated_data.get("billing_address", instance.billing_address)
        instance.notes = validated_data.get("notes", instance.notes)
        instance.terms = validated_data.get("terms", instance.terms)
        
        item_list = self.validated_data['item_list']
        ids = [int(i['id']) for i in item_list]
        quantities = [int(i['quantity']) for i in item_list]

        instance.item_list = ids
        instance.quantity_list = quantities


        instance.item_total = validated_data.get("item_total", instance.item_total)
        tax = self.validated_data.get("tax", 0)
        if tax == '':
            tax = instance.tax
        instance.tax = tax
        
        add_charges = self.validated_data.get("add_charges", 0)
        if add_charges == '':
            add_charges = instance.add_charges
        instance.add_charges = add_charges
        
        instance.grand_total = validated_data.get("grand_total", instance.grand_total)

        instance.save()

        set_tasks(instance, "quote", False)

        recurring_data = self.validated_data['recurring']

        if len(recurring_data) > 0:
            instance.recurring_data = recurring_data
            instance.recurring = True
        else:
            instance.recurring = False

        instance.save()

        if len(recurring_data) > 0:
            set_recurring_task(instance, "quote", "update")

        return instance






class PayQuoteSerializer(ModelSerializer):
    quote_id = serializers.IntegerField()
    required_error = "{fieldname} is required."
    blank_error = "{fieldname} can not be blank."
    class Meta:
        model = PayQuote
        fields = ["payment_type", "paid_date", "paid_amount", "payment_method", "reference", "quote_id"]
        


    def save(self, quote):

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

        delete_tasks(quote.customer.email, "quote", quote.id)

        return pay_quote










############################################################ credit note ##############################################################################


class CNCreateSerializer(ModelSerializer):
    send_email = serializers.BooleanField(required=True)
    download = serializers.BooleanField(required=True)
    customer_id = serializers.IntegerField(required=True)

    item_list = serializers.ListField(required=True, validators=[validate_item_list])
    tax = serializers.CharField(required=False, allow_blank=True, allow_null=True, validators=[validate_tax])
    add_charges = serializers.CharField(required=False, allow_blank=True, allow_null=True,validators=[validate_add_charges])
    recurring = serializers.DictField(validators = [validate_recurring], allow_empty=True, default={})
    pdf_number = serializers.CharField(required=False)


    required_error = "{fieldname} is required."
    blank_error = "{fieldname} can not be blank."
    class Meta:
        model = CreditNote
        fields = [ "customer_id", "recurring", "pdf_number",
                    "cn_date", "po_number", "due_date", "ship_to", "shipping_address", "bill_to", "billing_address",
                    "notes", "item_list", 
                    "item_total", "tax", "add_charges", "grand_total", "send_email", "download", "terms"]       

    
    def validate(self, data):
        download = data['download']
        send_email = data['send_email']
        pdf_number = data.get("pdf_number", None)
        if download or send_email:
            if not pdf_number:
                raise serializers.ValidationError("If you want to download or send email, you have to choose a pdf template")
            else:
                if len(pdf_number) < 8:
                    raise serializers.ValidationError("Pass a valid pdf number")
        return data


    def save(self, request):
        new_credit = CreditNote()
        new_credit.customer = Customer.objects.get(id=self.validated_data['customer_id'])
        new_credit.cn_number = get_number(request, 'credit_note')
        new_credit.cn_date = self.validated_data["cn_date"]
        new_credit.po_number = self.validated_data.get('po_number', 0)
        new_credit.due_date = self.validated_data["due_date"]
        new_credit.ship_to = self.validated_data.get("ship_to", "")
        new_credit.shipping_address = self.validated_data.get("shipping_address", "")
        new_credit.bill_to = self.validated_data.get("bill_to", "")
        new_credit.billing_address = self.validated_data.get("billing_address", "")
        new_credit.notes = self.validated_data.get("notes", "")
        new_credit.terms = self.validated_data.get("terms", "")
        
        item_list = self.validated_data['item_list']
        ids = [int(i['id']) for i in item_list]
        quantities = [int(i['quantity']) for i in item_list]

        new_credit.item_list = ids
        new_credit.quantity_list = quantities


        new_credit.item_total = self.validated_data["item_total"]
        tax = self.validated_data.get("tax", 0)
        if tax == '':
            tax = 0
        new_credit.tax = tax

        add_charges = self.validated_data.get("add_charges", 0)
        if add_charges == '':
            add_charges = 0
        new_credit.add_charges = add_charges

        new_credit.grand_total = self.validated_data["grand_total"]

        
        new_credit.status = "New"

        new_credit.vendor = request.user

        new_credit.save()

        set_tasks(new_credit, "credit note", True)

        recurring_data = self.validated_data['recurring']

        if len(recurring_data) > 0:
            new_credit.recurring_data = recurring_data
            new_credit.recurring = True
        else:
            new_credit.recurring = False

        new_credit.save()

        if len(recurring_data) > 0:
            set_recurring_task(new_credit, "credit note", "save")

        return new_credit



class CreditNoteSerailizer(DynamicFieldsModelSerializer):
    customer = CustomerDetailsSerializer(read_only=True)
    class Meta:
        model = CreditNote
        fields = [
                "id", "customer", 
                    "cn_number", "cn_date", "po_number", "due_date", "ship_to", "shipping_address", "notes",  "item_list", "quantity_list", 
                    "item_total", "tax", "add_charges", "grand_total", "status", "terms", "recurring", "recurring_data", 
                    "bill_to", "billing_address"]





class CNEditSerializer(ModelSerializer):
    send_email = serializers.BooleanField(required=True)
    download = serializers.BooleanField(required=True)
    customer_id = serializers.IntegerField(required=True)

    item_list = serializers.ListField(required=True, validators=[validate_item_list])
    tax = serializers.CharField(required=False, allow_blank=True, allow_null=True, validators=[validate_tax])
    add_charges = serializers.CharField(required=False, allow_blank=True, allow_null=True,validators=[validate_add_charges])
    recurring = serializers.DictField(validators = [validate_recurring], allow_empty=True, default={})
    pdf_number = serializers.CharField(required=False)


    required_error = "{fieldname} is required."
    blank_error = "{fieldname} can not be blank."
    class Meta:
        model = CreditNote
        fields = [
                "customer_id", "recurring", "pdf_number", "bill_to", "billing_address",
                    "cn_date", "po_number", "due_date", "ship_to", "shipping_address", "notes", "item_list", 
                    "item_total", "tax", "add_charges", "grand_total", "status", "send_email", "download", "terms"]


    def validate(self, data):
        download = data['download']
        send_email = data['send_email']
        pdf_number = data.get("pdf_number", None)
        if download or send_email:
            if not pdf_number:
                raise serializers.ValidationError("If you want to download or send email, you have to choose a pdf template")
            else:
                if len(pdf_number) < 8:
                    raise serializers.ValidationError("Pass a valid pdf number")
        return data


    def update(self, instance, validated_data):
        instance.customer = Customer.objects.get(id=validated_data['customer_id'])
        instance.cn_date = validated_data.get("cn_date", instance.cn_date)
        instance.po_number = validated_data.get("po_number", instance.po_number)
        instance.due_date = validated_data.get("due_date", instance.due_date)
        instance.ship_to = validated_data.get("ship_to", instance.ship_to)
        instance.shipping_address = validated_data.get("shipping_address", instance.shipping_address)
        instance.bill_to = validated_data.get("bill_to", instance.bill_to)
        instance.billing_address = validated_data.get("billing_address", instance.billing_address)
        instance.notes = validated_data.get("notes", instance.notes)
        instance.terms = validated_data.get("terms", instance.terms)
        
        item_list = self.validated_data['item_list']
        ids = [int(i['id']) for i in item_list]
        quantities = [int(i['quantity']) for i in item_list]

        instance.item_list = ids
        instance.quantity_list = quantities


        instance.item_total = validated_data.get("item_total", instance.item_total)
        tax = self.validated_data.get("tax", 0)
        if tax == '':
            tax = instance.tax
        instance.tax = tax

        add_charges = self.validated_data.get("add_charges", 0)
        if add_charges == '':
            add_charges = instance.add_charges
        instance.add_charges = add_charges

        instance.grand_total = validated_data.get("grand_total", instance.grand_total)

        instance.save()

        set_tasks(instance, "credit note", False)

        recurring_data = self.validated_data['recurring']

        if len(recurring_data) > 0:
            instance.recurring_data = recurring_data
            instance.recurring = True
        else:
            instance.recurring = False

        instance.save()

        if len(recurring_data) > 0:
            set_recurring_task(instance, "credit note", "update")

        return instance






class PayCNSerializer(ModelSerializer):
    credit_id = serializers.IntegerField()
    required_error = "{fieldname} is required."
    blank_error = "{fieldname} can not be blank."
    class Meta:
        model = PayCreditNote
        fields = ["payment_type", "paid_date", "paid_amount", "payment_method", "reference", "credit_id"]
        


    def save(self, credit):

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

        delete_tasks(credit.customer.email, "credit note", credit.id)

        return pay_credit














############################################################ receipt ##############################################################################


class REceiptCreateSerializer(ModelSerializer):
    send_email = serializers.BooleanField(required=True)
    download = serializers.BooleanField(required=True)
    customer_id = serializers.IntegerField(required=True)

    item_list = serializers.ListField(required=True, validators=[validate_item_list])
    tax = serializers.CharField(required=False, allow_blank=True, allow_null=True, validators=[validate_tax])
    add_charges = serializers.CharField(required=False, allow_blank=True, allow_null=True,validators=[validate_add_charges])
    recurring = serializers.DictField(validators = [validate_recurring], allow_empty=True, default={})
    pdf_number = serializers.CharField(required=False)


    required_error = "{fieldname} is required."
    blank_error = "{fieldname} can not be blank."
    class Meta:
        model = Receipt
        fields = [ "customer_id", "recurring", "pdf_number",
                    "receipt_date", "po_number", "due_date", "ship_to", "shipping_address", "bill_to", "billing_address", 
                    "notes", "item_list", "item_total", "tax", "add_charges", "grand_total", "send_email", "download", "terms"]



    def validate(self, data):
        download = data['download']
        send_email = data['send_email']
        pdf_number = data.get("pdf_number", None)
        if download or send_email:
            if not pdf_number:
                raise serializers.ValidationError("If you want to download or send email, you have to choose a pdf template")
            else:
                if len(pdf_number) < 8:
                    raise serializers.ValidationError("Pass a valid pdf number")

        return data




    def save(self, request):
        new_receipt = Receipt()
        new_receipt.customer = Customer.objects.get(id=self.validated_data['customer_id'])
        new_receipt.receipt_number = get_number(request, 'receipt')
        new_receipt.receipt_date = self.validated_data["receipt_date"]
        new_receipt.po_number = self.validated_data.get('po_number', 0)
        new_receipt.due_date = self.validated_data["due_date"]
        new_receipt.ship_to = self.validated_data.get("ship_to", "")
        new_receipt.shipping_address = self.validated_data.get("shipping_address", "")
        new_receipt.bill_to = self.validated_data.get("bill_to", "")
        new_receipt.billing_address = self.validated_data.get("billing_address", "")
        new_receipt.notes = self.validated_data.get("notes", "")
        new_receipt.terms = self.validated_data.get("terms", "")
        
        item_list = self.validated_data['item_list']
        ids = [int(i['id']) for i in item_list]
        quantities = [int(i['quantity']) for i in item_list]

        new_receipt.item_list = ids
        new_receipt.quantity_list = quantities


        new_receipt.item_total = self.validated_data["item_total"]
        tax = self.validated_data.get("tax", 0)
        if tax == '':
            tax = 0
        new_receipt.tax = tax

        add_charges = self.validated_data.get("add_charges", 0)
        if add_charges == '':
            add_charges = 0
        new_receipt.add_charges = add_charges

        new_receipt.grand_total = self.validated_data["grand_total"]

        
        new_receipt.status = "New"

        new_receipt.vendor = request.user

        new_receipt.save()

        set_tasks(new_receipt, "receipt", True)

        recurring_data = self.validated_data['recurring']

        if len(recurring_data) > 0:
            new_receipt.recurring_data = recurring_data
            new_receipt.recurring = True
        else:
            new_receipt.recurring = False

        new_receipt.save()

        if len(recurring_data) > 0:
            set_recurring_task(new_receipt, "receipt", "save")

        return new_receipt



class ReceiptSerailizer(DynamicFieldsModelSerializer):
    customer = CustomerDetailsSerializer(read_only=True)
    class Meta:
        model = Receipt
        fields = [
                "id", "customer", "recurring", "recurring_data",
                    "receipt_number", "receipt_date", "po_number", "due_date", "ship_to", "shipping_address", "bill_to", "billing_address", 
                    "notes", "item_list", "quantity_list", "item_total", "tax", "add_charges", "grand_total", "status", "terms"]










class ReceiptEditSerializer(ModelSerializer):
    send_email = serializers.BooleanField(required=True)
    download = serializers.BooleanField(required=True)
    customer_id = serializers.IntegerField(required=True)

    item_list = serializers.ListField(required=True, validators=[validate_item_list])
    tax = serializers.CharField(required=False, allow_blank=True, allow_null=True, validators=[validate_tax])
    add_charges = serializers.CharField(required=False, allow_blank=True, allow_null=True,validators=[validate_add_charges])
    recurring = serializers.DictField(validators = [validate_recurring], allow_empty=True, default={})
    pdf_number = serializers.CharField(required=False)


    required_error = "{fieldname} is required."
    blank_error = "{fieldname} can not be blank."
    class Meta:
        model = Receipt
        fields = [
                "customer_id", "reucrring", "pdf_number",
                    "receipt_date", "po_number", "due_date", "ship_to", "shipping_address", "bill_to", "billing_address", 
                    "notes", "item_list", "item_total", "tax", "add_charges", "grand_total", "status", "send_email", "download", "terms"]



    def validate(self, data):
        download = data['download']
        send_email = data['send_email']
        pdf_number = data.get("pdf_number", None)
        if download or send_email:
            if not pdf_number:
                raise serializers.ValidationError("If you want to download or send email, you have to choose a pdf template")
            else:
                if len(pdf_number) < 8:
                    raise serializers.ValidationError("Pass a valid pdf number")
        
        return data



    def update(self, instance, validated_data):
        instance.customer = Customer.objects.get(id=validated_data['customer_id'])
        instance.receipt_date = validated_data.get("receipt_date", instance.receipt_date)
        instance.po_number = validated_data.get("po_number", instance.po_number)
        instance.due_date = validated_data.get("due_date", instance.due_date)
        instance.ship_to = validated_data.get("ship_to", instance.ship_to)
        instance.shipping_address = validated_data.get("shipping_address", instance.shipping_address)
        instance.bill_to = validated_data.get("bill_to", instance.bill_to)
        instance.billing_address = validated_data.get("billing_address", instance.billing_address)
        instance.notes = validated_data.get("notes", instance.notes)
        instance.terms = validated_data.get("terms", instance.terms)
        
        item_list = self.validated_data['item_list']
        ids = [int(i['id']) for i in item_list]
        quantities = [int(i['quantity']) for i in item_list]

        instance.item_list = ids
        instance.quantity_list = quantities


        instance.item_total = validated_data.get("item_total", instance.item_total)
        tax = self.validated_data.get("tax", 0)
        if tax == '':
            tax = instance.tax
        instance.tax = tax

        add_charges = self.validated_data.get("add_charges", 0)
        if add_charges == '':
            add_charges = instance.add_charges
        instance.add_charges = add_charges

        instance.grand_total = validated_data.get("grand_total", instance.grand_total)

        instance.save()

        set_tasks(instance, "receipt", False)

        recurring_data = self.validated_data['recurring']

        if len(recurring_data) > 0:
            instance.recurring_data = recurring_data
            instance.recurring = True
        else:
            instance.recurring = False

        instance.save()

        if len(recurring_data) > 0:
            set_recurring_task(instance, "receipt", "update")

        return instance






class PayReceiptSerializer(ModelSerializer):
    receipt_id = serializers.IntegerField()
    required_error = "{fieldname} is required."
    blank_error = "{fieldname} can not be blank."
    class Meta:
        model = PayReceipt
        fields = ["payment_type", "paid_date", "paid_amount", "payment_method", "reference", "receipt_id"]
        


    def save(self, receipt):

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

        delete_tasks(receipt.customer.email, "receipt", receipt.id)

        return pay_receipt













################################################# delivery note ############################################################################

class DNCreateSerializer(ModelSerializer):
    send_email = serializers.BooleanField(required=True)
    download = serializers.BooleanField(required=True)
    customer_id = serializers.IntegerField(required=True)

    item_list = serializers.ListField(required=True, validators=[validate_item_list])
    tax = serializers.CharField(required=False, allow_blank=True, allow_null=True, validators=[validate_tax])
    add_charges = serializers.CharField(required=False, allow_blank=True, allow_null=True,validators=[validate_add_charges])
    recurring = serializers.DictField(validators = [validate_recurring], allow_empty=True, default={})
    pdf_number = serializers.CharField(required=False)


    required_error = "{fieldname} is required."
    blank_error = "{fieldname} can not be blank."
    class Meta:
        model = DeliveryNote
        fields = [ "customer_id", "recurring", "pdf_number",
                    "dn_date", "po_number", "due_date", "ship_to", "shipping_address", "bill_to", "billing_address",
                    "notes", "item_list", "item_total", "tax", "add_charges", "grand_total", "send_email", "download", "terms"]


    def validate(self, data):
        download = data['download']
        send_email = data['send_email']
        pdf_number = data.get("pdf_number", None)
        if download or send_email:
            if not pdf_number:
                raise serializers.ValidationError("If you want to download or send email, you have to choose a pdf template")
            else:
                if len(pdf_number) < 8:
                    raise serializers.ValidationError("Pass a valid pdf number")

        return data




    def save(self, request):
        new_delivery = DeliveryNote()
        new_delivery.customer = Customer.objects.get(id=self.validated_data['customer_id'])
        new_delivery.dn_number = get_number(request, 'delivery_note')
        new_delivery.dn_date = self.validated_data["dn_date"]
        new_delivery.po_number = self.validated_data.get('po_number', 0)
        new_delivery.due_date = self.validated_data["due_date"]
        new_delivery.ship_to = self.validated_data.get("ship_to", "")
        new_delivery.shipping_address = self.validated_data.get("shipping_address", "")
        new_delivery.bill_to = self.validated_data.get("bill_to", "")
        new_delivery.billing_address = self.validated_data.get("billing_address", "")
        new_delivery.notes = self.validated_data.get("notes", "")
        new_delivery.terms = self.validated_data.get("terms", "")
        
        item_list = self.validated_data['item_list']
        ids = [int(i['id']) for i in item_list]
        quantities = [int(i['quantity']) for i in item_list]

        new_delivery.item_list = ids
        new_delivery.quantity_list = quantities


        new_delivery.item_total = self.validated_data["item_total"]
        tax = self.validated_data.get("tax", 0)
        if tax == '':
            tax = 0
        new_delivery.tax = tax

        add_charges = self.validated_data.get("add_charges", 0)
        if add_charges == '':
            add_charges = 0
        new_delivery.add_charges = add_charges

        new_delivery.grand_total = self.validated_data["grand_total"]

        
        new_delivery.status = "New"

        new_delivery.vendor = request.user

        new_delivery.save()

        set_tasks(new_delivery, "delivery note", True)

        recurring_data = self.validated_data['recurring']

        if len(recurring_data) > 0:
            new_delivery.recurring_data = recurring_data
            new_delivery.recurring = True
        else:
            new_delivery.recurring = False

        new_delivery.save()

        if len(recurring_data) > 0:
            set_recurring_task(new_delivery, "delivery note", "save")

        return new_delivery



class DNSerailizer(DynamicFieldsModelSerializer):
    customer = CustomerDetailsSerializer(read_only=True)
    class Meta:
        model = DeliveryNote
        fields = [
                "id", "customer", "recurring", "recurring_data", "bill_to", "billing_address",
                    "dn_number", "dn_date", "po_number", "due_date", "ship_to", "shipping_address", 
                    "notes", "item_list", "quantity_list", "item_total", "tax", "add_charges", "grand_total", "status", "terms"]      









class DNEditSerializer(ModelSerializer):
    send_email = serializers.BooleanField(required=True)
    download = serializers.BooleanField(required=True)
    customer_id = serializers.IntegerField(required=True)

    item_list = serializers.ListField(required=True, validators=[validate_item_list])
    tax = serializers.CharField(required=False, allow_blank=True, allow_null=True, validators=[validate_tax])
    add_charges = serializers.CharField(required=False, allow_blank=True, allow_null=True,validators=[validate_add_charges])
    recurring = serializers.DictField(validators = [validate_recurring], allow_empty=True, default={})
    pdf_number = serializers.CharField(required=False)


    required_error = "{fieldname} is required."
    blank_error = "{fieldname} can not be blank."
    class Meta:
        model = DeliveryNote
        fields = [
                "customer_id", "recurring", "dn_date", "po_number", "due_date", "ship_to", "shipping_address", 
                "notes", "item_list", "item_total", "tax", "add_charges", "grand_total", "status", "send_email", 
                "download", "terms", "pdf_number", "bill_to", "billing_address"]


    def validate(self, data):
        download = data['download']
        send_email = data['send_email']
        pdf_number = data.get("pdf_number", None)
        if download or send_email:
            if not pdf_number:
                raise serializers.ValidationError("If you want to download or send email, you have to choose a pdf template")
            else:
                if len(pdf_number) < 8:
                    raise serializers.ValidationError("Pass a valid pdf number")

        return data




    def update(self, instance, validated_data):
        instance.customer = Customer.objects.get(id=validated_data['customer_id'])
        instance.dn_date = validated_data.get("dn_date", instance.dn_date)
        instance.po_number = validated_data.get("po_number", instance.po_number)
        instance.due_date = validated_data.get("due_date", instance.due_date)
        instance.ship_to = validated_data.get("ship_to", instance.ship_to)
        instance.shipping_address = validated_data.get("shipping_address", instance.shipping_address)
        instance.bill_to = validated_data.get("bill_to", instance.bill_to)
        instance.billing_address = validated_data.get("billing_address", instance.billing_address)
        instance.notes = validated_data.get("notes", instance.notes)
        instance.terms = validated_data.get("terms", instance.terms)
        
        item_list = self.validated_data['item_list']
        ids = [int(i['id']) for i in item_list]
        quantities = [int(i['quantity']) for i in item_list]

        instance.item_list = ids
        instance.quantity_list = quantities


        instance.item_total = validated_data.get("item_total", instance.item_total)
        tax = self.validated_data.get("tax", 0)
        if tax == '':
            tax = instance.tax
        instance.tax = tax
        
        add_charges = self.validated_data.get("add_charges", 0)
        if add_charges == '':
            add_charges = instance.add_charges
        instance.add_charges = add_charges
        
        instance.grand_total = validated_data.get("grand_total", instance.grand_total)

        instance.save()

        set_tasks(instance, "delivery note", False)

        recurring_data = self.validated_data['recurring']

        if len(recurring_data) > 0:
            instance.recurring_data = recurring_data
            instance.recurring = True
        else:
            instance.recurring = False

        instance.save()

        if len(recurring_data) > 0:
            set_recurring_task(instance, "delivery note", "update")

        return instance






class PayDNSerializer(ModelSerializer):
    delivery_id = serializers.IntegerField()
    required_error = "{fieldname} is required."
    blank_error = "{fieldname} can not be blank."
    class Meta:
        model = PayDeliveryNote
        fields = ["payment_type", "paid_date", "paid_amount", "payment_method", "reference", "delivery_id"]
        


    def save(self, delivery):
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

        delete_tasks(delivery.customer.email, "delivery note", delivery.id)

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
        fields = ["lang_pref", "region", "email_report", "currency", "paypal", "bank_transfer", "e_transfer", "other_payment"]


    
    def update(self, instance):

        instance.lang_pref = self.validated_data.get("lang_pref", instance.lang_pref)
        instance.region = self.validated_data.get("region", instance.region)
        instance.email_report = self.validated_data.get("email_report", instance.email_report)
        instance.paypal = self.validated_data.get("paypal", instance.paypal)
        instance.bank_transfer = self.validated_data.get("bank_transfer", instance.bank_transfer)
        instance.e_transfer = self.validated_data.get("e_transfer", instance.e_transfer)
        instance.other_payment = self.validated_data.get("other_payment", instance.other_payment)

        cur = self.validated_data.get("currency", None)
        if cur:
            my_cur = pycountry.currencies.get(name=cur).alpha_3
            instance.currency = my_cur



        instance.save()

        return instance







############################################# pdf endpoint ###############################################################

class UploadPDFTemplate(serializers.Serializer):
    name = serializers.CharField()
    photo_path = serializers.ImageField()


    
    def save(self):
        new_pdf = PDFTemplate()
        new_pdf.name = self.validated_data['name']
        new_pdf.photo_path = upload_pdf_template(self.validated_data["photo_path"], self.validated_data['name'])
        new_pdf.save()

        return new_pdf



class PDFTemplateSerializer(serializers.ModelSerializer):
    photo_path = serializers.ImageField(required=False)
    class Meta:
        model = PDFTemplate
        fields = ['name', 'photo_path']
    