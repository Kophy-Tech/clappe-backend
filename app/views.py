#django imports
from datetime import datetime, timedelta
import os, io
from django.contrib.auth import authenticate
from django.http import FileResponse

#rest_frameworf imports
from rest_framework.decorators import api_view, authentication_classes, permission_classes, parser_classes
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

#import from custom files
from .serializers import CNCreateSerializer, CNEditSerializer, CreateItemSerializer, CreditNoteSerailizer, CustomerCreateSerializer,\
                        CustomerEditSerializer, CustomerSerializer, DNCreateSerializer, DNEditSerializer, DNSerailizer, \
                        EstimateCreateSerializer, EstimateEditSerializer, EstimateSerailizer, InvoiceEditSerializer, \
                        InvoiceSerializer, ItemSerializer, PayCNSerializer, PayDNSerializer, PayEstimateSerializer, PayInvoiceSerializer,\
                        PayQuoteSerializer, PayReceiptSerializer, ProformaCreateSerializer, ProformaEditSerializer, \
                        ProformerInvoiceSerailizer, QuoteCreateSerializer, QuoteEditSerializer, QuoteSerailizer, REceiptCreateSerializer,\
                        ReceiptEditSerializer, ReceiptSerailizer, SignUpSerializer, LoginSerializer, UserSerializer, InvoiceCreate,\
                        PayProformaSerializer, PurchaseCreateSerializer, PurchaseEditSerializer, PurchaseOrderSerailizer, \
                        PayPurchaseSerializer, ProfileSerializer, PasswordChangeSerializer, PreferenceSerializer,\
                        custom_item_serializer, CURRENCY_MAPPING, pdf_item_serializer

from app.pdf.main import get_report
from app.my_email import send_my_email
from .authentication import get_access_token, MyAuthentication
from .models import JWT, CreditNote, Customer, DeliveryNote, Estimate, Invoice, Item, MyUsers, ProformaInvoice, PurchaseOrder, Quote, Receipt












#homepage view
@api_view(['GET'])
def home(request):
    context = {
        'message' : "Home page"
    }
    return Response(context, status=status.HTTP_200_OK)




#signup view
@api_view(['GET', 'POST'])
def signup(request):
    if request.method == 'GET':
        context = {}
        context['message'] = 'Welcome to User signup page, please pass the required fields'
        context['required'] = 'first_name, last_name, password, email, phone_number'
        return Response(context, status=status.HTTP_200_OK)

    if request.method == 'POST':
        serializer = SignUpSerializer(data=request.data)
        context = {}
        if serializer.is_valid():
            new_user = serializer.save()

            context['message'] = 'User created successfully, you can now login with your email and password'
            return Response(context, status=status.HTTP_201_CREATED)

        else:
            errors = {**serializer.errors}
            new_errors = {key: value[0] for key,value in errors.items()}
            errors_list = [k for k in new_errors.values()]
            context = {'message': errors_list[0], 'errors': new_errors}
            return Response(context, status=status.HTTP_400_BAD_REQUEST)



# login view
@api_view(["GET", "POST"])
def login(request):
    context = {}
    if request.method == 'GET':
        context['message'] = 'Welcome to login page, please pass the required fields'
        context['required'] = 'email, password'
        return Response(context, status=status.HTTP_200_OK)



    if request.method == "POST":
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(username=serializer.validated_data['email'], password=serializer.validated_data['password'])
            if user is not None:
                JWT.objects.filter(user_id=user.id).delete()
                access_token = get_access_token({'user_id':user.id})
                JWT.objects.create(user_id=user.id, access=access_token)
                user_serializer = UserSerializer(user)

                context['message'] = 'Login successful!'
                context['first_name'] = user_serializer.data['first_name']
                context['last_name'] = user_serializer.data['last_name']
                context['email'] = user_serializer.data['email']
                context['auth_token '] = access_token

                return Response(context, status=status.HTTP_200_OK)
            else:
                context['message'] = "Invalid login credentials, please check and try again"
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
        else:
            errors = {**serializer.errors}
            new_errors = {key: value[0] for key,value in errors.items()}
            errors_list = [k for k in new_errors.values()]
            context = {'message': errors_list[0], 'errors': new_errors}
            return Response(context, status=status.HTTP_400_BAD_REQUEST)





@api_view(["GET", "POST"])
@authentication_classes((MyAuthentication, ))
@permission_classes((IsAuthenticated, ))
def user_profile(request):
    if request.method == 'GET':
        try:
            user = MyUsers.objects.get(id=request.user.id)
            user_serializer = UserSerializer(user)
            context = {**user_serializer.data}

            return Response(context, status=status.HTTP_200_OK)
        
        except Exception as e:
            print(e)
            context = {'message': "User not found"}
            
            return Response(context, status=status.HTTP_404_NOT_FOUND)









@api_view(["GET", "POST"])
@authentication_classes((MyAuthentication, ))
@permission_classes((IsAuthenticated, ))
def logout(request):
    context = {"message": "logout page"}
    if request.method == "POST":
        access = JWT.objects.get(user_id=request.user.id)
        access.delete()

        #the access token should be deleted from frontend

        context = {'message': 'Logout successful'}
    return Response(context, status=status.HTTP_200_OK)










############################################### customer ####################################################
@api_view(["GET"])
@authentication_classes((MyAuthentication, ))
@permission_classes((IsAuthenticated, ))
def my_customer(request):
    
    all_customers = Customer.objects.filter(vendor=request.user)
    if len(all_customers) > 0:
        serialized_customers = CustomerSerializer(all_customers, many=True)
        context = {"customers": serialized_customers.data}
        return Response(context, status=status.HTTP_200_OK)
    else:
        context = {"message": "You don't have any customer"}
        return Response(context, status=status.HTTP_404_NOT_FOUND)

    






@api_view(["GET", "POST"])
@authentication_classes((MyAuthentication, ))
@permission_classes((IsAuthenticated, ))
def customer(request):

    if request.method == "POST":
        form = CustomerCreateSerializer(data=request.data)
        context = {}

        if form.is_valid():
            new_customer = form.save(request)
            context['message'] = "success"
            context['customer'] = new_customer.first_name + ' ' + new_customer.last_name

            return Response(context, status=status.HTTP_201_CREATED)

        else:
            errors = {**form.errors}
            new_errors = {key: value[0] for key,value in errors.items()}
            errors_list = [k for k in new_errors.values()]
            context = {'message': errors_list[0], 'errors': new_errors}

            return Response(context, status=status.HTTP_400_BAD_REQUEST)
    else:
        context = {"message": "create customer page", "required fields": ["first_name", "last_name", "business_name", "address", "email", "phone_number", "taxable", 
                    "invoice_pref", "logo_path", "ship_to", "shipping_address", "billing_address", "notes", "status",
                    "invoice_number", "amount"]}

        return Response(context, status=status.HTTP_200_OK)











@api_view(["GET", "PUT", "DELETE"])
@authentication_classes((MyAuthentication, ))
@permission_classes((IsAuthenticated, ))
def edit_customer(request, id):
    context = {}

    if request.method == "GET":
        try:
            customer = Customer.objects.get(id=id)
            serialized_customer = CustomerSerializer(customer)
            context['customer'] = serialized_customer.data
            return Response(context, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            context['message'] = "Customer not found"
            return Response(context, status=status.HTTP_404_NOT_FOUND)

        


    if request.method == "PUT":
        customer = Customer.objects.get(id=id)
        form = CustomerEditSerializer(instance=customer, data=request.data)
        context = {}

        if form.is_valid():
            updated_customer = form.update(customer, form.validated_data)
            context['message'] = "success"
            context['id'] = customer.id
            context['customer'] = updated_customer.first_name + ' ' + updated_customer.last_name

            return Response(context, status=status.HTTP_200_OK)

        else:
            errors = {**form.errors}
            new_errors = {key: value[0] for key,value in errors.items()}
            errors_list = [k for k in new_errors.values()]
            context = {'message': errors_list[0], 'errors': new_errors}

            return Response(context, status=status.HTTP_400_BAD_REQUEST)


    if request.method == "DELETE":
        customer = Customer.objects.get(id=id)
        customer.delete()
        context = {"message": "success"}

        return Response(context, status=status.HTTP_200_OK)







############################################ invoice ###########################################################
@api_view(["GET"])
@authentication_classes((MyAuthentication, ))
@permission_classes((IsAuthenticated, ))
def all_invoice(request):
    my_invoice = Invoice.objects.filter(vendor=request.user.id).all()
    context = {}

    if len(my_invoice) > 0:
        invoices = InvoiceSerializer(my_invoice, many=True)
        # context["message"] = invoices.data
        total_invoices = []
        for invoice in invoices.data:
            invoice['item_list'] = custom_item_serializer(invoice['item_list'], invoice['quantity_list'])
            invoice.pop("quantity_list")
            total_invoices.append(invoice)

        context = {"message": total_invoices}
        return Response(context, status=status.HTTP_200_OK)

    else:
        context['message'] = "You don't have any Invoice"
        return Response(context, status=status.HTTP_404_NOT_FOUND)



@api_view(["GET", "POST"])
@authentication_classes((MyAuthentication, ))
@permission_classes((IsAuthenticated, ))
def create_invoice(request):

    if request.method == "POST":


        form = InvoiceCreate(data=request.data)
        context = {}

        if form.is_valid():
            new_invoice = form.save(request)
            context['message'] = "success"
            context['invoice'] = {"id": new_invoice.id, **form.data}
            # context['invoice']['item_list'] = [{"id": a, "quantity": b} for a,b in zip(new_invoice.iten_list, new_invoice.quantity_list)]
            # context['invoice']['item_list'] = custom_item_serializer(new_invoice.item_list, new_invoice.quantity_list)


            
            if form.validated_data['download']:
                buffer = io.BytesIO()
                invoice_ser = InvoiceSerializer(new_invoice).data
                invoice_ser['item_list'] = pdf_item_serializer(new_invoice.item_list, new_invoice.quantity_list)
                file_name = get_report(buffer, invoice_ser, CURRENCY_MAPPING[request.user.currency], "invoice", request, form.validated_data['terms'])

                buffer.seek(0)
                return FileResponse(buffer, as_attachment=True, filename=file_name)
            
            elif form.validated_data['send_email']:
                # for sending email when creating a new document
                now = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
                file_name = f"{'invoice'.title()} for {request.user.email} - {now}.pdf"
                invoice_ser = InvoiceSerializer(new_invoice).data
                invoice_ser['item_list'] = pdf_item_serializer(new_invoice.item_list, new_invoice.quantity_list)
                file_name = get_report(file_name, invoice_ser, CURRENCY_MAPPING[request.user.currency], "invoice", request, form.validated_data['terms'])
                body = "Attached to the email is the receipt of your transaction on https://www.clappe.com"
                subject = "Transaction Receipt"
                send_my_email(new_invoice.customer.email, body, subject, file_name)
                os.remove(file_name)
                new_invoice.emailed = True
                new_invoice.save()


            # if pdf_file:
            #     return FileResponse()

            return Response(context, status=status.HTTP_200_OK)

        else:
            errors = {**form.errors}
            new_errors = {key: value[0] for key,value in errors.items()}
            errors_list = [k for k in new_errors.values()]
            context = {'message': errors_list[0], 'errors': new_errors}

            return Response(context, status=status.HTTP_400_BAD_REQUEST)
    else:
        context = {"message": "create invoice page", "required fields": [
            "first_name","last_name","address","email","phone_number","taxable","invoice_pref","logo_path","invoice_number",
            "invoice_date","po_number","due_date","ship_to","shipping_address","bill_to","billing_address","notes","item_list",
            "item_total","tax","add_charges","sub_total","discount_type","discount_amount","grand_total"]}
        return Response(context, status=status.HTTP_200_OK)





@api_view(["GET", "PUT", "DELETE"])
@authentication_classes((MyAuthentication, ))
@permission_classes((IsAuthenticated, ))
def edit_invoice(request, id):

    context = {}

    if request.method == "GET":
        try:
            invoice = Invoice.objects.get(id=id)
            if invoice.vendor == request.user:
                serialized_invoice = InvoiceSerializer(invoice)
                context['message'] = serialized_invoice.data
                context["message"].pop("quantity_list")
                context['message']['item_list'] = custom_item_serializer(invoice.item_list, invoice.quantity_list)

                return Response(context, status=status.HTTP_200_OK)

            else:
                context['message'] = "You don't have access."
                return Response(context, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            print(e)
            context['message'] = "Invoice not found"
            return Response(context, status=status.HTTP_404_NOT_FOUND)
    
    elif request.method == 'PUT':
        # try:
            invoice = Invoice.objects.get(id=id)
            form = InvoiceEditSerializer(instance=invoice, data=request.data)
            context = {}

            if form.is_valid():
                updated_invoice = form.update(invoice, form.validated_data, request)
                context['message'] = "success"
                context['invoice'] = {"id": updated_invoice.id, **form.validated_data}


                if form.validated_data['download']:
                    buffer = io.BytesIO()
                    invoice_ser = InvoiceSerializer(updated_invoice).data
                    invoice_ser['item_list'] = pdf_item_serializer(updated_invoice.item_list, updated_invoice.quantity_list)
                    file_name = get_report(buffer, invoice_ser, CURRENCY_MAPPING[request.user.currency], "invoice", request, form.validated_data['terms'])

                    buffer.seek(0)
                    return FileResponse(buffer, as_attachment=True, filename=file_name)

                if form.validated_data['send_email']:
                    # for sending email when creating a new document
                    now = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
                    file_name = f"{'invoice'.title()} for {request.user.email} - {now}.pdf"
                    invoice_ser = InvoiceSerializer(updated_invoice).data
                    invoice_ser['item_list'] = pdf_item_serializer(updated_invoice.item_list, updated_invoice.quantity_list)
                    file_name = get_report(file_name, invoice_ser, CURRENCY_MAPPING[request.user.currency], "invoice", request, form.validated_data['terms'])
                    body = "Attached to the email is the receipt of your transaction on https://www.clappe.com"
                    subject = "Transaction Receipt"
                    send_my_email(updated_invoice.customer.email, body, subject, file_name)
                    os.remove(file_name)
                    updated_invoice.emailed = True
                    updated_invoice.save()



                return Response(context, status=status.HTTP_200_OK)

            else:
                errors = {**form.errors}
                new_errors = {key: value[0] for key,value in errors.items()}
                errors_list = [k for k in new_errors.values()]
                context = {'message': errors_list[0], 'errors': new_errors}

                return Response(context, status=status.HTTP_400_BAD_REQUEST)
        
        # except Exception as e:
        #     print(e)
        #     context = {'message' :"Invoice not found"}
        #     return Response(context, status=status.HTTP_404_NOT_FOUND)

    
    elif request.method == "DELETE":
        try:
            invoice = Invoice.objects.get(id=id)
            invoice.delete()
            context = {"message": "Success"}

            return Response(context, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            context = {"message": "Invoice not found"}
            
            return Response(context, status=status.HTTP_404_NOT_FOUND)






@api_view(["GET", "POST"])
@authentication_classes((MyAuthentication, ))
@permission_classes((IsAuthenticated, ))
def pay_invoice(request):
    
    if request.method == "POST":
        form = PayInvoiceSerializer(data=request.data)
        context = {}

        if form.is_valid():
            try:
                invoice = Invoice.objects.get(id=form.validated_data['invoice_id'])
                if invoice.status == "Paid":
                    context['message'] = "Invoice have been paid for already"
                    return Response(context, status=status.HTTP_400_BAD_REQUEST)

                else:
                    pay_invoice = form.save(invoice)
                    # if pay_invoice:
                    context['message'] = "success"
                    context['pay_invoice'] = {"id": pay_invoice.id, **form.data}

                    return Response(context, status=status.HTTP_200_OK)
                    # else:
                    #     context['message'] = "Invalid Invoice ID"
                    #     return Response(context, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                print(e)

        else:
            errors = {**form.errors}
            new_errors = {key: value[0] for key,value in errors.items()}
            errors_list = [k for k in new_errors.values()]
            context = {'message': errors_list[0], 'errors': new_errors}

            return Response(context, status=status.HTTP_400_BAD_REQUEST)

    else:
        context = {}
        context['message'] = "New invoice payment"
        context['required_fields'] = ["payment_type", "paid_date", "paid_amount", "payment_method", "reference", "invoice_id"]

        return Response(context, status.HTTP_200_OK)











############################ proforma invoice #######################################################################################
@api_view(["GET"])
@authentication_classes((MyAuthentication, ))
@permission_classes((IsAuthenticated, ))
def all_proforma(request):
    my_invoice = ProformaInvoice.objects.filter(vendor=request.user.id).all()
    context = {}

    if len(my_invoice) > 0:
        invoices = ProformerInvoiceSerailizer(my_invoice, many=True)
        total_invoices = []
        for invoice in invoices.data:
            invoice['item_list'] = custom_item_serializer(invoice['item_list'], invoice['quantity_list'])
            invoice.pop("quantity_list")
            total_invoices.append(invoice)

        context = {"message": total_invoices}
        return Response(context, status=status.HTTP_200_OK)

    else:
        context['message'] = "You don't have any Proforma Invoice"
        return Response(context, status=status.HTTP_404_NOT_FOUND)



@api_view(["GET", "POST"])
@authentication_classes((MyAuthentication, ))
@permission_classes((IsAuthenticated, ))
def create_proforma(request):

    if request.method == "POST":
        form = ProformaCreateSerializer(data=request.data)
        context = {}

        if form.is_valid():
            new_invoice = form.save(request)
            context['message'] = "success"
            context['invoice'] = {"id": new_invoice.id, **form.data}
            # context['invoice']['item_list'] = custom_item_serializer(new_invoice.item_list, new_invoice.quantity_list)

            if form.validated_data['download']:
                buffer = io.BytesIO()
                invoice_ser = ProformerInvoiceSerailizer(new_invoice).data
                invoice_ser['item_list'] = pdf_item_serializer(new_invoice.item_list, new_invoice.quantity_list)
                file_name = get_report(buffer, invoice_ser, CURRENCY_MAPPING[request.user.currency], "proforma invoice", request, form.validated_data['terms'])

                buffer.seek(0)
                return FileResponse(buffer, as_attachment=True, filename=file_name)


            elif form.validated_data['send_email']:
                # for sending email when creating a new document
                now = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
                file_name = f"{'proforma invoice'.title()} for {request.user.email} - {now}.pdf"
                invoice_ser = ProformerInvoiceSerailizer(new_invoice).data
                invoice_ser['item_list'] = pdf_item_serializer(new_invoice.item_list, new_invoice.quantity_list)
                file_name = get_report(file_name, invoice_ser, CURRENCY_MAPPING[request.user.currency], "proforma invoice", request, form.validated_data['terms'])
                body = "Attached to the email is the receipt of your transaction on https://www.clappe.com"
                subject = "Transaction Receipt"
                send_my_email(new_invoice.customer.email, body, subject, file_name)
                os.remove(file_name)
                new_invoice.emailed = True
                new_invoice.save()


            return Response(context, status=status.HTTP_200_OK)

        else:
            errors = {**form.errors}
            new_errors = {key: value[0] for key,value in errors.items()}
            errors_list = [k for k in new_errors.values()]
            context = {'message': errors_list[0], 'errors': new_errors}

            return Response(context, status=status.HTTP_400_BAD_REQUEST)
    else:
        context = {"message": "create preforma invoice page", "required fields": [
                "first_name", "last_name", "address", "email", "phone_number", "taxable", "invoice_pref", "logo_path", 
                    "invoice_number", "invoice_date", "po_number", "due_date", "notes", "item_list", 
                    "item_total", "tax", "add_charges", "grand_total"]}
        return Response(context, status=status.HTTP_200_OK)





@api_view(["GET", "PUT", "DELETE"])
@authentication_classes((MyAuthentication, ))
@permission_classes((IsAuthenticated, ))
def edit_proforma(request, id):

    context = {}

    if request.method == "GET":
        try:
            proforma = ProformaInvoice.objects.get(id=id)
            if proforma.vendor == request.user:
                serialized_proforma = ProformerInvoiceSerailizer(proforma)
                context['message'] = serialized_proforma.data
                context["message"].pop("quantity_list")
                context['message']['item_list'] = custom_item_serializer(proforma.item_list, proforma.quantity_list)
                return Response(context, status=status.HTTP_200_OK)

            else:
                context['message'] = "You don't have access."
                return Response(context, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            print(e)
            context['message'] = "Proforma not found"
            return Response(context, status=status.HTTP_404_NOT_FOUND)
    
    elif request.method == 'PUT':
        try:
            proforma = ProformaInvoice.objects.get(id=id)
            form = ProformaEditSerializer(instance=proforma, data=request.data)
            context = {}

            if form.is_valid():
                updated_proforma = form.update(proforma, form.validated_data)
                context['message'] = "success"
                context['proforma'] = {"id": updated_proforma.id, **form.validated_data}
                # context['proforma']['item_list'] = custom_item_serializer(updated_proforma.item_list, updated_proforma.quantity_list)

                if form.validated_data['download']:
                    buffer = io.BytesIO()
                    invoice_ser = ProformerInvoiceSerailizer(updated_proforma).data
                    invoice_ser['item_list'] = pdf_item_serializer(updated_proforma.item_list, updated_proforma.quantity_list)
                    file_name = get_report(buffer, invoice_ser, CURRENCY_MAPPING[request.user.currency], "proforma invoice", request, form.validated_data['terms'])

                    buffer.seek(0)
                    return FileResponse(buffer, as_attachment=True, filename=file_name)


                elif form.validated_data['send_email']:
                    # for sending email when creating a new document
                    now = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
                    file_name = f"{'proforma invoice'.title()} for {request.user.email} - {now}.pdf"
                    invoice_ser = ProformerInvoiceSerailizer(updated_proforma).data
                    invoice_ser['item_list'] = pdf_item_serializer(updated_proforma.item_list, updated_proforma.quantity_list)
                    file_name = get_report(file_name, invoice_ser, CURRENCY_MAPPING[request.user.currency], "proforma invoice", request, form.validated_data['terms'])
                    body = "Attached to the email is the receipt of your transaction on https://www.clappe.com"
                    subject = "Transaction Receipt"
                    send_my_email(updated_proforma.customer.email, body, subject, file_name)
                    os.remove(file_name)
                    updated_proforma.emailed = True
                    updated_proforma.save()

                
                return Response(context, status=status.HTTP_200_OK)

            else:
                errors = {**form.errors}
                new_errors = {key: value[0] for key,value in errors.items()}
                errors_list = [k for k in new_errors.values()]
                context = {'message': errors_list[0], 'errors': new_errors}

                return Response(context, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            print(e)
            context = {'message' :"Proforma not found"}
            return Response(context, status=status.HTTP_404_NOT_FOUND)

    
    elif request.method == "DELETE":
        try:
            proforma = ProformaInvoice.objects.get(id=id)
            proforma.delete()
            context = {"message": "Success"}

            return Response(context, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            context = {"message": "Proforma not found"}
            
            return Response(context, status=status.HTTP_404_NOT_FOUND)






@api_view(["GET", "POST"])
@authentication_classes((MyAuthentication, ))
@permission_classes((IsAuthenticated, ))
def pay_proforma(request):
    
    if request.method == "POST":
        form = PayProformaSerializer(data=request.data)
        context = {}

        if form.is_valid():
            try:
                proforma = ProformaInvoice.objects.get(id=form.validated_data['proforma_id'])
                if proforma.status == "Paid":
                    context['message'] = "Proforma Invoice have been paid for already"
                    return Response(context, status=status.HTTP_400_BAD_REQUEST)

                else:
                    pay_proforma = form.save(proforma)
                    context['message'] = "success"
                    context['pay_proforma'] = {"id": pay_proforma.id, **form.data}

                    return Response(context, status=status.HTTP_200_OK)

            except Exception as e:
                print(e)

        else:
            errors = {**form.errors}
            new_errors = {key: value[0] for key,value in errors.items()}
            errors_list = [k for k in new_errors.values()]
            context = {'message': errors_list[0], 'errors': new_errors}

            return Response(context, status=status.HTTP_400_BAD_REQUEST)

    else:
        context = {}
        context['message'] = "New Proforma payment"
        context['required_fields'] = ["payment_type", "paid_date", "paid_amount", "payment_method", "reference", "proforma_id"]

        return Response(context, status.HTTP_200_OK)





###################################################### purchase order ##############################################################
@api_view(["GET"])
@authentication_classes((MyAuthentication, ))
@permission_classes((IsAuthenticated, ))
def all_purchaseorder(request):
    my_po = PurchaseOrder.objects.filter(vendor=request.user.id).all()
    context = {}

    if len(my_po) > 0:
        pos = PurchaseOrderSerailizer(my_po, many=True)
        total_invoices = []
        for invoice in pos.data:
            invoice['item_list'] = custom_item_serializer(invoice['item_list'], invoice['quantity_list'])
            invoice.pop("quantity_list")
            total_invoices.append(invoice)

        context = {"message": total_invoices}
        return Response(context, status=status.HTTP_200_OK)

    else:
        context['message'] = "You don't have any Purchase Order"
        return Response(context, status=status.HTTP_404_NOT_FOUND)




@api_view(["GET", "POST"])
@authentication_classes((MyAuthentication, ))
@permission_classes((IsAuthenticated, ))
def create_purchaseorder(request):

    if request.method == "POST":
        form = PurchaseCreateSerializer(data=request.data)
        context = {}

        if form.is_valid():
            new_po = form.save(request)
            context['message'] = "success"
            context['invoice'] = {"id": new_po.id, **form.data}
            # context['invoice']['item_list'] = custom_item_serializer(new_po.item_list, new_po.quantity_list)

            if form.validated_data['download']:
                buffer = io.BytesIO()
                invoice_ser = PurchaseOrderSerailizer(new_po).data
                invoice_ser['item_list'] = pdf_item_serializer(new_po.item_list, new_po.quantity_list)
                file_name = get_report(buffer, invoice_ser, CURRENCY_MAPPING[request.user.currency], "purchase order", request, form.validated_data['terms'])

                buffer.seek(0)
                return FileResponse(buffer, as_attachment=True, filename=file_name)


            elif form.validated_data['send_email']:
                # for sending email when creating a new document
                now = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
                file_name = f"{'purchase order'.title()} for {request.user.email} - {now}.pdf"
                invoice_ser = PurchaseOrderSerailizer(new_po).data
                invoice_ser['item_list'] = pdf_item_serializer(new_po.item_list, new_po.quantity_list)
                file_name = get_report(file_name, invoice_ser, CURRENCY_MAPPING[request.user.currency], "purchase order", request, form.validated_data['terms'])
                body = "Attached to the email is the receipt of your transaction on https://www.clappe.com"
                subject = "Transaction Receipt"
                send_my_email(new_po.customer.email, body, subject, file_name)
                os.remove(file_name)
                new_po.emailed = True
                new_po.save()

            return Response(context, status=status.HTTP_200_OK)

        else:
            errors = {**form.errors}
            new_errors = {key: value[0] for key,value in errors.items()}
            errors_list = [k for k in new_errors.values()]
            context = {'message': errors_list[0], 'errors': new_errors}

            return Response(context, status=status.HTTP_400_BAD_REQUEST)
    else:
        context = {"message": "create purchase order page", "required fields": [
                "first_name", "last_name", "address", "email", "phone_number", "taxable", "po_pref", "logo_path", 
                    "po_number", "po_date", "ship_to", "notes", "shipping_address", "item_list", 
                    "item_total", "tax", "add_charges", "grand_total"]}
        return Response(context, status=status.HTTP_200_OK)





@api_view(["GET", "PUT", "DELETE"])
@authentication_classes((MyAuthentication, ))
@permission_classes((IsAuthenticated, ))
def edit_purchaseorder(request, id):

    context = {}

    if request.method == "GET":
        try:
            purchase = PurchaseOrder.objects.get(id=id)
            if purchase.vendor == request.user:
                serialized_purchase = PurchaseOrderSerailizer(purchase)
                context['message'] = serialized_purchase.data
                context["message"].pop("quantity_list")
                context['message']['item_list'] = custom_item_serializer(purchase.item_list, purchase.quantity_list)
                return Response(context, status=status.HTTP_200_OK)

            else:
                context['message'] = "You don't have access."
                return Response(context, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            print(e)
            context['message'] = "Purchase order not found"
            return Response(context, status=status.HTTP_404_NOT_FOUND)
    
    elif request.method == 'PUT':
        try:
            purchase = PurchaseOrder.objects.get(id=id)
            form = PurchaseEditSerializer(instance=purchase, data=request.data)
            context = {}

            if form.is_valid():
                updated_purchase = form.update(purchase, form.validated_data)
                context['message'] = "success"
                context['purchase'] = {"id": updated_purchase.id, **form.validated_data}
                # context['purchase']['item_list'] = custom_item_serializer(updated_purchase.item_list, updated_purchase.quantity_list)

                if form.validated_data['download']:
                    buffer = io.BytesIO()
                    invoice_ser = PurchaseOrderSerailizer(updated_purchase).data
                    invoice_ser['item_list'] = pdf_item_serializer(updated_purchase.item_list, updated_purchase.quantity_list)
                    file_name = get_report(buffer, invoice_ser, CURRENCY_MAPPING[request.user.currency], "purchase order", request, form.validated_data['terms'])

                    buffer.seek(0)
                    return FileResponse(buffer, as_attachment=True, filename=file_name)


                elif form.validated_data['send_email']:
                    # for sending email when creating a new document
                    now = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
                    file_name = f"{'purchase order'.title()} for {request.user.email} - {now}.pdf"
                    invoice_ser = PurchaseOrderSerailizer(updated_purchase).data
                    invoice_ser['item_list'] = pdf_item_serializer(updated_purchase.item_list, updated_purchase.quantity_list)
                    file_name = get_report(file_name, invoice_ser, CURRENCY_MAPPING[request.user.currency], "purchase order", request, form.validated_data['terms'])
                    body = "Attached to the email is the receipt of your transaction on https://www.clappe.com"
                    subject = "Transaction Receipt"
                    send_my_email(updated_purchase.customer.email, body, subject, file_name)
                    os.remove(file_name)
                    updated_purchase.emailed = True
                    updated_purchase.save()

                return Response(context, status=status.HTTP_200_OK)

            else:
                errors = {**form.errors}
                new_errors = {key: value[0] for key,value in errors.items()}
                errors_list = [k for k in new_errors.values()]
                context = {'message': errors_list[0], 'errors': new_errors}

                return Response(context, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            print(e)
            context = {'message' :"Purchase order not found"}
            return Response(context, status=status.HTTP_404_NOT_FOUND)

    
    elif request.method == "DELETE":
        try:
            purchase = PurchaseOrder.objects.get(id=id)
            purchase.delete()
            context = {"message": "Success"}

            return Response(context, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            context = {"message": "Purchase Order not found"}
            
            return Response(context, status=status.HTTP_404_NOT_FOUND)






@api_view(["GET", "POST"])
@authentication_classes((MyAuthentication, ))
@permission_classes((IsAuthenticated, ))
def pay_purchaseorder(request):
    
    if request.method == "POST":
        form = PayPurchaseSerializer(data=request.data)
        context = {}

        if form.is_valid():
            try:
                purchase = PurchaseOrder.objects.get(id=form.validated_data['purchase_id'])
                if purchase.status == "Paid":
                    context['message'] = "Purchase order have been paid for already"
                    return Response(context, status=status.HTTP_400_BAD_REQUEST)

                else:
                    Pay_purchase = form.save(purchase)
                    context['message'] = "success"
                    context['Pay_purchase'] = {"id": Pay_purchase.id, **form.data}

                    return Response(context, status=status.HTTP_200_OK)

            except Exception as e:
                print(e)

        else:
            errors = {**form.errors}
            new_errors = {key: value[0] for key,value in errors.items()}
            errors_list = [k for k in new_errors.values()]
            context = {'message': errors_list[0], 'errors': new_errors}

            return Response(context, status=status.HTTP_400_BAD_REQUEST)


    else:
        context = {}
        context['message'] = "New Purchase order payment"
        context['required_fields'] = ["payment_type", "paid_date", "paid_amount", "payment_method", "reference", "purchase_id"]

        return Response(context, status.HTTP_200_OK)














###################################################### estimate ##############################################################
@api_view(["GET"])
@authentication_classes((MyAuthentication, ))
@permission_classes((IsAuthenticated, ))
def all_estimate(request):

    my_estimate = Estimate.objects.filter(vendor=request.user.id).all()
    context = {}

    if len(my_estimate) > 0:
        estimates = EstimateSerailizer(my_estimate, many=True)
        total_invoices = []
        for invoice in estimates.data:
            invoice['item_list'] = custom_item_serializer(invoice['item_list'], invoice['quantity_list'])
            invoice.pop("quantity_list")
            total_invoices.append(invoice)

        context = {"message": total_invoices}
        return Response(context, status=status.HTTP_200_OK)

    else:
        context['message'] = "You don't have any Estimate"
        return Response(context, status=status.HTTP_404_NOT_FOUND)




@api_view(["GET", "POST"])
@authentication_classes((MyAuthentication, ))
@permission_classes((IsAuthenticated, ))
def create_estimate(request):

    if request.method == "POST":
        form = EstimateCreateSerializer(data=request.data)
        context = {}

        if form.is_valid():
            new_estimate = form.save(request)
            context['message'] = "success"
            context['estimate'] = {"id": new_estimate.id, **form.data}
            # context['estimate']['item_list'] = custom_item_serializer(new_estimate.item_list, new_estimate.quantity_list)

            if form.validated_data['download']:
                buffer = io.BytesIO()
                invoice_ser = EstimateSerailizer(new_estimate).data
                invoice_ser['item_list'] = pdf_item_serializer(new_estimate.item_list, new_estimate.quantity_list)
                file_name = get_report(buffer, invoice_ser, CURRENCY_MAPPING[request.user.currency], "estimate", request, form.validated_data['terms'])

                buffer.seek(0)
                return FileResponse(buffer, as_attachment=True, filename=file_name)


            elif form.validated_data['send_email']:
                # for sending email when creating a new document
                now = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
                file_name = f"{'estimate'.title()} for {request.user.email} - {now}.pdf"
                invoice_ser = EstimateSerailizer(new_estimate).data
                invoice_ser['item_list'] = pdf_item_serializer(new_estimate.item_list, new_estimate.quantity_list)
                file_name = get_report(file_name, invoice_ser, CURRENCY_MAPPING[request.user.currency], "estimate", request, form.validated_data['terms'])
                body = "Attached to the email is the receipt of your transaction on https://www.clappe.com"
                subject = "Transaction Receipt"
                send_my_email(new_estimate.customer.email, body, subject, file_name)
                os.remove(file_name)
                new_estimate.emailed = True
                new_estimate.save()

            return Response(context, status=status.HTTP_200_OK)

        else:
            errors = {**form.errors}
            new_errors = {key: value[0] for key,value in errors.items()}
            errors_list = [k for k in new_errors.values()]
            context = {'message': errors_list[0], 'errors': new_errors}

            return Response(context, status=status.HTTP_400_BAD_REQUEST)
    else:
        context = {"message": "create estimate page", "required fields": [
                "customer_id", "taxable", "estimate_pref", "logo_path", 
                    "estimate_number", "estimate_date", "ship_to", "shipping_address", "bill_to", "billing_address",
                    "notes", "item_list", "item_total", "tax", "add_charges", "grand_total"]}
        return Response(context, status=status.HTTP_200_OK)





@api_view(["GET", "PUT", "DELETE"])
@authentication_classes((MyAuthentication, ))
@permission_classes((IsAuthenticated, ))
def edit_estimate(request, id):

    context = {}

    if request.method == "GET":
        try:
            estimate = Estimate.objects.get(id=id)
            if estimate.vendor == request.user:
                serialized_estimate = EstimateSerailizer(estimate)
                context['message'] = serialized_estimate.data
                context["message"].pop("quantity_list")
                context['message']['item_list'] = custom_item_serializer(estimate.item_list, estimate.quantity_list)
                return Response(context, status=status.HTTP_200_OK)

            else:
                context['message'] = "You don't have access."
                return Response(context, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            print(e)
            context['message'] = "Estimate not found"
            return Response(context, status=status.HTTP_404_NOT_FOUND)
    
    elif request.method == 'PUT':
        try:
            estimate = Estimate.objects.get(id=id)
            form = EstimateEditSerializer(instance=estimate, data=request.data)
            context = {}

            if form.is_valid():
                updated_estimate = form.update(estimate, form.validated_data)
                context['message'] = "success"
                context['estimate'] = {"id": updated_estimate.id, **form.validated_data}
                # context['estimate']['item_list'] = custom_item_serializer(updated_estimate.item_list, updated_estimate.quantity_list)

                if form.validated_data['download']:
                    buffer = io.BytesIO()
                    invoice_ser = EstimateSerailizer(updated_estimate).data
                    invoice_ser['item_list'] = pdf_item_serializer(updated_estimate.item_list, updated_estimate.quantity_list)
                    file_name = get_report(buffer, invoice_ser, CURRENCY_MAPPING[request.user.currency], "estimate", request, form.validated_data['terms'])

                    buffer.seek(0)
                    return FileResponse(buffer, as_attachment=True, filename=file_name)

                elif form.validated_data['send_email']:
                    # for sending email when creating a new document
                    now = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
                    file_name = f"{'estimate'.title()} for {request.user.email} - {now}.pdf"
                    invoice_ser = EstimateSerailizer(updated_estimate).data
                    invoice_ser['item_list'] = pdf_item_serializer(updated_estimate.item_list, updated_estimate.quantity_list)
                    file_name = get_report(file_name, invoice_ser, CURRENCY_MAPPING[request.user.currency], "estimate", request, form.validated_data['terms'])
                    body = "Attached to the email is the receipt of your transaction on https://www.clappe.com"
                    subject = "Transaction Receipt"
                    send_my_email(updated_estimate.customer.email, body, subject, file_name)
                    os.remove(file_name)
                    updated_estimate.emailed = True
                    updated_estimate.save()

                return Response(context, status=status.HTTP_200_OK)

            else:
                errors = {**form.errors}
                new_errors = {key: value[0] for key,value in errors.items()}
                errors_list = [k for k in new_errors.values()]
                context = {'message': errors_list[0], 'errors': new_errors}

                return Response(context, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            print(e)
            context = {'message' :"Estimate not found"}
            return Response(context, status=status.HTTP_404_NOT_FOUND)

    
    elif request.method == "DELETE":
        try:
            estimate = Estimate.objects.get(id=id)
            estimate.delete()
            context = {"message": "Success"}

            return Response(context, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            context = {"message": "Estimate not found"}
            
            return Response(context, status=status.HTTP_404_NOT_FOUND)






@api_view(["GET", "POST"])
@authentication_classes((MyAuthentication, ))
@permission_classes((IsAuthenticated, ))
def pay_estimate(request):
    
    if request.method == "POST":
        form = PayEstimateSerializer(data=request.data)
        context = {}

        if form.is_valid():
            try:
                estimate = Estimate.objects.get(id=form.validated_data['estimate_id'])
                if estimate.status == "Paid":
                    context['message'] = "Estimate have been paid for already"
                    return Response(context, status=status.HTTP_400_BAD_REQUEST)

                else:
                    pay_estimate = form.save(estimate)
                    context['message'] = "success"
                    context['pay_estimate'] = {"id": pay_estimate.id, **form.data}

                    return Response(context, status=status.HTTP_200_OK)

            except Exception as e:
                print(e)

        else:
            errors = {**form.errors}
            new_errors = {key: value[0] for key,value in errors.items()}
            errors_list = [k for k in new_errors.values()]
            context = {'message': errors_list[0], 'errors': new_errors}

            return Response(context, status=status.HTTP_400_BAD_REQUEST)


    else:
        context = {}
        context['message'] = "New Estimate payment"
        context['required_fields'] = ["payment_type", "paid_date", "paid_amount", "payment_method", "reference", "estimate_id"]

        return Response(context, status.HTTP_200_OK)












################################################ items ##########################################################

@api_view(["GET", "POST"])
@authentication_classes((MyAuthentication, ))
@permission_classes((IsAuthenticated, ))
def all_items(request):
    my_items = Item.objects.filter(vendor=request.user.id).all()
    context = {}

    if len(my_items) > 0:
        items = ItemSerializer(my_items, many=True)
        context = {"message": items.data}
        return Response(context, status=status.HTTP_200_OK)

    else:
        context['message'] = "You don't have any items"
        return Response(context, status=status.HTTP_404_NOT_FOUND)





@api_view(["GET", "POST"])
@authentication_classes((MyAuthentication, ))
@permission_classes((IsAuthenticated, ))
def create_item(request):

    if request.method == "POST":
        form = CreateItemSerializer(data=request.data)
        context = {}

        if form.is_valid():
            new_item = form.save(request)
            context['message'] = "success"
            context['estimate'] = {"id": new_item.id, **form.data}

            return Response(context, status=status.HTTP_200_OK)

        else:
            errors = {**form.errors}
            new_errors = {key: value[0] for key,value in errors.items()}
            errors_list = [k for k in new_errors.values()]
            context = {'message': errors_list[0], 'errors': new_errors}

            return Response(context, status=status.HTTP_400_BAD_REQUEST)
    else:
        context = {"message": "create item page", "required fields": ["name", "description", "cost_price", "sales_price", "sales_tax"]}
        return Response(context, status=status.HTTP_200_OK)





@api_view(["GET", "PUT", "DELETE"])
@authentication_classes((MyAuthentication, ))
@permission_classes((IsAuthenticated, ))
def edit_item(request, id):

    context = {}

    if request.method == "GET":
        try:
            item = Item.objects.get(id=id)
            if item.vendor == request.user:
                serialized_item = CreateItemSerializer(item)
                context['message'] = serialized_item.data
                return Response(context, status=status.HTTP_200_OK)

            else:
                context['message'] = "You don't have access."
                return Response(context, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            print(e)
            context['message'] = "Item not found"
            return Response(context, status=status.HTTP_404_NOT_FOUND)
    
    elif request.method == 'PUT':
        try:
            item = Item.objects.get(id=id)
            form = CreateItemSerializer(instance=item, data=request.data)
            context = {}

            if form.is_valid():
                updated_item = form.update(item)
                context['message'] = "success"
                context['item'] = {"id": updated_item.id, **form.data}

                return Response(context, status=status.HTTP_200_OK)

            else:
                errors = {**form.errors}
                new_errors = {key: value[0] for key,value in errors.items()}
                errors_list = [k for k in new_errors.values()]
                context = {'message': errors_list[0], 'errors': new_errors}

                return Response(context, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            print(e)
            context = {'message' :"Item not found"}
            return Response(context, status=status.HTTP_404_NOT_FOUND)

    
    elif request.method == "DELETE":
        try:
            item = Item.objects.get(id=id)
            item.delete()
            context = {"message": "Success"}

            return Response(context, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            context = {"message": "Item not found"}
            
            return Response(context, status=status.HTTP_404_NOT_FOUND)














###################################################### quote ##############################################################
@api_view(["GET"])
@authentication_classes((MyAuthentication, ))
@permission_classes((IsAuthenticated, ))
def all_quote(request):

    my_quote = Quote.objects.filter(vendor=request.user.id).all()
    context = {}

    if len(my_quote) > 0:
        quotes = QuoteSerailizer(my_quote, many=True)
        total_invoices = []
        for invoice in quotes.data:
            invoice['item_list'] = custom_item_serializer(invoice['item_list'], invoice['quantity_list'])
            invoice.pop("quantity_list")
            total_invoices.append(invoice)

        context = {"message": total_invoices}
        return Response(context, status=status.HTTP_200_OK)

    else:
        context['message'] = "You don't have any Quote"
        return Response(context, status=status.HTTP_404_NOT_FOUND)




@api_view(["GET", "POST"])
@authentication_classes((MyAuthentication, ))
@permission_classes((IsAuthenticated, ))
def create_quote(request):

    if request.method == "POST":
        form = QuoteCreateSerializer(data=request.data)
        context = {}

        if form.is_valid():
            new_quote = form.save(request)
            context['message'] = "success"
            context['quote'] = {"id": new_quote.id, **form.data}
            # context['quote']['item_list'] = custom_item_serializer(new_quote.item_list, new_quote.quantity_list)

            if form.validated_data['download']:
                buffer = io.BytesIO()
                invoice_ser = QuoteSerailizer(new_quote).data
                invoice_ser['item_list'] = pdf_item_serializer(new_quote.item_list, new_quote.quantity_list)
                file_name = get_report(buffer, invoice_ser, CURRENCY_MAPPING[request.user.currency], "quote", request, form.validated_data['terms'])

                buffer.seek(0)
                return FileResponse(buffer, as_attachment=True, filename=file_name)

            elif form.validated_data['send_email']:
                # for sending email when creating a new document
                now = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
                file_name = f"{'quote'.title()} for {request.user.email} - {now}.pdf"
                invoice_ser = QuoteSerailizer(new_quote).data
                invoice_ser['item_list'] = pdf_item_serializer(new_quote.item_list, new_quote.quantity_list)
                file_name = get_report(file_name, invoice_ser, CURRENCY_MAPPING[request.user.currency], "quote", request, form.validated_data['terms'])
                body = "Attached to the email is the receipt of your transaction on https://www.clappe.com"
                subject = "Transaction Receipt"
                send_my_email(new_quote.customer.email, body, subject, file_name)
                os.remove(file_name)
                new_quote.emailed = True
                new_quote.save()

            return Response(context, status=status.HTTP_200_OK)

        else:
            errors = {**form.errors}
            new_errors = {key: value[0] for key,value in errors.items()}
            errors_list = [k for k in new_errors.values()]
            context = {'message': errors_list[0], 'errors': new_errors}

            return Response(context, status=status.HTTP_400_BAD_REQUEST)
    else:
        context = {"message": "create quote page", "required fields": [
                "customer_id", "taxable", "quote_pref", "logo_path", "due_date",
                    "quote_number", "quote_date", "po_number", "ship_to", "shipping_address", "bill_to", "billing_address", 
                    "notes", "item_list", "item_total", "tax", "add_charges", "grand_total"]}

        return Response(context, status=status.HTTP_200_OK)





@api_view(["GET", "PUT", "DELETE"])
@authentication_classes((MyAuthentication, ))
@permission_classes((IsAuthenticated, ))
def edit_quote(request, id):

    context = {}

    if request.method == "GET":
        try:
            quote = Quote.objects.get(id=id)
            if quote.vendor == request.user:
                serialized_quote = QuoteSerailizer(quote)
                context['message'] = serialized_quote.data
                context["message"].pop("quantity_list")
                context['message']['item_list'] = custom_item_serializer(quote.item_list, quote.quantity_list)
                return Response(context, status=status.HTTP_200_OK)

            else:
                context['message'] = "You don't have access."
                return Response(context, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            print(e)
            context['message'] = "Quote not found"
            return Response(context, status=status.HTTP_404_NOT_FOUND)
    
    elif request.method == 'PUT':
        try:
            quote = Quote.objects.get(id=id)
            form = QuoteEditSerializer(instance=quote, data=request.data)
            context = {}

            if form.is_valid():
                updated_quote = form.update(quote, form.validated_data)
                context['message'] = "success"
                context['quote'] = {"id": updated_quote.id, **form.validated_data}
                # context['quote']['item_list'] = custom_item_serializer(updated_quote.item_list, updated_quote.quantity_list)

                if form.validated_data['download']:
                    buffer = io.BytesIO()
                    invoice_ser = QuoteSerailizer(updated_quote).data
                    invoice_ser['item_list'] = pdf_item_serializer(updated_quote.item_list, updated_quote.quantity_list)
                    file_name = get_report(buffer, invoice_ser, CURRENCY_MAPPING[request.user.currency], "quote", request, form.validated_data['terms'])

                    buffer.seek(0)
                    return FileResponse(buffer, as_attachment=True, filename=file_name)


                elif form.validated_data['send_email']:
                    # for sending email when creating a new document
                    now = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
                    file_name = f"{'quote'.title()} for {request.user.email} - {now}.pdf"
                    invoice_ser = QuoteSerailizer(updated_quote).data
                    invoice_ser['item_list'] = pdf_item_serializer(updated_quote.item_list, updated_quote.quantity_list)
                    file_name = get_report(file_name, invoice_ser, CURRENCY_MAPPING[request.user.currency], "quote", request, form.validated_data['terms'])
                    body = "Attached to the email is the receipt of your transaction on https://www.clappe.com"
                    subject = "Transaction Receipt"
                    send_my_email(updated_quote.customer.email, body, subject, file_name)
                    os.remove(file_name)
                    updated_quote.emailed = True
                    updated_quote.save()

                return Response(context, status=status.HTTP_200_OK)

            else:
                errors = {**form.errors}
                new_errors = {key: value[0] for key,value in errors.items()}
                errors_list = [k for k in new_errors.values()]
                context = {'message': errors_list[0], 'errors': new_errors}

                return Response(context, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            print(e)
            context = {'message' :"Quote not found"}
            return Response(context, status=status.HTTP_404_NOT_FOUND)

    
    elif request.method == "DELETE":
        try:
            quote = Quote.objects.get(id=id)
            quote.delete()
            context = {"message": "Success"}

            return Response(context, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            context = {"message": "Quote not found"}
            
            return Response(context, status=status.HTTP_404_NOT_FOUND)






@api_view(["GET", "POST"])
@authentication_classes((MyAuthentication, ))
@permission_classes((IsAuthenticated, ))
def pay_quote(request):
    
    if request.method == "POST":
        form = PayQuoteSerializer(data=request.data)
        context = {}

        if form.is_valid():
            try:
                quote = Quote.objects.get(id=form.validated_data['quote_id'])
                if quote.status == "Paid":
                    context['message'] = "Quote have been paid for already"
                    return Response(context, status=status.HTTP_400_BAD_REQUEST)

                else:
                    pay_quote = form.save(quote)
                    context['message'] = "success"
                    context['pay_quote'] = {"id": pay_quote.id, **form.data}

                    return Response(context, status=status.HTTP_200_OK)

            except Exception as e:
                print(e)

        else:
            errors = {**form.errors}
            new_errors = {key: value[0] for key,value in errors.items()}
            errors_list = [k for k in new_errors.values()]
            context = {'message': errors_list[0], 'errors': new_errors}

            return Response(context, status=status.HTTP_400_BAD_REQUEST)

    else:
        context = {}
        context['message'] = "New Quote payment"
        context['required_fields'] = ["payment_type", "paid_date", "paid_amount", "payment_method", "reference", "quote_id"]

        return Response(context, status.HTTP_200_OK)










###################################################### receipt ##############################################################
@api_view(["GET"])
@authentication_classes((MyAuthentication, ))
@permission_classes((IsAuthenticated, ))
def all_receipt(request):

    my_receipt = Receipt.objects.filter(vendor=request.user.id).all()
    context = {}

    if len(my_receipt) > 0:
        receipts = ReceiptSerailizer(my_receipt, many=True)
        total_invoices = []
        for invoice in receipts.data:
            invoice['item_list'] = custom_item_serializer(invoice['item_list'], invoice['quantity_list'])
            invoice.pop("quantity_list")
            total_invoices.append(invoice)

        context = {"message": total_invoices}
        return Response(context, status=status.HTTP_200_OK)

    else:
        context['message'] = "You don't have any receipt"
        return Response(context, status=status.HTTP_404_NOT_FOUND)




@api_view(["GET", "POST"])
@authentication_classes((MyAuthentication, ))
@permission_classes((IsAuthenticated, ))
def create_receipt(request):

    if request.method == "POST":
        form = REceiptCreateSerializer(data=request.data)
        context = {}

        if form.is_valid():
            new_receipt = form.save(request)
            context['message'] = "success"
            context['receipt'] = {"id": new_receipt.id, **form.data}
            # context['receipt']['item_list'] = custom_item_serializer(new_receipt.item_list, new_receipt.quantity_list)

            if form.validated_data['download']:
                buffer = io.BytesIO()
                invoice_ser = ReceiptSerailizer(new_receipt).data
                invoice_ser['item_list'] = pdf_item_serializer(new_receipt.item_list, new_receipt.quantity_list)
                file_name = get_report(buffer, invoice_ser, CURRENCY_MAPPING[request.user.currency], "receipt", request, form.validated_data['terms'])

                buffer.seek(0)
                return FileResponse(buffer, as_attachment=True, filename=file_name)


            elif form.validated_data['send_email']:
                # for sending email when creating a new document
                now = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
                file_name = f"{'receipt'.title()} for {request.user.email} - {now}.pdf"
                invoice_ser = ReceiptSerailizer(new_receipt).data
                invoice_ser['item_list'] = pdf_item_serializer(new_receipt.item_list, new_receipt.quantity_list)
                file_name = get_report(file_name, invoice_ser, CURRENCY_MAPPING[request.user.currency], "receipt", request, form.validated_data['terms'])
                body = "Attached to the email is the receipt of your transaction on https://www.clappe.com"
                subject = "Transaction Receipt"
                send_my_email(new_receipt.customer.email, body, subject, file_name)
                os.remove(file_name)
                new_receipt.emailed = True
                new_receipt.save()

            return Response(context, status=status.HTTP_200_OK)

        else:
            errors = {**form.errors}
            new_errors = {key: value[0] for key,value in errors.items()}
            errors_list = [k for k in new_errors.values()]
            context = {'message': errors_list[0], 'errors': new_errors}

            return Response(context, status=status.HTTP_400_BAD_REQUEST)
    else:
        context = {"message": "create receipt page", "required fields": [
                "customer_id", "taxable", "receipt_pref", "logo_path", 
                    "receipt_number", "receipt_date", "po_number", "due_date", "ship_to", "shipping_address", "bill_to", "billing_address", 
                    "notes", "item_list", "item_total", "tax", "add_charges", "grand_total"]}

        return Response(context, status=status.HTTP_200_OK)





@api_view(["GET", "PUT", "DELETE"])
@authentication_classes((MyAuthentication, ))
@permission_classes((IsAuthenticated, ))
def edit_receipt(request, id):

    context = {}

    if request.method == "GET":
        try:
            receipt = Receipt.objects.get(id=id)
            if receipt.vendor == request.user:
                serialized_receipt = ReceiptSerailizer(receipt)
                context['message'] = serialized_receipt.data
                context["message"].pop("quantity_list")
                context['message']['item_list'] = custom_item_serializer(receipt.item_list, receipt.quantity_list)
                return Response(context, status=status.HTTP_200_OK)

            else:
                context['message'] = "You don't have access."
                return Response(context, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            print(e)
            context['message'] = "Receipt not found"
            return Response(context, status=status.HTTP_404_NOT_FOUND)
    
    elif request.method == 'PUT':
        try:
            receipt = Receipt.objects.get(id=id)
            form = ReceiptEditSerializer(instance=receipt, data=request.data)
            context = {}

            if form.is_valid():
                updated_receipt = form.update(receipt, form.validated_data)
                context['message'] = "success"
                context['receipt'] = {"id": updated_receipt.id, **form.validated_data}
                # context['receipt']['item_list'] = custom_item_serializer(updated_receipt.item_list, updated_receipt.quantity_list)

                if form.validated_data['download']:
                    buffer = io.BytesIO()
                    invoice_ser = ReceiptSerailizer(updated_receipt).data
                    invoice_ser['item_list'] = pdf_item_serializer(updated_receipt.item_list, updated_receipt.quantity_list)
                    file_name = get_report(buffer, invoice_ser, CURRENCY_MAPPING[request.user.currency], "receipt", request, form.validated_data['terms'])

                    buffer.seek(0)
                    return FileResponse(buffer, as_attachment=True, filename=file_name)


                elif form.validated_data['send_email']:
                    # for sending email when creating a new document
                    now = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
                    file_name = f"{'receipt'.title()} for {request.user.email} - {now}.pdf"
                    invoice_ser = ReceiptSerailizer(updated_receipt).data
                    invoice_ser['item_list'] = pdf_item_serializer(updated_receipt.item_list, updated_receipt.quantity_list)
                    file_name = get_report(file_name, invoice_ser, CURRENCY_MAPPING[request.user.currency], "receipt", request, form.validated_data['terms'])
                    body = "Attached to the email is the receipt of your transaction on https://www.clappe.com"
                    subject = "Transaction Receipt"
                    send_my_email(updated_receipt.customer.email, body, subject, file_name)
                    os.remove(file_name)
                    updated_receipt.emailed = True
                    updated_receipt.save()

                return Response(context, status=status.HTTP_200_OK)

            else:
                errors = {**form.errors}
                new_errors = {key: value[0] for key,value in errors.items()}
                errors_list = [k for k in new_errors.values()]
                context = {'message': errors_list[0], 'errors': new_errors}

                return Response(context, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            print(e)
            context = {'message' :"Receipt not found"}
            return Response(context, status=status.HTTP_404_NOT_FOUND)

    
    elif request.method == "DELETE":
        try:
            receipt = Receipt.objects.get(id=id)
            receipt.delete()
            context = {"message": "Success"}

            return Response(context, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            context = {"message": "Receipt not found"}
            
            return Response(context, status=status.HTTP_404_NOT_FOUND)






@api_view(["GET", "POST"])
@authentication_classes((MyAuthentication, ))
@permission_classes((IsAuthenticated, ))
def pay_receipt(request):
    
    if request.method == "POST":
        form = PayReceiptSerializer(data=request.data)
        context = {}

        if form.is_valid():
            try:
                receipt = Receipt.objects.get(id=form.validated_data['receipt_id'])
                if receipt.status == "Paid":
                    context['message'] = "Receipt have been paid for already"
                    return Response(context, status=status.HTTP_400_BAD_REQUEST)

                else:
                    pay_receipt = form.save(receipt)
                    context['message'] = "success"
                    context['pay_receipt'] = {"id": pay_receipt.id, **form.data}

                    return Response(context, status=status.HTTP_200_OK)

            except Exception as e:
                print(e)

        else:
            errors = {**form.errors}
            new_errors = {key: value[0] for key,value in errors.items()}
            errors_list = [k for k in new_errors.values()]
            context = {'message': errors_list[0], 'errors': new_errors}

            return Response(context, status=status.HTTP_400_BAD_REQUEST)

    else:
        context = {}
        context['message'] = "New Receipt payment"
        context['required_fields'] = ["payment_type", "paid_date", "paid_amount", "payment_method", "reference", "receipt_id"]

        return Response(context, status.HTTP_200_OK)













###################################################### creditnote ##############################################################
@api_view(["GET"])
@authentication_classes((MyAuthentication, ))
@permission_classes((IsAuthenticated, ))
def all_credit(request):

    my_credit = CreditNote.objects.filter(vendor=request.user.id).all()
    context = {}

    if len(my_credit) > 0:
        credits = CreditNoteSerailizer(my_credit, many=True)
        total_invoices = []
        for invoice in credits.data:
            invoice['item_list'] = custom_item_serializer(invoice['item_list'], invoice['quantity_list'])
            invoice.pop("quantity_list")
            total_invoices.append(invoice)

        context = {"message": total_invoices}
        return Response(context, status=status.HTTP_200_OK)

    else:
        context['message'] = "You don't have any Credit Note"
        return Response(context, status=status.HTTP_404_NOT_FOUND)




@api_view(["GET", "POST"])
@authentication_classes((MyAuthentication, ))
@permission_classes((IsAuthenticated, ))
def create_credit(request):

    if request.method == "POST":
        form = CNCreateSerializer(data=request.data)
        context = {}

        if form.is_valid():
            new_credit = form.save(request)
            context['message'] = "success"
            context['credit'] = {"id": new_credit.id, **form.data}
            # context['credit']['item_list'] = custom_item_serializer(new_credit.item_list, new_credit.quantity_list)

            if form.validated_data['download']:
                buffer = io.BytesIO()
                invoice_ser = CreditNoteSerailizer(new_credit).data
                invoice_ser['item_list'] = pdf_item_serializer(new_credit.item_list, new_credit.quantity_list)
                file_name = get_report(buffer, invoice_ser, CURRENCY_MAPPING[request.user.currency], "credit note", request, form.validated_data['terms'])

                buffer.seek(0)
                return FileResponse(buffer, as_attachment=True, filename=file_name)


            elif form.validated_data['send_email']:
                # for sending email when creating a new document
                now = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
                file_name = f"{'credit note'.title()} for {request.user.email} - {now}.pdf"
                invoice_ser = CreditNoteSerailizer(new_credit).data
                invoice_ser['item_list'] = pdf_item_serializer(new_credit.item_list, new_credit.quantity_list)
                file_name = get_report(file_name, invoice_ser, CURRENCY_MAPPING[request.user.currency], "credit note", request, form.validated_data['terms'])
                body = "Attached to the email is the receipt of your transaction on https://www.clappe.com"
                subject = "Transaction Receipt"
                send_my_email(new_credit.customer.email, body, subject, file_name)
                os.remove(file_name)
                new_credit.emailed = True
                new_credit.save()

            return Response(context, status=status.HTTP_200_OK)

        else:
            errors = {**form.errors}
            new_errors = {key: value[0] for key,value in errors.items()}
            errors_list = [k for k in new_errors.values()]
            context = {'message': errors_list[0], 'errors': new_errors}

            return Response(context, status=status.HTTP_400_BAD_REQUEST)
    else:
        context = {"message": "create credit note page", "required fields": [
                 "first_name", "last_name", "address", "email", "phone_number", "taxable", "cn_pref", "logo_path", 
                    "cn_number", "cn_date", "po_number", "due_date", "ship_to", "shipping_address", "notes", "item_list", 
                    "item_total", "tax", "add_charges", "grand_total"]}

        return Response(context, status=status.HTTP_200_OK)





@api_view(["GET", "PUT", "DELETE"])
@authentication_classes((MyAuthentication, ))
@permission_classes((IsAuthenticated, ))
def edit_credit(request, id):

    context = {}

    if request.method == "GET":
        try:
            credit = CreditNote.objects.get(id=id)
            if credit.vendor == request.user:
                serialized_credit = CreditNoteSerailizer(credit)
                context['message'] = serialized_credit.data
                context["message"].pop("quantity_list")
                context['message']['item_list'] = custom_item_serializer(credit.item_list, credit.quantity_list)
                return Response(context, status=status.HTTP_200_OK)

            else:
                context['message'] = "You don't have access."
                return Response(context, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            print(e)
            context['message'] = "Credit Note not found"
            return Response(context, status=status.HTTP_404_NOT_FOUND)
    
    elif request.method == 'PUT':
        try:
            credit = CreditNote.objects.get(id=id)
            form = CNEditSerializer(instance=credit, data=request.data)
            context = {}

            if form.is_valid():
                updated_credit = form.update(credit, form.validated_data)
                context['message'] = "success"
                context['credit'] = {"id": updated_credit.id, **form.validated_data}
                # context['credit']['item_list'] = custom_item_serializer(updated_credit.item_list, updated_credit.quantity_list)

                if form.validated_data['download']:
                    buffer = io.BytesIO()
                    invoice_ser = CreditNoteSerailizer(updated_credit).data
                    invoice_ser['item_list'] = pdf_item_serializer(updated_credit.item_list, updated_credit.quantity_list)
                    file_name = get_report(buffer, invoice_ser, CURRENCY_MAPPING[request.user.currency], "credit note", request, form.validated_data['terms'])

                    buffer.seek(0)
                    return FileResponse(buffer, as_attachment=True, filename=file_name)

                elif form.validated_data['send_email']:
                    # for sending email when creating a new document
                    now = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
                    file_name = f"{'credit note'.title()} for {request.user.email} - {now}.pdf"
                    invoice_ser = CreditNoteSerailizer(updated_credit).data
                    invoice_ser['item_list'] = pdf_item_serializer(updated_credit.item_list, updated_credit.quantity_list)
                    file_name = get_report(file_name, invoice_ser, CURRENCY_MAPPING[request.user.currency], "credit note", request, form.validated_data['terms'])
                    body = "Attached to the email is the receipt of your transaction on https://www.clappe.com"
                    subject = "Transaction Receipt"
                    send_my_email(updated_credit.customer.email, body, subject, file_name)
                    os.remove(file_name)
                    updated_credit.emailed = True
                    updated_credit.save()

                return Response(context, status=status.HTTP_200_OK)

            else:
                errors = {**form.errors}
                new_errors = {key: value[0] for key,value in errors.items()}
                errors_list = [k for k in new_errors.values()]
                context = {'message': errors_list[0], 'errors': new_errors}

                return Response(context, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            print(e)
            context = {'message' :"Credit Note not found"}
            return Response(context, status=status.HTTP_404_NOT_FOUND)

    
    elif request.method == "DELETE":
        try:
            credit = CreditNote.objects.get(id=id)
            credit.delete()
            context = {"message": "Success"}

            return Response(context, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            context = {"message": "Credit Note not found"}
            
            return Response(context, status=status.HTTP_404_NOT_FOUND)






@api_view(["GET", "POST"])
@authentication_classes((MyAuthentication, ))
@permission_classes((IsAuthenticated, ))
def pay_credit(request):
    
    if request.method == "POST":
        form = PayCNSerializer(data=request.data)
        context = {}

        if form.is_valid():
            try:
                credit = CreditNote.objects.get(id=form.validated_data['credit_id'])
                if credit.status == "Paid":
                    context['message'] = "Credit Note have been paid for already"
                    return Response(context, status=status.HTTP_400_BAD_REQUEST)

                else:
                    pay_credit = form.save(credit)
                    context['message'] = "success"
                    context['pay_credit'] = {"id": pay_credit.id, **form.data}

                    return Response(context, status=status.HTTP_200_OK)

            except Exception as e:
                print(e)

        else:
            errors = {**form.errors}
            new_errors = {key: value[0] for key,value in errors.items()}
            errors_list = [k for k in new_errors.values()]
            context = {'message': errors_list[0], 'errors': new_errors}

            return Response(context, status=status.HTTP_400_BAD_REQUEST)

    else:
        context = {}
        context['message'] = "New credit note payment"
        context['required_fields'] = ["payment_type", "paid_date", "paid_amount", "payment_method", "reference", "credit_id"]

        return Response(context, status.HTTP_200_OK)








###################################################### delivery note #####################################################################

@api_view(["GET"])
@authentication_classes((MyAuthentication, ))
@permission_classes((IsAuthenticated, ))
def all_delivery(request):

    my_delivery = DeliveryNote.objects.filter(vendor=request.user.id).all()
    context = {}

    if len(my_delivery) > 0:
        deliverys = DNSerailizer(my_delivery, many=True)
        total_invoices = []
        for invoice in deliverys.data:
            invoice['item_list'] = custom_item_serializer(invoice['item_list'], invoice['quantity_list'])
            invoice.pop("quantity_list")
            total_invoices.append(invoice)

        context = {"message": total_invoices}
        return Response(context, status=status.HTTP_200_OK)

    else:
        context['message'] = "You don't have any Delivery Note"
        return Response(context, status=status.HTTP_404_NOT_FOUND)




@api_view(["GET", "POST"])
@authentication_classes((MyAuthentication, ))
@permission_classes((IsAuthenticated, ))
def create_delivery(request):

    if request.method == "POST":
        form = DNCreateSerializer(data=request.data)
        context = {}

        if form.is_valid():
            new_delivery = form.save(request)
            context['message'] = "success"
            context['delivery'] = {"id": new_delivery.id, **form.data}
            # context['delivery']['item_list'] = custom_item_serializer(new_delivery.item_list, new_delivery.quantity_list)

            if form.validated_data['download']:
                buffer = io.BytesIO()
                invoice_ser = DNSerailizer(new_delivery).data
                invoice_ser['item_list'] = pdf_item_serializer(new_delivery.item_list, new_delivery.quantity_list)
                file_name = get_report(buffer, invoice_ser, CURRENCY_MAPPING[request.user.currency], "delivery note", request, form.validated_data['terms'])

                buffer.seek(0)
                return FileResponse(buffer, as_attachment=True, filename=file_name)


            elif form.validated_data['send_email']:
                # for sending email when creating a new document
                now = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
                file_name = f"{'delivery note'.title()} for {request.user.email} - {now}.pdf"
                invoice_ser = DNSerailizer(new_delivery).data
                invoice_ser['item_list'] = pdf_item_serializer(new_delivery.item_list, new_delivery.quantity_list)
                file_name = get_report(file_name, invoice_ser, CURRENCY_MAPPING[request.user.currency], "delivery note", request, form.validated_data['terms'])
                body = "Attached to the email is the receipt of your transaction on https://www.clappe.com"
                subject = "Transaction Receipt"
                send_my_email(new_delivery.customer.email, body, subject, file_name)
                os.remove(file_name)
                new_delivery.emailed = True
                new_delivery.save()

            return Response(context, status=status.HTTP_200_OK)

        else:
            errors = {**form.errors}
            new_errors = {key: value[0] for key,value in errors.items()}
            errors_list = [k for k in new_errors.values()]
            context = {'message': errors_list[0], 'errors': new_errors}

            return Response(context, status=status.HTTP_400_BAD_REQUEST)
    else:
        context = {"message": "create delivery note page", "required fields": [
                 "customer_id", "taxable", "dn_pref", "logo_path", 
                    "dn_number", "dn_date", "po_number", "due_date", "ship_to", "shipping_address", "notes", "item_list", 
                    "item_total", "tax", "add_charges", "grand_total"]}

        return Response(context, status=status.HTTP_200_OK)





@api_view(["GET", "PUT", "DELETE"])
@authentication_classes((MyAuthentication, ))
@permission_classes((IsAuthenticated, ))
def edit_delivery(request, id):

    context = {}

    if request.method == "GET":
        try:
            delivery = DeliveryNote.objects.get(id=id)
            if delivery.vendor == request.user:
                serialized_delivery = DNSerailizer(delivery)
                context['message'] = serialized_delivery.data
                context["message"].pop("quantity_list")
                context['message']['item_list'] = custom_item_serializer(delivery.item_list, delivery.quantity_list)
                return Response(context, status=status.HTTP_200_OK)

            else:
                context['message'] = "You don't have access."
                return Response(context, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            print(e)
            context['message'] = "Delivery Note not found"
            return Response(context, status=status.HTTP_404_NOT_FOUND)
    
    elif request.method == 'PUT':
        try:
            delivery = DeliveryNote.objects.get(id=id)
            form = DNEditSerializer(instance=delivery, data=request.data)
            context = {}

            if form.is_valid():
                updated_delivery = form.update(delivery, form.validated_data)
                context['message'] = "success"
                context['delivery'] = {"id": updated_delivery.id, **form.validated_data}
                # context['delivery']['item_list'] = custom_item_serializer(updated_delivery.item_list, updated_delivery.quantity_list)

                if form.validated_data['download']:
                    buffer = io.BytesIO()
                    invoice_ser = DNSerailizer(updated_delivery).data
                    invoice_ser['item_list'] = pdf_item_serializer(updated_delivery.item_list, updated_delivery.quantity_list)
                    file_name = get_report(buffer, invoice_ser, CURRENCY_MAPPING[request.user.currency], "delivery note", request, form.validated_data['terms'])

                    buffer.seek(0)
                    return FileResponse(buffer, as_attachment=True, filename=file_name)

                elif form.validated_data['send_email']:
                    # for sending email when creating a new document
                    now = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
                    file_name = f"{'delivery note'.title()} for {request.user.email} - {now}.pdf"
                    invoice_ser = DNSerailizer(updated_delivery).data
                    invoice_ser['item_list'] = pdf_item_serializer(updated_delivery.item_list, updated_delivery.quantity_list)
                    file_name = get_report(file_name, invoice_ser, CURRENCY_MAPPING[request.user.currency], "delivery note", request, form.validated_data['terms'])
                    body = "Attached to the email is the receipt of your transaction on https://www.clappe.com"
                    subject = "Transaction Receipt"
                    send_my_email(updated_delivery.customer.email, body, subject, file_name)
                    os.remove(file_name)
                    updated_delivery.emailed = True
                    updated_delivery.save()

                return Response(context, status=status.HTTP_200_OK)

            else:
                errors = {**form.errors}
                new_errors = {key: value[0] for key,value in errors.items()}
                errors_list = [k for k in new_errors.values()]
                context = {'message': errors_list[0], 'errors': new_errors}

                return Response(context, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            print(e)
            context = {'message' :"Delivery Note not found"}
            return Response(context, status=status.HTTP_404_NOT_FOUND)

    
    elif request.method == "DELETE":
        try:
            delivery = DeliveryNote.objects.get(id=id)
            delivery.delete()
            context = {"message": "Success"}

            return Response(context, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            context = {"message": "Delivery Note not found"}
            
            return Response(context, status=status.HTTP_404_NOT_FOUND)






@api_view(["GET", "POST"])
@authentication_classes((MyAuthentication, ))
@permission_classes((IsAuthenticated, ))
def pay_delivery(request):
    
    if request.method == "POST":
        form = PayDNSerializer(data=request.data)
        context = {}

        if form.is_valid():
            try:
                delivery = DeliveryNote.objects.get(id=form.validated_data['delivery_id'])
                if delivery.status == "Paid":
                    context['message'] = "Delivery Note have been paid for already"
                    return Response(context, status=status.HTTP_400_BAD_REQUEST)

                else:
                    pay_delivery = form.save(delivery)
                    context['message'] = "success"
                    context['pay_delivery'] = {"id": pay_delivery.id, **form.data}

                    return Response(context, status=status.HTTP_200_OK)

            except Exception as e:
                print(e)

        else:
            errors = {**form.errors}
            new_errors = {key: value[0] for key,value in errors.items()}
            errors_list = [k for k in new_errors.values()]
            context = {'message': errors_list[0], 'errors': new_errors}

            return Response(context, status=status.HTTP_400_BAD_REQUEST)

    else:
        context = {}
        context['message'] = "New delivery note payment"
        context['required_fields'] = ["payment_type", "paid_date", "paid_amount", "payment_method", "reference", "delivery_id"]

        return Response(context, status.HTTP_200_OK)
















############################################################# other ################################################################

@api_view(["GET", "POST"])
@authentication_classes((MyAuthentication, ))
@permission_classes((IsAuthenticated, ))
@parser_classes([FormParser, MultiPartParser])
def change_profile(request):

    if request.method == "GET":
        my_profile = ProfileSerializer(instance=request.user)
        context = {**my_profile.data}
        return Response(context, status=status.HTTP_200_OK)

    if request.method == "POST":
        context = {}

        form = ProfileSerializer(instance=request.user, data=request.data)
        if form.is_valid():
            updated_profile = form.update(request.user, form.validated_data)
            context['message'] = "Success"
            context['profile'] = {**form.validated_data}
            if "photo_path" in context['profile'].keys():
                context['profile']['photo_path'] = updated_profile.photo_path
            
            if "logo_path" in context['profile'].keys():
                # context['profile']['photo_path'] = updated_profile.photo_path
                context['profile']['logo_path'] = updated_profile.logo_path
            
            if "signature" in context['profile'].keys():
                context['profile']['signature'] = updated_profile.signature

            return Response(context, status=status.HTTP_200_OK)

        else:
            errors = {**form.errors}
            new_errors = {key: value[0] for key,value in errors.items()}
            errors_list = [k for k in new_errors.values()]
            context = {'message': errors_list[0], 'errors': new_errors}

        return Response(context, status=status.HTTP_400_BAD_REQUEST)






@api_view(["GET", "POST"])
@authentication_classes((MyAuthentication, ))
@permission_classes((IsAuthenticated, ))
def change_password(request):

    if request.method == "GET":
        context = {}
        context['message'] = "change password page"
        context['required_fields'] = ["old_password", "new_password", "confirm_password"]
        return Response(context, status=status.HTTP_200_OK)



    if request.method == "POST":
        context = {}
        # my_profile = PasswordChangeSerializer(instance=request.user)

        form = PasswordChangeSerializer(instance=request.user, data=request.data)
        if form.is_valid():
            code, message = form.save(request)

            if code == 200:
                context['message'] = message
                return Response(context, status=status.HTTP_200_OK)

            else:
                context['message'] = message
                return Response(context, status=status.HTTP_400_BAD_REQUEST)


        else:
            errors = {**form.errors}
            new_errors = {key: value[0] for key,value in errors.items()}
            errors_list = [k for k in new_errors.values()]
            context = {'message': errors_list[0], 'errors': new_errors}

            return Response(context, status=status.HTTP_400_BAD_REQUEST)










@api_view(["GET", "POST"])
@authentication_classes((MyAuthentication, ))
@permission_classes((IsAuthenticated, ))
def change_preference(request):

    my_preference = PreferenceSerializer(instance=request.user)


    if request.method == "GET":
            context = {**my_preference.data}
            return Response(context, status=status.HTTP_200_OK)
    

    if request.method == "POST":
        context = {}
        pref_ser = PreferenceSerializer(instance=my_preference, data=request.data)

        if pref_ser.is_valid():
            result = pref_ser.update(request.user)

            context['message'] = "Preference Saved successfully"
            context['preference'] = {**pref_ser.validated_data}

            return Response(context, status=status.HTTP_200_OK)

        else:

            errors = {**pref_ser.errors}
            new_errors = {key: value[0] for key,value in errors.items()}
            errors_list = [k for k in new_errors.values()]
            context = {'message': errors_list[0], 'errors': new_errors}

            return Response(context, status=status.HTTP_400_BAD_REQUEST)











# @api_view(["GET", "POST"])
# @authentication_classes((MyAuthentication, ))
# @permission_classes((IsAuthenticated, ))
# def change_payment(request):

#     my_preference = PaymentSerializer(instance=request.user)


#     if request.method == "GET":
#             context = {**my_preference.data}
#             return Response(context, status=status.HTTP_200_OK)
    

#     if request.method == "POST":
#         context = {}
#         payment_info = PaymentSerializer(instance=my_preference, data=request.data)

#         if payment_info.is_valid():
#             result = payment_info.update(request)

#             context['message'] = "Payment info Saved successfully"
#             context['preference'] = {**payment_info.validated_data}

#             return Response(context, status=status.HTTP_200_OK)

#         else:

#             errors = {**payment_info.errors}
#             new_errors = {key: value[0] for key,value in errors.items()}
#             errors_list = [k for k in new_errors.values()]
#             context = {'message': errors_list[0], 'errors': new_errors}

#             return Response(context, status=status.HTTP_400_BAD_REQUEST)






@api_view(["GET", "POST"])
@authentication_classes((MyAuthentication, ))
@permission_classes((IsAuthenticated, ))
def get_number(request):

    if request.method == "POST":
        num_type = request.data.get("type", None)

        context = {}

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


        else:
            context['error'] = "pass either of invoice, proforma, pruchase_order, estimate, quote, receipt, credit_note, delivery_note as the type"

            return Response(context, status.HTTP_400_BAD_REQUEST)


        context['message'] = "00" + str(count)

        return Response(context, status.HTTP_200_OK)

    else:
        context = {}
        context['error'] = "pass either of invoice, proforma, pruchase_order, estimate, quote, receipt, credit_note, delivery_note as the type"

        return Response(context, status.HTTP_200_OK)








#################################################### report #######################################################################



@api_view(["GET"])
@authentication_classes((MyAuthentication, ))
@permission_classes((IsAuthenticated, ))
def customer_report(request):
    context = {}

    # report_type = request.query_params.get("type", None)
    measure = request.query_params.get("measure", None)
    start_date = request.query_params.get("start", None)
    end_date = request.query_params.get("end", None)

    if measure != "searchable window":

        if start_date:
            if end_date:
                
                # 1.1
                if measure == "customer search":
                    customers = Customer.objects.filter(vendor=request.user.id)\
                                                .filter(date_created__gte=start_date)\
                                                .filter(date_created__lte=end_date).order_by("first_name").all()
                    if len(customers) > 0:
                        customer_ser = CustomerSerializer(customers, many=True)
                        context["message"] = customer_ser.data
                        return Response(context, status=status.HTTP_200_OK)

                    else:
                        context["message"] = "No customers were created within this date range"
                        return Response(context, status=status.HTTP_404_NOT_FOUND)
                
                # 1.2
                elif measure == "purchase summary":
                    context = {}
                    customers = Customer.objects.filter(vendor=request.user.id)\
                                                .order_by("first_name").all().values_list("id", flat=True)
                    for id in list(customers):

                        invoices = Invoice.objects.filter(ucstomer_id=id)\
                                                    .filter(date_created__lte=end_date)\
                                                    .filter(date_created__gte=start_date).order_by("date_created")
                        invoice_ser = InvoiceSerializer(invoices, many=True)

                        proformas = ProformaInvoice.objects.filter(ucstomer_id=id)\
                                                    .filter(date_created__lte=end_date)\
                                                    .filter(date_created__gte=start_date).order_by("date_created")
                        proforma_ser = ProformerInvoiceSerailizer(proformas, many=True)

                        purchases = PurchaseOrder.objects.filter(ucstomer_id=id)\
                                                    .filter(date_created__lte=end_date)\
                                                    .filter(date_created__gte=start_date).order_by("date_created")
                        purchase_ser = PurchaseOrderSerailizer(purchases, many=True)

                        estimates = Estimate.objects.filter(ucstomer_id=id)\
                                                    .filter(date_created__lte=end_date)\
                                                    .filter(date_created__gte=start_date).order_by("date_created")
                        estimate_ser = EstimateSerailizer(estimates, many=True)

                        quotes = Quote.objects.filter(ucstomer_id=id)\
                                                    .filter(date_created__lte=end_date)\
                                                    .filter(date_created__gte=start_date).order_by("date_created")
                        quote_ser = QuoteSerailizer(quotes, many=True)

                        receipts = Receipt.objects.filter(ucstomer_id=id)\
                                                    .filter(date_created__lte=end_date)\
                                                    .filter(date_created__gte=start_date).order_by("date_created")
                        receipt_ser = ReceiptSerailizer(receipts, many=True)

                        credits = CreditNote.objects.filter(ucstomer_id=id)\
                                                    .filter(date_created__lte=end_date)\
                                                    .filter(date_created__gte=start_date).order_by("date_created")
                        credit_ser = CreditNoteSerailizer(credits, many=True)

                        deliverys = DeliveryNote.objects.filter(ucstomer_id=id)\
                                                    .filter(date_created__lte=end_date)\
                                                    .filter(date_created__gte=start_date).order_by("date_created")
                        delivery_ser = DNSerailizer(deliverys, many=True)

                        context["customer_id"] = id
                        context[id]['invoice'] = invoice_ser.data
                        context[id]['proforma'] = proforma_ser.data
                        context[id]['estimate'] = estimate_ser.data
                        context[id]['quote'] = quote_ser.data
                        context[id]['receipt'] = receipt_ser.data
                        context[id]['credit'] = credit_ser.data
                        context[id]['purchase'] = purchase_ser.data
                        context[id]['delivery'] = delivery_ser.data

                    return Response(context, status=status.HTTP_200_OK)
                
                # 1.3
                elif measure == "transactions":
                    context = {}
                    customers = Customer.objects.filter(vendor=request.user.id)\
                                                .order_by("first_name").all().values_list("id", flat=True)
                    for id in list(customers):

                        invoices = Invoice.objects.filter(ucstomer_id=id)\
                                                    .filter(date_created__lte=end_date)\
                                                    .filter(date_created__gte=start_date).order_by("date_created")
                        invoice_ser = InvoiceSerializer(invoices, many=True)

                        proformas = ProformaInvoice.objects.filter(ucstomer_id=id)\
                                                    .filter(date_created__lte=end_date)\
                                                    .filter(date_created__gte=start_date).order_by("date_created")
                        proforma_ser = ProformerInvoiceSerailizer(proformas, many=True)

                        purchases = PurchaseOrder.objects.filter(ucstomer_id=id)\
                                                    .filter(date_created__lte=end_date)\
                                                    .filter(date_created__gte=start_date).order_by("date_created")
                        purchase_ser = PurchaseOrderSerailizer(purchases, many=True)

                        estimates = Estimate.objects.filter(ucstomer_id=id)\
                                                    .filter(date_created__lte=end_date)\
                                                    .filter(date_created__gte=start_date).order_by("date_created")
                        estimate_ser = EstimateSerailizer(estimates, many=True)

                        quotes = Quote.objects.filter(ucstomer_id=id)\
                                                    .filter(date_created__lte=end_date)\
                                                    .filter(date_created__gte=start_date).order_by("date_created")
                        quote_ser = QuoteSerailizer(quotes, many=True)

                        receipts = Receipt.objects.filter(ucstomer_id=id)\
                                                    .filter(date_created__lte=end_date)\
                                                    .filter(date_created__gte=start_date).order_by("date_created")
                        receipt_ser = ReceiptSerailizer(receipts, many=True)

                        credits = CreditNote.objects.filter(ucstomer_id=id)\
                                                    .filter(date_created__lte=end_date)\
                                                    .filter(date_created__gte=start_date).order_by("date_created")
                        credit_ser = CreditNoteSerailizer(credits, many=True)

                        deliverys = DeliveryNote.objects.filter(ucstomer_id=id)\
                                                    .filter(date_created__lte=end_date)\
                                                    .filter(date_created__gte=start_date).order_by("date_created")
                        delivery_ser = DNSerailizer(deliverys, many=True)

                        context["customer_id"] = id

                        context[id]['invoice'] = invoice_ser.data
                        context[id]['invoice']["total_number"] = len(invoice_ser.data)
                        total_amount = 0
                        for inv in invoice_ser.data:
                            total_amount += int(inv['grand_total'])
                        context[id]['invoice']["total_amount"] = total_amount

                        context[id]['proforma'] = proforma_ser.data
                        context[id]['proforma']["total_number"] = len(proforma_ser.data)
                        total_amount = 0
                        for inv in proforma_ser.data:
                            total_amount += int(inv['grand_total'])
                        context[id]['proforma']["total_amount"] = total_amount

                        context[id]['estimate'] = estimate_ser.data
                        context[id]['estimate']["total_number"] = len(estimate_ser.data)
                        total_amount = 0
                        for inv in estimate_ser.data:
                            total_amount += int(inv['grand_total'])
                        context[id]['estimate']["total_amount"] = total_amount

                        context[id]['quote'] = quote_ser.data
                        context[id]['quote']["total_number"] = len(quote_ser.data)
                        total_amount = 0
                        for inv in quote_ser.data:
                            total_amount += int(inv['grand_total'])
                        context[id]['quote']["total_amount"] = total_amount

                        context[id]['receipt'] = receipt_ser.data
                        context[id]['receipt']["total_number"] = len(receipt_ser.data)
                        total_amount = 0
                        for inv in receipt_ser.data:
                            total_amount += int(inv['grand_total'])
                        context[id]['receipt']["total_amount"] = total_amount

                        context[id]['credit'] = credit_ser.data
                        context[id]['credit']["total_number"] = len(credit_ser.data)
                        total_amount = 0
                        for inv in credit_ser.data:
                            total_amount += int(inv['grand_total'])
                        context[id]['credit']["total_amount"] = total_amount

                        context[id]['purchase'] = purchase_ser.data
                        context[id]['purchase']["total_number"] = len(purchase_ser.data)
                        total_amount = 0
                        for inv in purchase_ser.data:
                            total_amount += int(inv['grand_total'])
                        context[id]['purchase']["total_amount"] = total_amount

                        context[id]['delivery'] = delivery_ser.data
                        context[id]['delivery']["total_number"] = len(delivery_ser.data)
                        total_amount = 0
                        for inv in delivery_ser.data:
                            total_amount += int(inv['grand_total'])
                        context[id]['delivery']["total_amount"] = total_amount


                    return Response(context, status=status.HTTP_200_OK)

                
                # 1.4
                elif measure == "company name":
                    customers = Customer.objects.filter(vendor=request.user.id)\
                                                .filter(date_created__gte=start_date)\
                                                .filter(date_created__lte=end_date).order_by("business_name").all()
                    if len(customers) > 0:
                        customer_ser = CustomerSerializer(customers, many=True)
                        context["message"] = customer_ser.data

                        return Response(context, status=status.HTTP_200_OK)

                    else:
                        context["message"] = "No customers were created within this date range"
                        return Response(context, status=status.HTTP_404_NOT_FOUND)


                # 1.5
                elif measure == "customer name":
                    customers = Customer.objects.filter(vendor=request.user.id)\
                                                .filter(date_created__gte=start_date)\
                                                .filter(date_created__lte=end_date).order_by("first_name").all()
                    if len(customers) > 0:
                        customer_ser = CustomerSerializer(customers, many=True)
                        context["message"] = customer_ser.data
                        
                        return Response(context, status=status.HTTP_200_OK)

                    else:
                        context["message"] = "No customers were created within this date range"
                        return Response(context, status=status.HTTP_404_NOT_FOUND)


                # 1.6
                elif measure == "customer and company":
                    customers = Customer.objects.filter(vendor=request.user.id)\
                                                .filter(date_created__gte=start_date)\
                                                .filter(date_created__lte=end_date).order_by("first_name", "business_name").all()
                    if len(customers) > 0:
                        customer_ser = CustomerSerializer(customers, many=True)
                        context["message"] = customer_ser.data
                        
                        return Response(context, status=status.HTTP_200_OK)

                    else:
                        context["message"] = "No customers were created within this date range"
                        return Response(context, status=status.HTTP_404_NOT_FOUND)


                # 1.8
                elif measure == "area code":
                    customers = Customer.objects.filter(vendor=request.user.id)\
                                                .filter(date_created__gte=start_date)\
                                                .filter(date_created__lte=end_date).order_by("phone_number").all()
                    if len(customers) > 0:
                        customer_ser = CustomerSerializer(customers, many=True)
                        context["message"] = customer_ser.data
                        
                        return Response(context, status=status.HTTP_200_OK)

                    else:
                        context["message"] = "No customers were created within this date range"
                        return Response(context, status=status.HTTP_404_NOT_FOUND)
                
                else:
                    context["message"] = "Incorrect measure"
                    return Response(context, status=status.HTTP_200_OK)

            else:

                context['message'] = "If you set start date, you have to set end date too"
                return Response(context, status=status.HTTP_400_BAD_REQUEST)

        else:
            context["message"] = "I think you need to pass a date range..."
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
    
    else:
        # 1.7
        customers = Customer.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date).all()
        if len(customers) > 0:
            customer_name = customers.order_by("first_name")
            customer_company = customers.order_by("business_name")
            customer_phone = customers.order_by("phone_number")

            # customer_ser = CustomerSerializer(customers, many=True)
            customer_name_ser = CustomerSerializer(customer_name, many=True)
            customer_company_ser = CustomerSerializer(customer_company, many=True)
            customer_phone_ser = CustomerSerializer(customer_phone, many=True)

            context["message"]['by_name'] = customer_name_ser.data
            context["message"]['by_company'] = customer_company_ser.data
            context["message"]['by_phone'] = customer_phone_ser.data
            
            return Response(context, status=status.HTTP_200_OK)

        else:
            context["message"] = "No customers were created within this date range"
            return Response(context, status=status.HTTP_404_NOT_FOUND)
        

    



@api_view(["GET"])
@authentication_classes((MyAuthentication, ))
@permission_classes((IsAuthenticated, ))
def invoice_report(request):
    context = {}
    measure = request.query_params.get("measure", None)
    start_date = request.query_params.get("start", None)
    end_date = request.query_params.get("end", None)

    # 2.1
    if measure == "invoice search":
        invoices = Invoice.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date).all().order_by("date_created")
        if len(invoices) > 0:
            invoice_ser = InvoiceSerializer(invoices, many=True)
            context['message'] = invoice_ser.data

            return Response(context, status=status.HTTP_200_OK)

        else:
            context["message"] = "No invoices were created within this date range"
            return Response(context, status=status.HTTP_404_NOT_FOUND)
    
    # 2.2
    elif measure == "amount search":
        invoices = Invoice.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date).all().order_by("date_created")

        if len(invoices) > 0:
            invoice_ser = InvoiceSerializer(invoices, many=True)
            context['message'] = invoice_ser.data

            return Response(context, status=status.HTTP_200_OK)

        else:
            context["message"] = "No invoices were created within this date range"
            return Response(context, status=status.HTTP_404_NOT_FOUND)
    

    # 2.3
    elif measure == "per customer":
        invoices = Invoice.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date).all().order_by("date_created")

        if len(invoices) > 0:
            invoice_ser = InvoiceSerializer(invoices, many=True)
            total_data = {}
            for inv in invoice_ser.data:
                full_name = inv['customer']['first_name'] + " " + inv['customer']['last_name']
                if full_name in total_data:
                    total_data[full_name] += float(inv['grand_total'])
                else:
                    total_data[full_name] = 0
            
            final_data = []
            for k,v in total_data.items():
                final_data.append({"full_name": k, "total_amount": v})

            context['message'] = final_data


            return Response(context, status=status.HTTP_200_OK)

        else:
            context["message"] = "No invoices were created within this date range"
            return Response(context, status=status.HTTP_404_NOT_FOUND)
    
    # 2.4
    elif measure == "total per date":
        context = {}
        how = request.query_params.get("how")

        if how == "hour":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_hours = int((interval.days*1440 + interval.seconds/60)/60)

            # total_data = {}
            for hour in range(0, total_hours+1):
                current_time = start_time + timedelta(hours=hour)
                invoices = Invoice.objects.filter(date_created__date=current_time.date())\
                                          .filter(date_created__hour=current_time.hour)
                invoice_ser = InvoiceSerializer(invoices, many=True)

                # for inv in invoice_ser.data:
                total_amount = 0
                for inv in invoice_ser.data:
                        total_amount += float(inv['grand_total'])

                context[current_time.strftime('%Y-%m-%d %I%p')] = total_amount
            
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "day":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_days = int(((interval.days*1440 + interval.seconds/60)/60)/24)

            # total_data = {}
            for day in range(0, total_days+1):
                current_time = start_time + timedelta(days=day)
                invoices = Invoice.objects.filter(date_created__date=current_time.date())

                invoice_ser = InvoiceSerializer(invoices, many=True)

                total_amount = 0
                for inv in invoice_ser.data:
                        total_amount += float(inv['grand_total'])

                context[current_time.strftime('%Y-%m-%d')] = total_amount
                
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "week":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_weeks = int((((interval.days*1440 + interval.seconds/60)/60)/24)/7)

            if total_weeks > 0:
                for week in range(0, total_weeks+1):
                    start_time += timedelta(weeks=week)
                    current_week = start_time + timedelta(weeks=week+1)

                    if current_week > end_time:
                        current_week = end_time

                    invoices = Invoice.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)
                    invoice_ser = InvoiceSerializer(invoices, many=True)
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"

                    total_amount = 0
                    for inv in invoice_ser.data:
                            total_amount += float(inv['grand_total'])

                    context[key] = total_amount
                        
                    # context[key] = invoice_ser.data
                
                return Response(context, status=status.HTTP_200_OK)

            else:
                invoices = Invoice.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date).all().order_by("date_created")

                if len(invoices) > 0:
                    invoice_ser = InvoiceSerializer(invoices, many=True)
                    key = f"{start_date} - {end_date}"

                    total_amount = 0
                    for inv in invoice_ser.data:
                            total_amount += float(inv['grand_total'])

                    context[key] = total_amount
                    # context['message'] = invoice_ser.data

                    return Response(context, status=status.HTTP_200_OK)

                else:
                    context["message"] = "No invoices were created within this date range"
                    return Response(context, status=status.HTTP_404_NOT_FOUND)
            
            # return Response(context, status=status.HTTP_200_OK)
        
        elif how == "months":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_months = int(((((interval.days*1440 + interval.seconds/60)/60)/24)/7)/4)

            if total_months > 0:
                for week in range(0, total_months+1):
                    start_time += timedelta(weeks=week*4)
                    current_week = start_time + timedelta(weeks=(week+1)*4)

                    if current_week > end_time:
                        current_week = end_time

                    invoices = Invoice.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)
                    invoice_ser = InvoiceSerializer(invoices, many=True)
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"
                    # key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"

                    total_amount = 0
                    for inv in invoice_ser.data:
                            total_amount += float(inv['grand_total'])

                    context[key] = total_amount
                    # context[key] = invoice_ser.data
                return Response(context, status=status.HTTP_200_OK)

            else:
                invoices = Invoice.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date).all().order_by("date_created")

                if len(invoices) > 0:
                    invoice_ser = InvoiceSerializer(invoices, many=True)
                    key = f"{start_date} - {end_date}"

                    total_amount = 0
                    for inv in invoice_ser.data:
                            total_amount += float(inv['grand_total'])

                    context[key] = total_amount
                    # context['message'] = invoice_ser.data

                    return Response(context, status=status.HTTP_200_OK)

                else:
                    context["message"] = "No invoices were created within this date range"
                    return Response(context, status=status.HTTP_404_NOT_FOUND)
            
            # return Response(context, status=status.HTTP_200_OK)
        

        elif how == "custom date":
            invoices = Invoice.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date).all().order_by("date_created")

            if len(invoices) > 0:
                invoice_ser = InvoiceSerializer(invoices, many=True)
                key = f"{start_date} - {end_date}"

                total_amount = 0
                for inv in invoice_ser.data:
                        total_amount += float(inv['grand_total'])

                context[key] = total_amount
                # context['message'] = invoice_ser.data

                return Response(context, status=status.HTTP_200_OK)

            else:
                context["message"] = "No invoices were created within this date range"
                return Response(context, status=status.HTTP_404_NOT_FOUND)


    
    # 2.5
    elif measure == "count invoice email":
        context = {}
        how = request.query_params.get("how")

        if how == "hour":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_hours = int((interval.days*1440 + interval.seconds/60)/60)

            
            for hour in range(0, total_hours+1):
                current_time = start_time + timedelta(hours=hour)
                emailed_count = Invoice.objects.filter(date_created__date=current_time.date())\
                                          .filter(date_created__hour=current_time.hour)\
                                            .filter(emailed=True).count()
                
                context[current_time.strftime('%Y-%m-%d %I%p')] = emailed_count
                

            
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "day":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_days = int(((interval.days*1440 + interval.seconds/60)/60)/24)

            
            for day in range(0, total_days+1):
                current_time = start_time + timedelta(days=day)
                
                emailed_count = Invoice.objects.filter(date_created__date=current_time.date())\
                                            .filter(emailed=True).count()
                
                context[current_time.strftime('%Y-%m-%d')] = emailed_count

                

                
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "week":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_weeks = int((((interval.days*1440 + interval.seconds/60)/60)/24)/7)

            if total_weeks > 0:
                for week in range(0, total_weeks+1):
                    start_time += timedelta(weeks=week)
                    current_week = start_time + timedelta(weeks=week+1)

                    if current_week > end_time:
                        current_week = end_time

                    emailed_count = Invoice.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)\
                                                .filter(emailed=True).count()
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"
                    context[key] = emailed_count
                            
                    
                
                return Response(context, status=status.HTTP_200_OK)

            else:
                emailed_count = Invoice.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(emailed=True)\
                            .count()

                key = f"{start_date} - {end_date}"
                context[key] = emailed_count
                return Response(context, status=status.HTTP_200_OK)
                
        
        elif how == "months":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_months = int(((((interval.days*1440 + interval.seconds/60)/60)/24)/7)/4)

            if total_months > 0:
                for week in range(0, total_months+1):
                    start_time += timedelta(weeks=week*4)
                    current_week = start_time + timedelta(weeks=(week+1)*4)

                    if current_week > end_time:
                        current_week = end_time

                    emailed_count = Invoice.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)\
                                                .filter(emailed=True).count()
                    
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"
                    context[key] = emailed_count
                    
                return Response(context, status=status.HTTP_200_OK)

            else:
                emailed_count = Invoice.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(emailed=True).count()

                key = f"{start_date} - {end_date}"
                context[key] = emailed_count
                return Response(context, status=status.HTTP_200_OK)
                
        

        elif how == "custom date":
            emailed_count = Invoice.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(emailed=True).count()
                
            key = f"{start_date} - {end_date}"
            context[key] = emailed_count
            return Response(context, status=status.HTTP_200_OK)
    

    # 2.6
    elif measure == "detail invoice email":
        context = {}
        how = request.query_params.get("how")

        if how == "hour":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_hours = int((interval.days*1440 + interval.seconds/60)/60)

            # total_data = {}
            for hour in range(0, total_hours+1):
                current_time = start_time + timedelta(hours=hour)
                invoices = Invoice.objects.filter(date_created__date=current_time.date())\
                                          .filter(date_created__hour=current_time.hour)\
                                          .filter(emailed=True)
                invoice_ser = InvoiceSerializer(invoices, many=True)

                # context['message'] = invoice_ser.data
                context[current_time.strftime('%Y-%m-%d %I%p')] = invoice_ser.data

                # # for inv in invoice_ser.data:
                # total_amount = 0
                # for inv in invoice_ser.data:
                #         total_amount += float(inv['grand_total'])

            
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "day":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_days = int(((interval.days*1440 + interval.seconds/60)/60)/24)

            # total_data = {}
            for day in range(0, total_days+1):
                current_time = start_time + timedelta(days=day)
                invoices = Invoice.objects.filter(date_created__date=current_time.date())\
                                            .filter(emailed=True)

                invoice_ser = InvoiceSerializer(invoices, many=True)

                # total_amount = 0
                # for inv in invoice_ser.data:
                #         total_amount += float(inv['grand_total'])

                context[current_time.strftime('%Y-%m-%d')] = invoice_ser.data
                
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "week":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_weeks = int((((interval.days*1440 + interval.seconds/60)/60)/24)/7)

            if total_weeks > 0:
                for week in range(0, total_weeks+1):
                    start_time += timedelta(weeks=week)
                    current_week = start_time + timedelta(weeks=week+1)

                    if current_week > end_time:
                        current_week = end_time

                    invoices = Invoice.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)\
                                                .filter(emailed=True)
                    invoice_ser = InvoiceSerializer(invoices, many=True)
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    context[key] = invoice_ser.data                        
                
                return Response(context, status=status.HTTP_200_OK)

            else:
                invoices = Invoice.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(emailed=True)\
                            .order_by("date_created")

                if len(invoices) > 0:
                    invoice_ser = InvoiceSerializer(invoices, many=True)
                    key = f"{start_date} - {end_date}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    # context[key] = total_amount
                    context[key] = invoice_ser.data

                    return Response(context, status=status.HTTP_200_OK)

                else:
                    context["message"] = "No emailed invoices within this date range"
                    return Response(context, status=status.HTTP_404_NOT_FOUND)
            
            # return Response(context, status=status.HTTP_200_OK)
        
        elif how == "months":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_months = int(((((interval.days*1440 + interval.seconds/60)/60)/24)/7)/4)

            if total_months > 0:
                for week in range(0, total_months+1):
                    start_time += timedelta(weeks=week*4)
                    current_week = start_time + timedelta(weeks=(week+1)*4)

                    if current_week > end_time:
                        current_week = end_time

                    invoices = Invoice.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)\
                                                .filter(emailed=True)\
                                                .order_by("date_created")

                    invoice_ser = InvoiceSerializer(invoices, many=True)
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"
                    # key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    # context[key] = total_amount
                    context[key] = invoice_ser.data
                return Response(context, status=status.HTTP_200_OK)

            else:
                invoices = Invoice.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(emailed=True)\
                            .order_by("date_created")

                if len(invoices) > 0:
                    invoice_ser = InvoiceSerializer(invoices, many=True)
                    key = f"{start_date} - {end_date}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    # context[key] = total_amount
                    context[key] = invoice_ser.data

                    return Response(context, status=status.HTTP_200_OK)

                else:
                    context["message"] = "No emailed invoices within this date range"
                    return Response(context, status=status.HTTP_404_NOT_FOUND)
            
            # return Response(context, status=status.HTTP_200_OK)
        

        elif how == "custom date":
            invoices = Invoice.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(emailed=True)\
                            .order_by("date_created")

            if len(invoices) > 0:
                invoice_ser = InvoiceSerializer(invoices, many=True)
                key = f"{start_date} - {end_date}"

                # total_amount = 0
                # for inv in invoice_ser.data:
                #         total_amount += float(inv['grand_total'])

                # context[key] = total_amount
                context[key] = invoice_ser.data

                return Response(context, status=status.HTTP_200_OK)

            else:
                context["message"] = "No invoices were created within this date range"
                return Response(context, status=status.HTTP_404_NOT_FOUND)


    

    # 2.7
    elif measure == "count invoice overdue":

        context = {}
        how = request.query_params.get("how")

        if how == "hour":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_hours = int((interval.days*1440 + interval.seconds/60)/60)

            
            for hour in range(0, total_hours+1):
                current_time = start_time + timedelta(hours=hour)
                overdue_count = Invoice.objects.filter(date_created__date=current_time.date())\
                                          .filter(date_created__hour=current_time.hour)\
                                            .filter(status="Overdue").count()
                
                context[current_time.strftime('%Y-%m-%d %I%p')] = overdue_count
                

            
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "day":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_days = int(((interval.days*1440 + interval.seconds/60)/60)/24)

            
            for day in range(0, total_days+1):
                current_time = start_time + timedelta(days=day)
                
                overdue_count = Invoice.objects.filter(date_created__date=current_time.date())\
                                            .filter(status="Overdue").count()
                
                context[current_time.strftime('%Y-%m-%d')] = overdue_count

                

                
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "week":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_weeks = int((((interval.days*1440 + interval.seconds/60)/60)/24)/7)

            if total_weeks > 0:
                for week in range(0, total_weeks+1):
                    start_time += timedelta(weeks=week)
                    current_week = start_time + timedelta(weeks=week+1)

                    if current_week > end_time:
                        current_week = end_time

                    overdue_count = Invoice.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)\
                                                .filter(status="Overdue").count()
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"
                    context[key] = overdue_count
                            
                    
                
                return Response(context, status=status.HTTP_200_OK)

            else:
                overdue_count = Invoice.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(status="Overdue")\
                            .count()

                key = f"{start_date} - {end_date}"
                context[key] = overdue_count
                return Response(context, status=status.HTTP_200_OK)
                
        
        elif how == "months":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_months = int(((((interval.days*1440 + interval.seconds/60)/60)/24)/7)/4)

            if total_months > 0:
                for week in range(0, total_months+1):
                    start_time += timedelta(weeks=week*4)
                    current_week = start_time + timedelta(weeks=(week+1)*4)

                    if current_week > end_time:
                        current_week = end_time

                    overdue_count = Invoice.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)\
                                                .filter(status="Overdue").count()
                    
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"
                    context[key] = overdue_count
                    
                return Response(context, status=status.HTTP_200_OK)

            else:
                overdue_count = Invoice.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(status="Overdue").count()

                key = f"{start_date} - {end_date}"
                context[key] = overdue_count
                return Response(context, status=status.HTTP_200_OK)
                
        

        elif how == "custom date":
            overdue_count = Invoice.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(status="Overdue").count()
                
            key = f"{start_date} - {end_date}"
            context[key] = overdue_count
            return Response(context, status=status.HTTP_200_OK)


    # 2.8
    elif measure == "detail invoice overdue":
        context = {}
        how = request.query_params.get("how")

        if how == "hour":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_hours = int((interval.days*1440 + interval.seconds/60)/60)

            # total_data = {}
            for hour in range(0, total_hours+1):
                current_time = start_time + timedelta(hours=hour)
                invoices = Invoice.objects.filter(date_created__date=current_time.date())\
                                          .filter(date_created__hour=current_time.hour)\
                                          .filter(status="Overdue")\
                                            .order_by("date_created")
                invoice_ser = InvoiceSerializer(invoices, many=True)

                # context['message'] = invoice_ser.data
                context[current_time.strftime('%Y-%m-%d %I%p')] = invoice_ser.data

                # # for inv in invoice_ser.data:
                # total_amount = 0
                # for inv in invoice_ser.data:
                #         total_amount += float(inv['grand_total'])

            
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "day":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_days = int(((interval.days*1440 + interval.seconds/60)/60)/24)

            # total_data = {}
            for day in range(0, total_days+1):
                current_time = start_time + timedelta(days=day)
                invoices = Invoice.objects.filter(date_created__date=current_time.date())\
                                            .filter(status="Overdue")\
                                            .order_by("date_created")

                invoice_ser = InvoiceSerializer(invoices, many=True)

                # total_amount = 0
                # for inv in invoice_ser.data:
                #         total_amount += float(inv['grand_total'])

                context[current_time.strftime('%Y-%m-%d')] = invoice_ser.data
                
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "week":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_weeks = int((((interval.days*1440 + interval.seconds/60)/60)/24)/7)

            if total_weeks > 0:
                for week in range(0, total_weeks+1):
                    start_time += timedelta(weeks=week)
                    current_week = start_time + timedelta(weeks=week+1)

                    if current_week > end_time:
                        current_week = end_time

                    invoices = Invoice.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)\
                                                .filter(status="Overdue")\
                                                .order_by("date_created")
                    invoice_ser = InvoiceSerializer(invoices, many=True)
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    context[key] = invoice_ser.data                        
                
                return Response(context, status=status.HTTP_200_OK)

            else:
                invoices = Invoice.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(status="Overdue")\
                            .order_by("date_created")

                if len(invoices) > 0:
                    invoice_ser = InvoiceSerializer(invoices, many=True)
                    key = f"{start_date} - {end_date}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    # context[key] = total_amount
                    context[key] = invoice_ser.data

                    return Response(context, status=status.HTTP_200_OK)

                else:
                    context["message"] = "No emailed invoices within this date range"
                    return Response(context, status=status.HTTP_404_NOT_FOUND)
            
            # return Response(context, status=status.HTTP_200_OK)
        
        elif how == "months":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_months = int(((((interval.days*1440 + interval.seconds/60)/60)/24)/7)/4)

            if total_months > 0:
                for week in range(0, total_months+1):
                    start_time += timedelta(weeks=week*4)
                    current_week = start_time + timedelta(weeks=(week+1)*4)

                    if current_week > end_time:
                        current_week = end_time

                    invoices = Invoice.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)\
                                                .filter(status="Overdue")\
                                                .order_by("date_created")

                    invoice_ser = InvoiceSerializer(invoices, many=True)
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"
                    # key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    # context[key] = total_amount
                    context[key] = invoice_ser.data
                return Response(context, status=status.HTTP_200_OK)

            else:
                invoices = Invoice.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(status="Overdue")\
                            .order_by("date_created")

                if len(invoices) > 0:
                    invoice_ser = InvoiceSerializer(invoices, many=True)
                    key = f"{start_date} - {end_date}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    # context[key] = total_amount
                    context[key] = invoice_ser.data

                    return Response(context, status=status.HTTP_200_OK)

                else:
                    context["message"] = "No emailed invoices within this date range"
                    return Response(context, status=status.HTTP_404_NOT_FOUND)
            
            # return Response(context, status=status.HTTP_200_OK)
        

        elif how == "custom date":
            invoices = Invoice.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(status="Overdue")\
                            .order_by("date_created")

            if len(invoices) > 0:
                invoice_ser = InvoiceSerializer(invoices, many=True)
                key = f"{start_date} - {end_date}"

                # total_amount = 0
                # for inv in invoice_ser.data:
                #         total_amount += float(inv['grand_total'])

                # context[key] = total_amount
                context[key] = invoice_ser.data

                return Response(context, status=status.HTTP_200_OK)

            else:
                context["message"] = "No invoices were created within this date range"
                return Response(context, status=status.HTTP_404_NOT_FOUND)

    
    # 2.9
    elif measure == "detail invoice pending":
        context = {}
        how = request.query_params.get("how")

        if how == "hour":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_hours = int((interval.days*1440 + interval.seconds/60)/60)

            # total_data = {}
            for hour in range(0, total_hours+1):
                current_time = start_time + timedelta(hours=hour)
                invoices = Invoice.objects.filter(date_created__date=current_time.date())\
                                          .filter(date_created__hour=current_time.hour)\
                                          .filter(status="Pending")\
                                            .order_by("date_created")
                invoice_ser = InvoiceSerializer(invoices, many=True)

                # context['message'] = invoice_ser.data
                context[current_time.strftime('%Y-%m-%d %I%p')] = invoice_ser.data

                # # for inv in invoice_ser.data:
                # total_amount = 0
                # for inv in invoice_ser.data:
                #         total_amount += float(inv['grand_total'])

            
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "day":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_days = int(((interval.days*1440 + interval.seconds/60)/60)/24)

            # total_data = {}
            for day in range(0, total_days+1):
                current_time = start_time + timedelta(days=day)
                invoices = Invoice.objects.filter(date_created__date=current_time.date())\
                                            .filter(status="Pending")\
                                            .order_by("date_created")

                invoice_ser = InvoiceSerializer(invoices, many=True)

                # total_amount = 0
                # for inv in invoice_ser.data:
                #         total_amount += float(inv['grand_total'])

                context[current_time.strftime('%Y-%m-%d')] = invoice_ser.data
                
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "week":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_weeks = int((((interval.days*1440 + interval.seconds/60)/60)/24)/7)

            if total_weeks > 0:
                for week in range(0, total_weeks+1):
                    start_time += timedelta(weeks=week)
                    current_week = start_time + timedelta(weeks=week+1)

                    if current_week > end_time:
                        current_week = end_time

                    invoices = Invoice.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)\
                                                .filter(status="Pending")\
                                                .order_by("date_created")
                    invoice_ser = InvoiceSerializer(invoices, many=True)
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    context[key] = invoice_ser.data                        
                
                return Response(context, status=status.HTTP_200_OK)

            else:
                invoices = Invoice.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(status="Pending")\
                            .order_by("date_created")

                if len(invoices) > 0:
                    invoice_ser = InvoiceSerializer(invoices, many=True)
                    key = f"{start_date} - {end_date}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    # context[key] = total_amount
                    context[key] = invoice_ser.data

                    return Response(context, status=status.HTTP_200_OK)

                else:
                    context["message"] = "No emailed invoices within this date range"
                    return Response(context, status=status.HTTP_404_NOT_FOUND)
            
            # return Response(context, status=status.HTTP_200_OK)
        
        elif how == "months":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_months = int(((((interval.days*1440 + interval.seconds/60)/60)/24)/7)/4)

            if total_months > 0:
                for week in range(0, total_months+1):
                    start_time += timedelta(weeks=week*4)
                    current_week = start_time + timedelta(weeks=(week+1)*4)

                    if current_week > end_time:
                        current_week = end_time

                    invoices = Invoice.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)\
                                                .filter(status="Pending")\
                                                .order_by("date_created")

                    invoice_ser = InvoiceSerializer(invoices, many=True)
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"
                    # key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    # context[key] = total_amount
                    context[key] = invoice_ser.data
                return Response(context, status=status.HTTP_200_OK)

            else:
                invoices = Invoice.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(status="Pending")\
                            .order_by("date_created")

                if len(invoices) > 0:
                    invoice_ser = InvoiceSerializer(invoices, many=True)
                    key = f"{start_date} - {end_date}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    # context[key] = total_amount
                    context[key] = invoice_ser.data

                    return Response(context, status=status.HTTP_200_OK)

                else:
                    context["message"] = "No emailed invoices within this date range"
                    return Response(context, status=status.HTTP_404_NOT_FOUND)
            
            # return Response(context, status=status.HTTP_200_OK)
        

        elif how == "custom date":
            invoices = Invoice.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(status="Pending")\
                            .order_by("date_created")

            if len(invoices) > 0:
                invoice_ser = InvoiceSerializer(invoices, many=True)
                key = f"{start_date} - {end_date}"

                # total_amount = 0
                # for inv in invoice_ser.data:
                #         total_amount += float(inv['grand_total'])

                # context[key] = total_amount
                context[key] = invoice_ser.data

                return Response(context, status=status.HTTP_200_OK)

            else:
                context["message"] = "No invoices were created within this date range"
                return Response(context, status=status.HTTP_404_NOT_FOUND)


    # 2.10
    elif measure == "detail inovice paid":
        context = {}
        how = request.query_params.get("how")

        if how == "hour":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_hours = int((interval.days*1440 + interval.seconds/60)/60)

            # total_data = {}
            for hour in range(0, total_hours+1):
                current_time = start_time + timedelta(hours=hour)
                invoices = Invoice.objects.filter(date_created__date=current_time.date())\
                                          .filter(date_created__hour=current_time.hour)\
                                          .filter(status="Paid")\
                                            .order_by("date_created")
                invoice_ser = InvoiceSerializer(invoices, many=True)

                # context['message'] = invoice_ser.data
                context[current_time.strftime('%Y-%m-%d %I%p')] = invoice_ser.data

                # # for inv in invoice_ser.data:
                # total_amount = 0
                # for inv in invoice_ser.data:
                #         total_amount += float(inv['grand_total'])

            
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "day":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_days = int(((interval.days*1440 + interval.seconds/60)/60)/24)

            # total_data = {}
            for day in range(0, total_days+1):
                current_time = start_time + timedelta(days=day)
                invoices = Invoice.objects.filter(date_created__date=current_time.date())\
                                            .filter(status="Paid")\
                                            .order_by("date_created")

                invoice_ser = InvoiceSerializer(invoices, many=True)

                # total_amount = 0
                # for inv in invoice_ser.data:
                #         total_amount += float(inv['grand_total'])

                context[current_time.strftime('%Y-%m-%d')] = invoice_ser.data
                
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "week":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_weeks = int((((interval.days*1440 + interval.seconds/60)/60)/24)/7)

            if total_weeks > 0:
                for week in range(0, total_weeks+1):
                    start_time += timedelta(weeks=week)
                    current_week = start_time + timedelta(weeks=week+1)

                    if current_week > end_time:
                        current_week = end_time

                    invoices = Invoice.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)\
                                                .filter(status="Paid")\
                                                .order_by("date_created")
                    invoice_ser = InvoiceSerializer(invoices, many=True)
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    context[key] = invoice_ser.data                        
                
                return Response(context, status=status.HTTP_200_OK)

            else:
                invoices = Invoice.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(status="Paid")\
                            .order_by("date_created")

                if len(invoices) > 0:
                    invoice_ser = InvoiceSerializer(invoices, many=True)
                    key = f"{start_date} - {end_date}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    # context[key] = total_amount
                    context[key] = invoice_ser.data

                    return Response(context, status=status.HTTP_200_OK)

                else:
                    context["message"] = "No emailed invoices within this date range"
                    return Response(context, status=status.HTTP_404_NOT_FOUND)
            
            # return Response(context, status=status.HTTP_200_OK)
        
        elif how == "months":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_months = int(((((interval.days*1440 + interval.seconds/60)/60)/24)/7)/4)

            if total_months > 0:
                for week in range(0, total_months+1):
                    start_time += timedelta(weeks=week*4)
                    current_week = start_time + timedelta(weeks=(week+1)*4)

                    if current_week > end_time:
                        current_week = end_time

                    invoices = Invoice.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)\
                                                .filter(status="Paid")\
                                                .order_by("date_created")

                    invoice_ser = InvoiceSerializer(invoices, many=True)
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"
                    # key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    # context[key] = total_amount
                    context[key] = invoice_ser.data
                return Response(context, status=status.HTTP_200_OK)

            else:
                invoices = Invoice.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(status="Paid")\
                            .order_by("date_created")

                if len(invoices) > 0:
                    invoice_ser = InvoiceSerializer(invoices, many=True)
                    key = f"{start_date} - {end_date}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    # context[key] = total_amount
                    context[key] = invoice_ser.data

                    return Response(context, status=status.HTTP_200_OK)

                else:
                    context["message"] = "No emailed invoices within this date range"
                    return Response(context, status=status.HTTP_404_NOT_FOUND)
            
            # return Response(context, status=status.HTTP_200_OK)
        

        elif how == "custom date":
            invoices = Invoice.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(status="Paid")\
                            .order_by("date_created")

            if len(invoices) > 0:
                invoice_ser = InvoiceSerializer(invoices, many=True)
                key = f"{start_date} - {end_date}"

                # total_amount = 0
                # for inv in invoice_ser.data:
                #         total_amount += float(inv['grand_total'])

                # context[key] = total_amount
                context[key] = invoice_ser.data

                return Response(context, status=status.HTTP_200_OK)

            else:
                context["message"] = "No invoices were created within this date range"
                return Response(context, status=status.HTTP_404_NOT_FOUND)
    

    # 2.11
    elif measure == "detail invoice unpaid":
        context = {}
        how = request.query_params.get("how")

        if how == "hour":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_hours = int((interval.days*1440 + interval.seconds/60)/60)

            # total_data = {}
            for hour in range(0, total_hours+1):
                current_time = start_time + timedelta(hours=hour)
                invoices = Invoice.objects.filter(date_created__date=current_time.date())\
                                          .filter(date_created__hour=current_time.hour)\
                                          .filter(status="Unpaid")\
                                            .order_by("date_created")
                invoice_ser = InvoiceSerializer(invoices, many=True)

                # context['message'] = invoice_ser.data
                context[current_time.strftime('%Y-%m-%d %I%p')] = invoice_ser.data

                # # for inv in invoice_ser.data:
                # total_amount = 0
                # for inv in invoice_ser.data:
                #         total_amount += float(inv['grand_total'])

            
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "day":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_days = int(((interval.days*1440 + interval.seconds/60)/60)/24)

            # total_data = {}
            for day in range(0, total_days+1):
                current_time = start_time + timedelta(days=day)
                invoices = Invoice.objects.filter(date_created__date=current_time.date())\
                                            .filter(status="Unpaid")\
                                            .order_by("date_created")

                invoice_ser = InvoiceSerializer(invoices, many=True)

                # total_amount = 0
                # for inv in invoice_ser.data:
                #         total_amount += float(inv['grand_total'])

                context[current_time.strftime('%Y-%m-%d')] = invoice_ser.data
                
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "week":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_weeks = int((((interval.days*1440 + interval.seconds/60)/60)/24)/7)

            if total_weeks > 0:
                for week in range(0, total_weeks+1):
                    start_time += timedelta(weeks=week)
                    current_week = start_time + timedelta(weeks=week+1)

                    if current_week > end_time:
                        current_week = end_time

                    invoices = Invoice.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)\
                                                .filter(status="Unpaid")\
                                                .order_by("date_created")
                    invoice_ser = InvoiceSerializer(invoices, many=True)
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    context[key] = invoice_ser.data                        
                
                return Response(context, status=status.HTTP_200_OK)

            else:
                invoices = Invoice.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(status="Unpaid")\
                            .order_by("date_created")

                if len(invoices) > 0:
                    invoice_ser = InvoiceSerializer(invoices, many=True)
                    key = f"{start_date} - {end_date}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    # context[key] = total_amount
                    context[key] = invoice_ser.data

                    return Response(context, status=status.HTTP_200_OK)

                else:
                    context["message"] = "No emailed invoices within this date range"
                    return Response(context, status=status.HTTP_404_NOT_FOUND)
            
            # return Response(context, status=status.HTTP_200_OK)
        
        elif how == "months":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_months = int(((((interval.days*1440 + interval.seconds/60)/60)/24)/7)/4)

            if total_months > 0:
                for week in range(0, total_months+1):
                    start_time += timedelta(weeks=week*4)
                    current_week = start_time + timedelta(weeks=(week+1)*4)

                    if current_week > end_time:
                        current_week = end_time

                    invoices = Invoice.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)\
                                                .filter(status="Unpaid")\
                                                .order_by("date_created")

                    invoice_ser = InvoiceSerializer(invoices, many=True)
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"
                    # key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    # context[key] = total_amount
                    context[key] = invoice_ser.data
                return Response(context, status=status.HTTP_200_OK)

            else:
                invoices = Invoice.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(status="Unpaid")\
                            .order_by("date_created")

                if len(invoices) > 0:
                    invoice_ser = InvoiceSerializer(invoices, many=True)
                    key = f"{start_date} - {end_date}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    # context[key] = total_amount
                    context[key] = invoice_ser.data

                    return Response(context, status=status.HTTP_200_OK)

                else:
                    context["message"] = "No emailed invoices within this date range"
                    return Response(context, status=status.HTTP_404_NOT_FOUND)
            
            # return Response(context, status=status.HTTP_200_OK)
        

        elif how == "custom date":
            invoices = Invoice.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(status="Unpaid")\
                            .order_by("date_created")

            if len(invoices) > 0:
                invoice_ser = InvoiceSerializer(invoices, many=True)
                key = f"{start_date} - {end_date}"

                # total_amount = 0
                # for inv in invoice_ser.data:
                #         total_amount += float(inv['grand_total'])

                # context[key] = total_amount
                context[key] = invoice_ser.data

                return Response(context, status=status.HTTP_200_OK)

            else:
                context["message"] = "No invoices were created within this date range"
                return Response(context, status=status.HTTP_404_NOT_FOUND)


    # 2.12
    elif measure == "detail sales tax":
        context = {}
        how = request.query_params.get("how")

        if how == "hour":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_hours = int((interval.days*1440 + interval.seconds/60)/60)

            # total_data = {}
            for hour in range(0, total_hours+1):
                current_time = start_time + timedelta(hours=hour)
                invoices = Invoice.objects.filter(date_created__date=current_time.date())\
                                          .filter(date_created__hour=current_time.hour)
                invoice_ser = InvoiceSerializer(invoices, many=True)

                # for inv in invoice_ser.data:
                total_amount = 0
                for inv in invoice_ser.data:
                        total_amount += float(inv['grand_total'])

                context[current_time.strftime('%Y-%m-%d %I%p')] = total_amount
            
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "day":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_days = int(((interval.days*1440 + interval.seconds/60)/60)/24)

            # total_data = {}
            for day in range(0, total_days+1):
                current_time = start_time + timedelta(days=day)
                invoices = Invoice.objects.filter(date_created__date=current_time.date())

                invoice_ser = InvoiceSerializer(invoices, many=True)

                total_amount = 0
                for inv in invoice_ser.data:
                        total_amount += float(inv['grand_total'])

                context[current_time.strftime('%Y-%m-%d')] = total_amount
                
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "week":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_weeks = int((((interval.days*1440 + interval.seconds/60)/60)/24)/7)

            if total_weeks > 0:
                for week in range(0, total_weeks+1):
                    start_time += timedelta(weeks=week)
                    current_week = start_time + timedelta(weeks=week+1)

                    if current_week > end_time:
                        current_week = end_time

                    invoices = Invoice.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)
                    invoice_ser = InvoiceSerializer(invoices, many=True)
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"

                    total_amount = 0
                    for inv in invoice_ser.data:
                            total_amount += float(inv['grand_total'])

                    context[key] = total_amount
                        
                    # context[key] = invoice_ser.data
                
                return Response(context, status=status.HTTP_200_OK)

            else:
                invoices = Invoice.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date).all().order_by("date_created")

                if len(invoices) > 0:
                    invoice_ser = InvoiceSerializer(invoices, many=True)
                    key = f"{start_date} - {end_date}"

                    total_amount = 0
                    for inv in invoice_ser.data:
                            total_amount += float(inv['grand_total'])

                    context[key] = total_amount
                    # context['message'] = invoice_ser.data

                    return Response(context, status=status.HTTP_200_OK)

                else:
                    context["message"] = "No invoices were created within this date range"
                    return Response(context, status=status.HTTP_404_NOT_FOUND)
            
            # return Response(context, status=status.HTTP_200_OK)
        
        elif how == "months":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_months = int(((((interval.days*1440 + interval.seconds/60)/60)/24)/7)/4)

            if total_months > 0:
                for week in range(0, total_months+1):
                    start_time += timedelta(weeks=week*4)
                    current_week = start_time + timedelta(weeks=(week+1)*4)

                    if current_week > end_time:
                        current_week = end_time

                    invoices = Invoice.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)
                    invoice_ser = InvoiceSerializer(invoices, many=True)
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"
                    # key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"

                    total_amount = 0
                    for inv in invoice_ser.data:
                            total_amount += float(inv['grand_total'])

                    context[key] = total_amount
                    # context[key] = invoice_ser.data
                return Response(context, status=status.HTTP_200_OK)

            else:
                invoices = Invoice.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date).all().order_by("date_created")

                if len(invoices) > 0:
                    invoice_ser = InvoiceSerializer(invoices, many=True)
                    key = f"{start_date} - {end_date}"

                    total_amount = 0
                    for inv in invoice_ser.data:
                            total_amount += float(inv['grand_total'])

                    context[key] = total_amount
                    # context['message'] = invoice_ser.data

                    return Response(context, status=status.HTTP_200_OK)

                else:
                    context["message"] = "No invoices were created within this date range"
                    return Response(context, status=status.HTTP_404_NOT_FOUND)
            
            # return Response(context, status=status.HTTP_200_OK)
        

        elif how == "custom date":
            invoices = Invoice.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date).all().order_by("date_created")

            if len(invoices) > 0:
                invoice_ser = InvoiceSerializer(invoices, many=True)
                key = f"{start_date} - {end_date}"

                total_amount = 0
                for inv in invoice_ser.data:
                        total_amount += float(inv['grand_total'])

                context[key] = total_amount
                # context['message'] = invoice_ser.data

                return Response(context, status=status.HTTP_200_OK)

            else:
                context["message"] = "No invoices were created within this date range"
                return Response(context, status=status.HTTP_404_NOT_FOUND)


    
    # 2.13
    elif measure == "different sales tax":
        context = {}
        how = request.query_params.get("how")

        if how == "hour":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_hours = int((interval.days*1440 + interval.seconds/60)/60)

            # total_data = {}
            for hour in range(0, total_hours+1):
                current_time = start_time + timedelta(hours=hour)
                invoices_percent = Invoice.objects.filter(date_created__date=current_time.date())\
                                          .filter(date_created__hour=current_time.hour)\
                                          .filter(discount_type="percent")\
                                            .order_by("date_created")
                
                invoices_value = Invoice.objects.filter(date_created__date=current_time.date())\
                                          .filter(date_created__hour=current_time.hour)\
                                          .filter(discount_type="value")\
                                            .order_by("date_created")

                invoice_pser = InvoiceSerializer(invoices_percent, many=True)
                invoice_vser = InvoiceSerializer(invoices_value, many=True)

                # context['message'] = invoice_ser.data
                context[current_time.strftime('%Y-%m-%d %I%p')]['percent'] = invoice_pser.data
                context[current_time.strftime('%Y-%m-%d %I%p')]['value'] = invoice_vser.data

                # # for inv in invoice_ser.data:
                # total_amount = 0
                # for inv in invoice_ser.data:
                #         total_amount += float(inv['grand_total'])

            
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "day":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_days = int(((interval.days*1440 + interval.seconds/60)/60)/24)

            # total_data = {}
            for day in range(0, total_days+1):
                current_time = start_time + timedelta(days=day)
                invoices_percent = Invoice.objects.filter(date_created__date=current_time.date())\
                                            .filter(discount_type="percent")\
                                            .order_by("date_created")

                invoices_value = Invoice.objects.filter(date_created__date=current_time.date())\
                                            .filter(discount_type="value")\
                                            .order_by("date_created")

                invoice_pser = InvoiceSerializer(invoices_percent, many=True)
                invoice_vser = InvoiceSerializer(invoices_value, many=True)

                # total_amount = 0
                # for inv in invoice_ser.data:
                #         total_amount += float(inv['grand_total'])

                context[current_time.strftime('%Y-%m-%d')]['percent'] = invoice_pser.data
                context[current_time.strftime('%Y-%m-%d')]['value'] = invoice_vser.data
                
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "week":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_weeks = int((((interval.days*1440 + interval.seconds/60)/60)/24)/7)

            if total_weeks > 0:
                for week in range(0, total_weeks+1):
                    start_time += timedelta(weeks=week)
                    current_week = start_time + timedelta(weeks=week+1)

                    if current_week > end_time:
                        current_week = end_time

                    invoices_percent = Invoice.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)\
                                                .filter(discount_type="percent")\
                                                .order_by("date_created")

                    invoices_value = Invoice.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)\
                                                .filter(discount_type="value")\
                                                .order_by("date_created")

                    invoice_pser = InvoiceSerializer(invoices_percent, many=True)
                    invoice_vser = InvoiceSerializer(invoices_value, many=True)

                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"


                    context[key]['percent'] = invoice_pser.data                     
                    context[key]['value'] = invoice_vser.data
                
                return Response(context, status=status.HTTP_200_OK)

            else:
                invoices_percent = Invoice.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(discount_type="percent")\
                            .order_by("date_created")

                invoices_value = Invoice.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(discount_type="value")\
                            .order_by("date_created")

                # if len(invoices_percent) > 0:
                invoice_pser = InvoiceSerializer(invoices_percent, many=True)
                invoice_vser = InvoiceSerializer(invoices_value, many=True)
                key = f"{start_date} - {end_date}"

                context[key]['percent'] = invoice_pser.data
                context[key]['value'] = invoice_vser.data

                return Response(context, status=status.HTTP_200_OK)


                # else:
                #     context["message"] = "No emailed invoices within this date range"
                #     return Response(context, status=status.HTTP_404_NOT_FOUND)
            
            # return Response(context, status=status.HTTP_200_OK)
        
        elif how == "months":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_months = int(((((interval.days*1440 + interval.seconds/60)/60)/24)/7)/4)

            if total_months > 0:
                for week in range(0, total_months+1):
                    start_time += timedelta(weeks=week*4)
                    current_week = start_time + timedelta(weeks=(week+1)*4)

                    if current_week > end_time:
                        current_week = end_time

                    invoices_percent = Invoice.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)\
                                                .filter(discount_type="percent")\
                                                .order_by("date_created")
                    
                    invoices_value = Invoice.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)\
                                                .filter(discount_type="value")\
                                                .order_by("date_created")

                    invoice_pser = InvoiceSerializer(invoices_percent, many=True)
                    invoice_vser = InvoiceSerializer(invoices_value, many=True)
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"
                    # key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    # context[key] = total_amount
                    context[key]['percent'] = invoice_pser.data
                    context[key]['value'] = invoice_vser.data
                return Response(context, status=status.HTTP_200_OK)

            else:
                invoices_percent = Invoice.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(discount_type="percent")\
                            .order_by("date_created")

                invoices_value = Invoice.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(discount_type="value")\
                            .order_by("date_created")

                # if len(invoices) > 0:
                invoice_pser = InvoiceSerializer(invoices_percent, many=True)
                invoice_vser = InvoiceSerializer(invoices_value, many=True)
                key = f"{start_date} - {end_date}"

                # total_amount = 0
                # for inv in invoice_ser.data:
                #         total_amount += float(inv['grand_total'])

                # context[key] = total_amount
                context[key]['percent'] = invoice_pser.data
                context[key]['value'] = invoice_vser.data

                return Response(context, status=status.HTTP_200_OK)

                # else:
                #     context["message"] = "No emailed invoices within this date range"
                #     return Response(context, status=status.HTTP_404_NOT_FOUND)
            
            # return Response(context, status=status.HTTP_200_OK)
        

        elif how == "custom date":
            invoices_percent = Invoice.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(discount_type="percent")\
                            .order_by("date_created")

            invoices_value = Invoice.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(discount_type="value")\
                            .order_by("date_created")

            # if len(invoices) > 0:
            invoice_pser = InvoiceSerializer(invoices_percent, many=True)
            invoice_vser = InvoiceSerializer(invoices_percent, many=True)
            key = f"{start_date} - {end_date}"

            # total_amount = 0
            # for inv in invoice_ser.data:
            #         total_amount += float(inv['grand_total'])

            # context[key] = total_amount
            context[key]['percent'] = invoice_pser.data
            context[key]['value'] = invoice_vser.data

            return Response(context, status=status.HTTP_200_OK)

            # else:
            #     context["message"] = "No invoices were created within this date range"
            #     return Response(context, status=status.HTTP_404_NOT_FOUND)


    # 2.14
    elif measure == "detail recurring invoice":
        context = {}
        how = request.query_params.get("how")

        if how == "hour":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_hours = int((interval.days*1440 + interval.seconds/60)/60)

            # total_data = {}
            for hour in range(0, total_hours+1):
                current_time = start_time + timedelta(hours=hour)
                invoices = Invoice.objects.filter(date_created__date=current_time.date())\
                                          .filter(date_created__hour=current_time.hour)\
                                          .filter(recurring=True)
                invoice_ser = InvoiceSerializer(invoices, many=True)

                # context['message'] = invoice_ser.data
                context[current_time.strftime('%Y-%m-%d %I%p')] = invoice_ser.data

                # # for inv in invoice_ser.data:
                # total_amount = 0
                # for inv in invoice_ser.data:
                #         total_amount += float(inv['grand_total'])

            
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "day":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_days = int(((interval.days*1440 + interval.seconds/60)/60)/24)

            # total_data = {}
            for day in range(0, total_days+1):
                current_time = start_time + timedelta(days=day)
                invoices = Invoice.objects.filter(date_created__date=current_time.date())\
                                            .filter(recurring=True)

                invoice_ser = InvoiceSerializer(invoices, many=True)

                # total_amount = 0
                # for inv in invoice_ser.data:
                #         total_amount += float(inv['grand_total'])

                context[current_time.strftime('%Y-%m-%d')] = invoice_ser.data
                
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "week":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_weeks = int((((interval.days*1440 + interval.seconds/60)/60)/24)/7)

            if total_weeks > 0:
                for week in range(0, total_weeks+1):
                    start_time += timedelta(weeks=week)
                    current_week = start_time + timedelta(weeks=week+1)

                    if current_week > end_time:
                        current_week = end_time

                    invoices = Invoice.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)\
                                                .filter(recurring=True)
                    invoice_ser = InvoiceSerializer(invoices, many=True)
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    context[key] = invoice_ser.data                        
                
                return Response(context, status=status.HTTP_200_OK)

            else:
                invoices = Invoice.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(recurring=True)\
                            .order_by("date_created")

                if len(invoices) > 0:
                    invoice_ser = InvoiceSerializer(invoices, many=True)
                    key = f"{start_date} - {end_date}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    # context[key] = total_amount
                    context[key] = invoice_ser.data

                    return Response(context, status=status.HTTP_200_OK)

                else:
                    context["message"] = "No emailed invoices within this date range"
                    return Response(context, status=status.HTTP_404_NOT_FOUND)
            
            # return Response(context, status=status.HTTP_200_OK)
        
        elif how == "months":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_months = int(((((interval.days*1440 + interval.seconds/60)/60)/24)/7)/4)

            if total_months > 0:
                for week in range(0, total_months+1):
                    start_time += timedelta(weeks=week*4)
                    current_week = start_time + timedelta(weeks=(week+1)*4)

                    if current_week > end_time:
                        current_week = end_time

                    invoices = Invoice.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)\
                                                .filter(recurring=True)\
                                                .order_by("date_created")

                    invoice_ser = InvoiceSerializer(invoices, many=True)
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"
                    # key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    # context[key] = total_amount
                    context[key] = invoice_ser.data
                return Response(context, status=status.HTTP_200_OK)

            else:
                invoices = Invoice.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(recurring=True)\
                            .order_by("date_created")

                if len(invoices) > 0:
                    invoice_ser = InvoiceSerializer(invoices, many=True)
                    key = f"{start_date} - {end_date}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    # context[key] = total_amount
                    context[key] = invoice_ser.data

                    return Response(context, status=status.HTTP_200_OK)

                else:
                    context["message"] = "No emailed invoices within this date range"
                    return Response(context, status=status.HTTP_404_NOT_FOUND)
            
            # return Response(context, status=status.HTTP_200_OK)
        

        elif how == "custom date":
            invoices = Invoice.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(recurring=True)\
                            .order_by("date_created")

            if len(invoices) > 0:
                invoice_ser = InvoiceSerializer(invoices, many=True)
                key = f"{start_date} - {end_date}"

                # total_amount = 0
                # for inv in invoice_ser.data:
                #         total_amount += float(inv['grand_total'])

                # context[key] = total_amount
                context[key] = invoice_ser.data

                return Response(context, status=status.HTTP_200_OK)

            else:
                context["message"] = "No invoices were created within this date range"
                return Response(context, status=status.HTTP_404_NOT_FOUND)















            
   


@api_view(["GET"])
@authentication_classes((MyAuthentication, ))
@permission_classes((IsAuthenticated, ))
def proforma_report(request):
    context = {}
    measure = request.query_params.get("measure", None)
    start_date = request.query_params.get("start", None)
    end_date = request.query_params.get("end", None)

    # 3.1
    if measure == "proforma search":
        invoices = ProformaInvoice.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date).all().order_by("date_created")
        if len(invoices) > 0:
            invoice_ser = ProformerInvoiceSerailizer(invoices, many=True)
            context['message'] = invoice_ser.data

            return Response(context, status=status.HTTP_200_OK)

        else:
            context["message"] = "No proforma invoice was created within this date range"
            return Response(context, status=status.HTTP_404_NOT_FOUND)
    
    # 3.2
    elif measure == "amount search":
        invoices = ProformaInvoice.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date).all().order_by("date_created")

        if len(invoices) > 0:
            invoice_ser = ProformerInvoiceSerailizer(invoices, many=True)
            context['message'] = invoice_ser.data

            return Response(context, status=status.HTTP_200_OK)

        else:
            context["message"] = "No proforma invoice was created within this date range"
            return Response(context, status=status.HTTP_404_NOT_FOUND)
    

    # 3.3
    elif measure == "per customer":
        invoices = ProformaInvoice.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date).all().order_by("date_created")

        if len(invoices) > 0:
            invoice_ser = ProformerInvoiceSerailizer(invoices, many=True)
            total_data = {}
            for inv in invoice_ser.data:
                full_name = inv['customer']['first_name'] + " " + inv['customer']['last_name']
                if full_name in total_data:
                    total_data[full_name] += float(inv['grand_total'])
                else:
                    total_data[full_name] = 0
            
            final_data = []
            for k,v in total_data.items():
                final_data.append({"full_name": k, "total_amount": v})

            context['message'] = final_data


            return Response(context, status=status.HTTP_200_OK)

        else:
            context["message"] = "No proforma invoice was created within this date range"
            return Response(context, status=status.HTTP_404_NOT_FOUND)
    
    # 3.4
    elif measure == "total per date":
        context = {}
        how = request.query_params.get("how")

        if how == "hour":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_hours = int((interval.days*1440 + interval.seconds/60)/60)

            # total_data = {}
            for hour in range(0, total_hours+1):
                current_time = start_time + timedelta(hours=hour)
                invoices = ProformaInvoice.objects.filter(date_created__date=current_time.date())\
                                          .filter(date_created__hour=current_time.hour)
                invoice_ser = ProformerInvoiceSerailizer(invoices, many=True)

                # for inv in invoice_ser.data:
                total_amount = 0
                for inv in invoice_ser.data:
                        total_amount += float(inv['grand_total'])

                context[current_time.strftime('%Y-%m-%d %I%p')] = total_amount
            
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "day":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_days = int(((interval.days*1440 + interval.seconds/60)/60)/24)

            # total_data = {}
            for day in range(0, total_days+1):
                current_time = start_time + timedelta(days=day)
                invoices = ProformaInvoice.objects.filter(date_created__date=current_time.date())

                invoice_ser = ProformerInvoiceSerailizer(invoices, many=True)

                total_amount = 0
                for inv in invoice_ser.data:
                        total_amount += float(inv['grand_total'])

                context[current_time.strftime('%Y-%m-%d')] = total_amount
                
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "week":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_weeks = int((((interval.days*1440 + interval.seconds/60)/60)/24)/7)

            if total_weeks > 0:
                for week in range(0, total_weeks+1):
                    start_time += timedelta(weeks=week)
                    current_week = start_time + timedelta(weeks=week+1)

                    if current_week > end_time:
                        current_week = end_time

                    invoices = ProformaInvoice.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)
                    invoice_ser = ProformerInvoiceSerailizer(invoices, many=True)
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"

                    total_amount = 0
                    for inv in invoice_ser.data:
                            total_amount += float(inv['grand_total'])

                    context[key] = total_amount
                        
                    # context[key] = invoice_ser.data
                
                return Response(context, status=status.HTTP_200_OK)

            else:
                invoices = ProformaInvoice.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date).all().order_by("date_created")

                if len(invoices) > 0:
                    invoice_ser = ProformerInvoiceSerailizer(invoices, many=True)
                    key = f"{start_date} - {end_date}"

                    total_amount = 0
                    for inv in invoice_ser.data:
                            total_amount += float(inv['grand_total'])

                    context[key] = total_amount
                    # context['message'] = invoice_ser.data

                    return Response(context, status=status.HTTP_200_OK)

                else:
                    context["message"] = "No proforma invoice was created within this date range"
                    return Response(context, status=status.HTTP_404_NOT_FOUND)
            
            # return Response(context, status=status.HTTP_200_OK)
        
        elif how == "months":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_months = int(((((interval.days*1440 + interval.seconds/60)/60)/24)/7)/4)

            if total_months > 0:
                for week in range(0, total_months+1):
                    start_time += timedelta(weeks=week*4)
                    current_week = start_time + timedelta(weeks=(week+1)*4)

                    if current_week > end_time:
                        current_week = end_time

                    invoices = ProformaInvoice.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)
                    invoice_ser = ProformerInvoiceSerailizer(invoices, many=True)
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"
                    # key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"

                    total_amount = 0
                    for inv in invoice_ser.data:
                            total_amount += float(inv['grand_total'])

                    context[key] = total_amount
                    # context[key] = invoice_ser.data
                return Response(context, status=status.HTTP_200_OK)

            else:
                invoices = ProformaInvoice.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date).all().order_by("date_created")

                if len(invoices) > 0:
                    invoice_ser = ProformerInvoiceSerailizer(invoices, many=True)
                    key = f"{start_date} - {end_date}"

                    total_amount = 0
                    for inv in invoice_ser.data:
                            total_amount += float(inv['grand_total'])

                    context[key] = total_amount
                    # context['message'] = invoice_ser.data

                    return Response(context, status=status.HTTP_200_OK)

                else:
                    context["message"] = "No proforma invoice was created within this date range"
                    return Response(context, status=status.HTTP_404_NOT_FOUND)
            
            # return Response(context, status=status.HTTP_200_OK)
        

        elif how == "custom date":
            invoices = ProformaInvoice.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date).all().order_by("date_created")

            if len(invoices) > 0:
                invoice_ser = ProformerInvoiceSerailizer(invoices, many=True)
                key = f"{start_date} - {end_date}"

                total_amount = 0
                for inv in invoice_ser.data:
                        total_amount += float(inv['grand_total'])

                context[key] = total_amount
                # context['message'] = invoice_ser.data

                return Response(context, status=status.HTTP_200_OK)

            else:
                context["message"] = "No invoices were created within this date range"
                return Response(context, status=status.HTTP_404_NOT_FOUND)


    
    # 3.5
    elif measure == "count proforma email":
        context = {}
        how = request.query_params.get("how")

        if how == "hour":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_hours = int((interval.days*1440 + interval.seconds/60)/60)

            
            for hour in range(0, total_hours+1):
                current_time = start_time + timedelta(hours=hour)
                emailed_count = ProformaInvoice.objects.filter(date_created__date=current_time.date())\
                                          .filter(date_created__hour=current_time.hour)\
                                            .filter(emailed=True).count()
                
                context[current_time.strftime('%Y-%m-%d %I%p')] = emailed_count
                

            
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "day":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_days = int(((interval.days*1440 + interval.seconds/60)/60)/24)

            
            for day in range(0, total_days+1):
                current_time = start_time + timedelta(days=day)
                
                emailed_count = ProformaInvoice.objects.filter(date_created__date=current_time.date())\
                                            .filter(emailed=True).count()
                
                context[current_time.strftime('%Y-%m-%d')] = emailed_count

                

                
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "week":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_weeks = int((((interval.days*1440 + interval.seconds/60)/60)/24)/7)

            if total_weeks > 0:
                for week in range(0, total_weeks+1):
                    start_time += timedelta(weeks=week)
                    current_week = start_time + timedelta(weeks=week+1)

                    if current_week > end_time:
                        current_week = end_time

                    emailed_count = ProformaInvoice.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)\
                                                .filter(emailed=True).count()
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"
                    context[key] = emailed_count
                            
                    
                
                return Response(context, status=status.HTTP_200_OK)

            else:
                emailed_count = ProformaInvoice.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(emailed=True)\
                            .count()

                key = f"{start_date} - {end_date}"
                context[key] = emailed_count
                return Response(context, status=status.HTTP_200_OK)
                
        
        elif how == "months":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_months = int(((((interval.days*1440 + interval.seconds/60)/60)/24)/7)/4)

            if total_months > 0:
                for week in range(0, total_months+1):
                    start_time += timedelta(weeks=week*4)
                    current_week = start_time + timedelta(weeks=(week+1)*4)

                    if current_week > end_time:
                        current_week = end_time

                    emailed_count = ProformaInvoice.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)\
                                                .filter(emailed=True).count()
                    
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"
                    context[key] = emailed_count
                    
                return Response(context, status=status.HTTP_200_OK)

            else:
                emailed_count = ProformaInvoice.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(emailed=True).count()

                key = f"{start_date} - {end_date}"
                context[key] = emailed_count
                return Response(context, status=status.HTTP_200_OK)
                
        

        elif how == "custom date":
            emailed_count = ProformaInvoice.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(emailed=True).count()
                
            key = f"{start_date} - {end_date}"
            context[key] = emailed_count
            return Response(context, status=status.HTTP_200_OK)
    

    # 3.6
    elif measure == "detail proforma email":
        context = {}
        how = request.query_params.get("how")

        if how == "hour":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_hours = int((interval.days*1440 + interval.seconds/60)/60)

            # total_data = {}
            for hour in range(0, total_hours+1):
                current_time = start_time + timedelta(hours=hour)
                invoices = ProformaInvoice.objects.filter(date_created__date=current_time.date())\
                                          .filter(date_created__hour=current_time.hour)\
                                          .filter(emailed=True)
                invoice_ser = ProformerInvoiceSerailizer(invoices, many=True)

                # context['message'] = invoice_ser.data
                context[current_time.strftime('%Y-%m-%d %I%p')] = invoice_ser.data

                # # for inv in invoice_ser.data:
                # total_amount = 0
                # for inv in invoice_ser.data:
                #         total_amount += float(inv['grand_total'])

            
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "day":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_days = int(((interval.days*1440 + interval.seconds/60)/60)/24)

            # total_data = {}
            for day in range(0, total_days+1):
                current_time = start_time + timedelta(days=day)
                invoices = ProformaInvoice.objects.filter(date_created__date=current_time.date())\
                                            .filter(emailed=True)

                invoice_ser = ProformerInvoiceSerailizer(invoices, many=True)

                # total_amount = 0
                # for inv in invoice_ser.data:
                #         total_amount += float(inv['grand_total'])

                context[current_time.strftime('%Y-%m-%d')] = invoice_ser.data
                
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "week":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_weeks = int((((interval.days*1440 + interval.seconds/60)/60)/24)/7)

            if total_weeks > 0:
                for week in range(0, total_weeks+1):
                    start_time += timedelta(weeks=week)
                    current_week = start_time + timedelta(weeks=week+1)

                    if current_week > end_time:
                        current_week = end_time

                    invoices = ProformaInvoice.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)\
                                                .filter(emailed=True)
                    invoice_ser = ProformerInvoiceSerailizer(invoices, many=True)
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    context[key] = invoice_ser.data                        
                
                return Response(context, status=status.HTTP_200_OK)

            else:
                invoices = ProformaInvoice.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(emailed=True)\
                            .order_by("date_created")

                if len(invoices) > 0:
                    invoice_ser = ProformerInvoiceSerailizer(invoices, many=True)
                    key = f"{start_date} - {end_date}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    # context[key] = total_amount
                    context[key] = invoice_ser.data

                    return Response(context, status=status.HTTP_200_OK)

                else:
                    context["message"] = "No emailed invoices within this date range"
                    return Response(context, status=status.HTTP_404_NOT_FOUND)
            
            # return Response(context, status=status.HTTP_200_OK)
        
        elif how == "months":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_months = int(((((interval.days*1440 + interval.seconds/60)/60)/24)/7)/4)

            if total_months > 0:
                for week in range(0, total_months+1):
                    start_time += timedelta(weeks=week*4)
                    current_week = start_time + timedelta(weeks=(week+1)*4)

                    if current_week > end_time:
                        current_week = end_time

                    invoices = ProformaInvoice.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)\
                                                .filter(emailed=True)\
                                                .order_by("date_created")

                    invoice_ser = ProformerInvoiceSerailizer(invoices, many=True)
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"
                    # key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    # context[key] = total_amount
                    context[key] = invoice_ser.data
                return Response(context, status=status.HTTP_200_OK)

            else:
                invoices = ProformaInvoice.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(emailed=True)\
                            .order_by("date_created")

                if len(invoices) > 0:
                    invoice_ser = ProformerInvoiceSerailizer(invoices, many=True)
                    key = f"{start_date} - {end_date}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    # context[key] = total_amount
                    context[key] = invoice_ser.data

                    return Response(context, status=status.HTTP_200_OK)

                else:
                    context["message"] = "No emailed invoices within this date range"
                    return Response(context, status=status.HTTP_404_NOT_FOUND)
            
            # return Response(context, status=status.HTTP_200_OK)
        

        elif how == "custom date":
            invoices = ProformaInvoice.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(emailed=True)\
                            .order_by("date_created")

            if len(invoices) > 0:
                invoice_ser = ProformerInvoiceSerailizer(invoices, many=True)
                key = f"{start_date} - {end_date}"

                # total_amount = 0
                # for inv in invoice_ser.data:
                #         total_amount += float(inv['grand_total'])

                # context[key] = total_amount
                context[key] = invoice_ser.data

                return Response(context, status=status.HTTP_200_OK)

            else:
                context["message"] = "No invoices were created within this date range"
                return Response(context, status=status.HTTP_404_NOT_FOUND)


    

    # 3.7
    elif measure == "count proforma overdue":

        context = {}
        how = request.query_params.get("how")

        if how == "hour":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_hours = int((interval.days*1440 + interval.seconds/60)/60)

            
            for hour in range(0, total_hours+1):
                current_time = start_time + timedelta(hours=hour)
                overdue_count = ProformaInvoice.objects.filter(date_created__date=current_time.date())\
                                          .filter(date_created__hour=current_time.hour)\
                                            .filter(status="Overdue").count()
                
                context[current_time.strftime('%Y-%m-%d %I%p')] = overdue_count
                

            
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "day":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_days = int(((interval.days*1440 + interval.seconds/60)/60)/24)

            
            for day in range(0, total_days+1):
                current_time = start_time + timedelta(days=day)
                
                overdue_count = ProformaInvoice.objects.filter(date_created__date=current_time.date())\
                                            .filter(status="Overdue").count()
                
                context[current_time.strftime('%Y-%m-%d')] = overdue_count

                

                
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "week":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_weeks = int((((interval.days*1440 + interval.seconds/60)/60)/24)/7)

            if total_weeks > 0:
                for week in range(0, total_weeks+1):
                    start_time += timedelta(weeks=week)
                    current_week = start_time + timedelta(weeks=week+1)

                    if current_week > end_time:
                        current_week = end_time

                    overdue_count = ProformaInvoice.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)\
                                                .filter(status="Overdue").count()
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"
                    context[key] = overdue_count
                            
                    
                
                return Response(context, status=status.HTTP_200_OK)

            else:
                overdue_count = ProformaInvoice.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(status="Overdue")\
                            .count()

                key = f"{start_date} - {end_date}"
                context[key] = overdue_count
                return Response(context, status=status.HTTP_200_OK)
                
        
        elif how == "months":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_months = int(((((interval.days*1440 + interval.seconds/60)/60)/24)/7)/4)

            if total_months > 0:
                for week in range(0, total_months+1):
                    start_time += timedelta(weeks=week*4)
                    current_week = start_time + timedelta(weeks=(week+1)*4)

                    if current_week > end_time:
                        current_week = end_time

                    overdue_count = ProformaInvoice.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)\
                                                .filter(status="Overdue").count()
                    
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"
                    context[key] = overdue_count
                    
                return Response(context, status=status.HTTP_200_OK)

            else:
                overdue_count = ProformaInvoice.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(status="Overdue").count()

                key = f"{start_date} - {end_date}"
                context[key] = overdue_count
                return Response(context, status=status.HTTP_200_OK)
                
        

        elif how == "custom date":
            overdue_count = ProformaInvoice.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(status="Overdue").count()
                
            key = f"{start_date} - {end_date}"
            context[key] = overdue_count
            return Response(context, status=status.HTTP_200_OK)


    # 3.8
    elif measure == "detail proforma overdue":
        context = {}
        how = request.query_params.get("how")

        if how == "hour":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_hours = int((interval.days*1440 + interval.seconds/60)/60)

            # total_data = {}
            for hour in range(0, total_hours+1):
                current_time = start_time + timedelta(hours=hour)
                invoices = ProformaInvoice.objects.filter(date_created__date=current_time.date())\
                                          .filter(date_created__hour=current_time.hour)\
                                          .filter(status="Overdue")\
                                            .order_by("date_created")
                invoice_ser = ProformerInvoiceSerailizer(invoices, many=True)

                # context['message'] = invoice_ser.data
                context[current_time.strftime('%Y-%m-%d %I%p')] = invoice_ser.data

                # # for inv in invoice_ser.data:
                # total_amount = 0
                # for inv in invoice_ser.data:
                #         total_amount += float(inv['grand_total'])

            
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "day":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_days = int(((interval.days*1440 + interval.seconds/60)/60)/24)

            # total_data = {}
            for day in range(0, total_days+1):
                current_time = start_time + timedelta(days=day)
                invoices = ProformaInvoice.objects.filter(date_created__date=current_time.date())\
                                            .filter(status="Overdue")\
                                            .order_by("date_created")

                invoice_ser = ProformerInvoiceSerailizer(invoices, many=True)

                # total_amount = 0
                # for inv in invoice_ser.data:
                #         total_amount += float(inv['grand_total'])

                context[current_time.strftime('%Y-%m-%d')] = invoice_ser.data
                
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "week":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_weeks = int((((interval.days*1440 + interval.seconds/60)/60)/24)/7)

            if total_weeks > 0:
                for week in range(0, total_weeks+1):
                    start_time += timedelta(weeks=week)
                    current_week = start_time + timedelta(weeks=week+1)

                    if current_week > end_time:
                        current_week = end_time

                    invoices = ProformaInvoice.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)\
                                                .filter(status="Overdue")\
                                                .order_by("date_created")
                    invoice_ser = ProformerInvoiceSerailizer(invoices, many=True)
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    context[key] = invoice_ser.data                        
                
                return Response(context, status=status.HTTP_200_OK)

            else:
                invoices = ProformaInvoice.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(status="Overdue")\
                            .order_by("date_created")

                if len(invoices) > 0:
                    invoice_ser = ProformerInvoiceSerailizer(invoices, many=True)
                    key = f"{start_date} - {end_date}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    # context[key] = total_amount
                    context[key] = invoice_ser.data

                    return Response(context, status=status.HTTP_200_OK)

                else:
                    context["message"] = "No emailed invoices within this date range"
                    return Response(context, status=status.HTTP_404_NOT_FOUND)
            
            # return Response(context, status=status.HTTP_200_OK)
        
        elif how == "months":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_months = int(((((interval.days*1440 + interval.seconds/60)/60)/24)/7)/4)

            if total_months > 0:
                for week in range(0, total_months+1):
                    start_time += timedelta(weeks=week*4)
                    current_week = start_time + timedelta(weeks=(week+1)*4)

                    if current_week > end_time:
                        current_week = end_time

                    invoices = ProformaInvoice.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)\
                                                .filter(status="Overdue")\
                                                .order_by("date_created")

                    invoice_ser = ProformerInvoiceSerailizer(invoices, many=True)
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"
                    # key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    # context[key] = total_amount
                    context[key] = invoice_ser.data
                return Response(context, status=status.HTTP_200_OK)

            else:
                invoices = ProformaInvoice.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(status="Overdue")\
                            .order_by("date_created")

                if len(invoices) > 0:
                    invoice_ser = ProformerInvoiceSerailizer(invoices, many=True)
                    key = f"{start_date} - {end_date}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    # context[key] = total_amount
                    context[key] = invoice_ser.data

                    return Response(context, status=status.HTTP_200_OK)

                else:
                    context["message"] = "No emailed invoices within this date range"
                    return Response(context, status=status.HTTP_404_NOT_FOUND)
            
            # return Response(context, status=status.HTTP_200_OK)
        

        elif how == "custom date":
            invoices = ProformaInvoice.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(status="Overdue")\
                            .order_by("date_created")

            if len(invoices) > 0:
                invoice_ser = ProformerInvoiceSerailizer(invoices, many=True)
                key = f"{start_date} - {end_date}"

                # total_amount = 0
                # for inv in invoice_ser.data:
                #         total_amount += float(inv['grand_total'])

                # context[key] = total_amount
                context[key] = invoice_ser.data

                return Response(context, status=status.HTTP_200_OK)

            else:
                context["message"] = "No invoices were created within this date range"
                return Response(context, status=status.HTTP_404_NOT_FOUND)

    
    # 3.9
    elif measure == "detail proforma pending":
        context = {}
        how = request.query_params.get("how")

        if how == "hour":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_hours = int((interval.days*1440 + interval.seconds/60)/60)

            # total_data = {}
            for hour in range(0, total_hours+1):
                current_time = start_time + timedelta(hours=hour)
                invoices = ProformaInvoice.objects.filter(date_created__date=current_time.date())\
                                          .filter(date_created__hour=current_time.hour)\
                                          .filter(status="Pending")\
                                            .order_by("date_created")
                invoice_ser = ProformerInvoiceSerailizer(invoices, many=True)

                # context['message'] = invoice_ser.data
                context[current_time.strftime('%Y-%m-%d %I%p')] = invoice_ser.data

                # # for inv in invoice_ser.data:
                # total_amount = 0
                # for inv in invoice_ser.data:
                #         total_amount += float(inv['grand_total'])

            
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "day":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_days = int(((interval.days*1440 + interval.seconds/60)/60)/24)

            # total_data = {}
            for day in range(0, total_days+1):
                current_time = start_time + timedelta(days=day)
                invoices = ProformaInvoice.objects.filter(date_created__date=current_time.date())\
                                            .filter(status="Pending")\
                                            .order_by("date_created")

                invoice_ser = ProformerInvoiceSerailizer(invoices, many=True)

                # total_amount = 0
                # for inv in invoice_ser.data:
                #         total_amount += float(inv['grand_total'])

                context[current_time.strftime('%Y-%m-%d')] = invoice_ser.data
                
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "week":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_weeks = int((((interval.days*1440 + interval.seconds/60)/60)/24)/7)

            if total_weeks > 0:
                for week in range(0, total_weeks+1):
                    start_time += timedelta(weeks=week)
                    current_week = start_time + timedelta(weeks=week+1)

                    if current_week > end_time:
                        current_week = end_time

                    invoices = ProformaInvoice.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)\
                                                .filter(status="Pending")\
                                                .order_by("date_created")
                    invoice_ser = ProformerInvoiceSerailizer(invoices, many=True)
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    context[key] = invoice_ser.data                        
                
                return Response(context, status=status.HTTP_200_OK)

            else:
                invoices = ProformaInvoice.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(status="Pending")\
                            .order_by("date_created")

                if len(invoices) > 0:
                    invoice_ser = ProformerInvoiceSerailizer(invoices, many=True)
                    key = f"{start_date} - {end_date}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    # context[key] = total_amount
                    context[key] = invoice_ser.data

                    return Response(context, status=status.HTTP_200_OK)

                else:
                    context["message"] = "No emailed invoices within this date range"
                    return Response(context, status=status.HTTP_404_NOT_FOUND)
            
            # return Response(context, status=status.HTTP_200_OK)
        
        elif how == "months":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_months = int(((((interval.days*1440 + interval.seconds/60)/60)/24)/7)/4)

            if total_months > 0:
                for week in range(0, total_months+1):
                    start_time += timedelta(weeks=week*4)
                    current_week = start_time + timedelta(weeks=(week+1)*4)

                    if current_week > end_time:
                        current_week = end_time

                    invoices = ProformaInvoice.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)\
                                                .filter(status="Pending")\
                                                .order_by("date_created")

                    invoice_ser = ProformerInvoiceSerailizer(invoices, many=True)
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"
                    # key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    # context[key] = total_amount
                    context[key] = invoice_ser.data
                return Response(context, status=status.HTTP_200_OK)

            else:
                invoices = ProformaInvoice.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(status="Pending")\
                            .order_by("date_created")

                if len(invoices) > 0:
                    invoice_ser = ProformerInvoiceSerailizer(invoices, many=True)
                    key = f"{start_date} - {end_date}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    # context[key] = total_amount
                    context[key] = invoice_ser.data

                    return Response(context, status=status.HTTP_200_OK)

                else:
                    context["message"] = "No emailed invoices within this date range"
                    return Response(context, status=status.HTTP_404_NOT_FOUND)
            
            # return Response(context, status=status.HTTP_200_OK)
        

        elif how == "custom date":
            invoices = ProformaInvoice.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(status="Pending")\
                            .order_by("date_created")

            if len(invoices) > 0:
                invoice_ser = ProformerInvoiceSerailizer(invoices, many=True)
                key = f"{start_date} - {end_date}"

                # total_amount = 0
                # for inv in invoice_ser.data:
                #         total_amount += float(inv['grand_total'])

                # context[key] = total_amount
                context[key] = invoice_ser.data

                return Response(context, status=status.HTTP_200_OK)

            else:
                context["message"] = "No invoices were created within this date range"
                return Response(context, status=status.HTTP_404_NOT_FOUND)


   


@api_view(["GET"])
@authentication_classes((MyAuthentication, ))
@permission_classes((IsAuthenticated, ))
def purchase_report(request):
    context = {}
    measure = request.query_params.get("measure", None)
    start_date = request.query_params.get("start", None)
    end_date = request.query_params.get("end", None)

    # 4.1
    if measure == "purchase search":
        invoices = PurchaseOrder.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date).all().order_by("date_created")
        if len(invoices) > 0:
            invoice_ser = PurchaseOrderSerailizer(invoices, many=True)
            context['message'] = invoice_ser.data

            return Response(context, status=status.HTTP_200_OK)

        else:
            context["message"] = "No purchase orders were created within this date range"
            return Response(context, status=status.HTTP_404_NOT_FOUND)
    
    # 4.2
    elif measure == "amount search":
        invoices = PurchaseOrder.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date).all().order_by("date_created")

        if len(invoices) > 0:
            invoice_ser = PurchaseOrderSerailizer(invoices, many=True)
            context['message'] = invoice_ser.data

            return Response(context, status=status.HTTP_200_OK)

        else:
            context["message"] = "No purchase orders were created within this date range"
            return Response(context, status=status.HTTP_404_NOT_FOUND)
    

    # 4.3
    elif measure == "per customer":
        invoices = PurchaseOrder.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date).all().order_by("date_created")

        if len(invoices) > 0:
            invoice_ser = PurchaseOrderSerailizer(invoices, many=True)
            total_data = {}
            for inv in invoice_ser.data:
                full_name = inv['customer']['first_name'] + " " + inv['customer']['last_name']
                if full_name in total_data:
                    total_data[full_name] += float(inv['grand_total'])
                else:
                    total_data[full_name] = 0
            
            final_data = []
            for k,v in total_data.items():
                final_data.append({"full_name": k, "total_amount": v})

            context['message'] = final_data


            return Response(context, status=status.HTTP_200_OK)

        else:
            context["message"] = "No purchase orders were created within this date range"
            return Response(context, status=status.HTTP_404_NOT_FOUND)
    
    # 4.4
    elif measure == "total per date":
        context = {}
        how = request.query_params.get("how")

        if how == "hour":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_hours = int((interval.days*1440 + interval.seconds/60)/60)

            # total_data = {}
            for hour in range(0, total_hours+1):
                current_time = start_time + timedelta(hours=hour)
                invoices = PurchaseOrder.objects.filter(date_created__date=current_time.date())\
                                          .filter(date_created__hour=current_time.hour)
                invoice_ser = PurchaseOrderSerailizer(invoices, many=True)

                # for inv in invoice_ser.data:
                total_amount = 0
                for inv in invoice_ser.data:
                        total_amount += float(inv['grand_total'])

                context[current_time.strftime('%Y-%m-%d %I%p')] = total_amount
            
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "day":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_days = int(((interval.days*1440 + interval.seconds/60)/60)/24)

            # total_data = {}
            for day in range(0, total_days+1):
                current_time = start_time + timedelta(days=day)
                invoices = PurchaseOrder.objects.filter(date_created__date=current_time.date())

                invoice_ser = PurchaseOrderSerailizer(invoices, many=True)

                total_amount = 0
                for inv in invoice_ser.data:
                        total_amount += float(inv['grand_total'])

                context[current_time.strftime('%Y-%m-%d')] = total_amount
                
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "week":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_weeks = int((((interval.days*1440 + interval.seconds/60)/60)/24)/7)

            if total_weeks > 0:
                for week in range(0, total_weeks+1):
                    start_time += timedelta(weeks=week)
                    current_week = start_time + timedelta(weeks=week+1)

                    if current_week > end_time:
                        current_week = end_time

                    invoices = PurchaseOrder.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)
                    invoice_ser = PurchaseOrderSerailizer(invoices, many=True)
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"

                    total_amount = 0
                    for inv in invoice_ser.data:
                            total_amount += float(inv['grand_total'])

                    context[key] = total_amount
                        
                    # context[key] = invoice_ser.data
                
                return Response(context, status=status.HTTP_200_OK)

            else:
                invoices = PurchaseOrder.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date).all().order_by("date_created")

                if len(invoices) > 0:
                    invoice_ser = PurchaseOrderSerailizer(invoices, many=True)
                    key = f"{start_date} - {end_date}"

                    total_amount = 0
                    for inv in invoice_ser.data:
                            total_amount += float(inv['grand_total'])

                    context[key] = total_amount
                    # context['message'] = invoice_ser.data

                    return Response(context, status=status.HTTP_200_OK)

                else:
                    context["message"] = "No invoices were created within this date range"
                    return Response(context, status=status.HTTP_404_NOT_FOUND)
            
            # return Response(context, status=status.HTTP_200_OK)
        
        elif how == "months":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_months = int(((((interval.days*1440 + interval.seconds/60)/60)/24)/7)/4)

            if total_months > 0:
                for week in range(0, total_months+1):
                    start_time += timedelta(weeks=week*4)
                    current_week = start_time + timedelta(weeks=(week+1)*4)

                    if current_week > end_time:
                        current_week = end_time

                    invoices = PurchaseOrder.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)
                    invoice_ser = PurchaseOrderSerailizer(invoices, many=True)
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"
                    # key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"

                    total_amount = 0
                    for inv in invoice_ser.data:
                            total_amount += float(inv['grand_total'])

                    context[key] = total_amount
                    # context[key] = invoice_ser.data
                return Response(context, status=status.HTTP_200_OK)

            else:
                invoices = PurchaseOrder.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date).all().order_by("date_created")

                if len(invoices) > 0:
                    invoice_ser = PurchaseOrderSerailizer(invoices, many=True)
                    key = f"{start_date} - {end_date}"

                    total_amount = 0
                    for inv in invoice_ser.data:
                            total_amount += float(inv['grand_total'])

                    context[key] = total_amount
                    # context['message'] = invoice_ser.data

                    return Response(context, status=status.HTTP_200_OK)

                else:
                    context["message"] = "No invoices were created within this date range"
                    return Response(context, status=status.HTTP_404_NOT_FOUND)
            
            # return Response(context, status=status.HTTP_200_OK)
        

        elif how == "custom date":
            invoices = PurchaseOrder.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date).all().order_by("date_created")

            if len(invoices) > 0:
                invoice_ser = PurchaseOrderSerailizer(invoices, many=True)
                key = f"{start_date} - {end_date}"

                total_amount = 0
                for inv in invoice_ser.data:
                        total_amount += float(inv['grand_total'])

                context[key] = total_amount
                # context['message'] = invoice_ser.data

                return Response(context, status=status.HTTP_200_OK)

            else:
                context["message"] = "No purchase orders were created within this date range"
                return Response(context, status=status.HTTP_404_NOT_FOUND)


    
    # 4.5
    elif measure == "count purchase email":
        context = {}
        how = request.query_params.get("how")

        if how == "hour":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_hours = int((interval.days*1440 + interval.seconds/60)/60)

            
            for hour in range(0, total_hours+1):
                current_time = start_time + timedelta(hours=hour)
                emailed_count = PurchaseOrder.objects.filter(date_created__date=current_time.date())\
                                          .filter(date_created__hour=current_time.hour)\
                                            .filter(emailed=True).count()
                
                context[current_time.strftime('%Y-%m-%d %I%p')] = emailed_count
                

            
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "day":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_days = int(((interval.days*1440 + interval.seconds/60)/60)/24)

            
            for day in range(0, total_days+1):
                current_time = start_time + timedelta(days=day)
                
                emailed_count = PurchaseOrder.objects.filter(date_created__date=current_time.date())\
                                            .filter(emailed=True).count()
                
                context[current_time.strftime('%Y-%m-%d')] = emailed_count

                

                
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "week":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_weeks = int((((interval.days*1440 + interval.seconds/60)/60)/24)/7)

            if total_weeks > 0:
                for week in range(0, total_weeks+1):
                    start_time += timedelta(weeks=week)
                    current_week = start_time + timedelta(weeks=week+1)

                    if current_week > end_time:
                        current_week = end_time

                    emailed_count = PurchaseOrder.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)\
                                                .filter(emailed=True).count()
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"
                    context[key] = emailed_count
                            
                    
                
                return Response(context, status=status.HTTP_200_OK)

            else:
                emailed_count = PurchaseOrder.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(emailed=True)\
                            .count()

                key = f"{start_date} - {end_date}"
                context[key] = emailed_count
                return Response(context, status=status.HTTP_200_OK)
                
        
        elif how == "months":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_months = int(((((interval.days*1440 + interval.seconds/60)/60)/24)/7)/4)

            if total_months > 0:
                for week in range(0, total_months+1):
                    start_time += timedelta(weeks=week*4)
                    current_week = start_time + timedelta(weeks=(week+1)*4)

                    if current_week > end_time:
                        current_week = end_time

                    emailed_count = PurchaseOrder.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)\
                                                .filter(emailed=True).count()
                    
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"
                    context[key] = emailed_count
                    
                return Response(context, status=status.HTTP_200_OK)

            else:
                emailed_count = PurchaseOrder.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(emailed=True).count()

                key = f"{start_date} - {end_date}"
                context[key] = emailed_count
                return Response(context, status=status.HTTP_200_OK)
                
        

        elif how == "custom date":
            emailed_count = PurchaseOrder.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(emailed=True).count()
                
            key = f"{start_date} - {end_date}"
            context[key] = emailed_count
            return Response(context, status=status.HTTP_200_OK)
    

    # 4.6
    elif measure == "detail purchase email":
        context = {}
        how = request.query_params.get("how")

        if how == "hour":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_hours = int((interval.days*1440 + interval.seconds/60)/60)

            # total_data = {}
            for hour in range(0, total_hours+1):
                current_time = start_time + timedelta(hours=hour)
                invoices = PurchaseOrder.objects.filter(date_created__date=current_time.date())\
                                          .filter(date_created__hour=current_time.hour)\
                                          .filter(emailed=True)
                invoice_ser = PurchaseOrderSerailizer(invoices, many=True)

                # context['message'] = invoice_ser.data
                context[current_time.strftime('%Y-%m-%d %I%p')] = invoice_ser.data

                # # for inv in invoice_ser.data:
                # total_amount = 0
                # for inv in invoice_ser.data:
                #         total_amount += float(inv['grand_total'])

            
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "day":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_days = int(((interval.days*1440 + interval.seconds/60)/60)/24)

            # total_data = {}
            for day in range(0, total_days+1):
                current_time = start_time + timedelta(days=day)
                invoices = PurchaseOrder.objects.filter(date_created__date=current_time.date())\
                                            .filter(emailed=True)

                invoice_ser = PurchaseOrderSerailizer(invoices, many=True)

                # total_amount = 0
                # for inv in invoice_ser.data:
                #         total_amount += float(inv['grand_total'])

                context[current_time.strftime('%Y-%m-%d')] = invoice_ser.data
                
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "week":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_weeks = int((((interval.days*1440 + interval.seconds/60)/60)/24)/7)

            if total_weeks > 0:
                for week in range(0, total_weeks+1):
                    start_time += timedelta(weeks=week)
                    current_week = start_time + timedelta(weeks=week+1)

                    if current_week > end_time:
                        current_week = end_time

                    invoices = PurchaseOrder.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)\
                                                .filter(emailed=True)
                    invoice_ser = PurchaseOrderSerailizer(invoices, many=True)
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    context[key] = invoice_ser.data                        
                
                return Response(context, status=status.HTTP_200_OK)

            else:
                invoices = PurchaseOrder.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(emailed=True)\
                            .order_by("date_created")

                if len(invoices) > 0:
                    invoice_ser = PurchaseOrderSerailizer(invoices, many=True)
                    key = f"{start_date} - {end_date}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    # context[key] = total_amount
                    context[key] = invoice_ser.data

                    return Response(context, status=status.HTTP_200_OK)

                else:
                    context["message"] = "No purchase orders were created within this date range"
                    return Response(context, status=status.HTTP_404_NOT_FOUND)
            
            # return Response(context, status=status.HTTP_200_OK)
        
        elif how == "months":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_months = int(((((interval.days*1440 + interval.seconds/60)/60)/24)/7)/4)

            if total_months > 0:
                for week in range(0, total_months+1):
                    start_time += timedelta(weeks=week*4)
                    current_week = start_time + timedelta(weeks=(week+1)*4)

                    if current_week > end_time:
                        current_week = end_time

                    invoices = PurchaseOrder.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)\
                                                .filter(emailed=True)\
                                                .order_by("date_created")

                    invoice_ser = PurchaseOrderSerailizer(invoices, many=True)
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"
                    # key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    # context[key] = total_amount
                    context[key] = invoice_ser.data
                return Response(context, status=status.HTTP_200_OK)

            else:
                invoices = PurchaseOrder.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(emailed=True)\
                            .order_by("date_created")

                if len(invoices) > 0:
                    invoice_ser = PurchaseOrderSerailizer(invoices, many=True)
                    key = f"{start_date} - {end_date}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    # context[key] = total_amount
                    context[key] = invoice_ser.data

                    return Response(context, status=status.HTTP_200_OK)

                else:
                    context["message"] = "No purchase orders were created within this date range"
                    return Response(context, status=status.HTTP_404_NOT_FOUND)
            
            # return Response(context, status=status.HTTP_200_OK)
        

        elif how == "custom date":
            invoices = PurchaseOrder.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(emailed=True)\
                            .order_by("date_created")

            if len(invoices) > 0:
                invoice_ser = PurchaseOrderSerailizer(invoices, many=True)
                key = f"{start_date} - {end_date}"

                # total_amount = 0
                # for inv in invoice_ser.data:
                #         total_amount += float(inv['grand_total'])

                # context[key] = total_amount
                context[key] = invoice_ser.data

                return Response(context, status=status.HTTP_200_OK)

            else:
                context["message"] = "No invoices were created within this date range"
                return Response(context, status=status.HTTP_404_NOT_FOUND)


    

    # 4.7
    elif measure == "count purchase overdue":

        context = {}
        how = request.query_params.get("how")

        if how == "hour":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_hours = int((interval.days*1440 + interval.seconds/60)/60)

            
            for hour in range(0, total_hours+1):
                current_time = start_time + timedelta(hours=hour)
                overdue_count = PurchaseOrder.objects.filter(date_created__date=current_time.date())\
                                          .filter(date_created__hour=current_time.hour)\
                                            .filter(status="Overdue").count()
                
                context[current_time.strftime('%Y-%m-%d %I%p')] = overdue_count
                

            
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "day":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_days = int(((interval.days*1440 + interval.seconds/60)/60)/24)

            
            for day in range(0, total_days+1):
                current_time = start_time + timedelta(days=day)
                
                overdue_count = PurchaseOrder.objects.filter(date_created__date=current_time.date())\
                                            .filter(status="Overdue").count()
                
                context[current_time.strftime('%Y-%m-%d')] = overdue_count

                

                
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "week":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_weeks = int((((interval.days*1440 + interval.seconds/60)/60)/24)/7)

            if total_weeks > 0:
                for week in range(0, total_weeks+1):
                    start_time += timedelta(weeks=week)
                    current_week = start_time + timedelta(weeks=week+1)

                    if current_week > end_time:
                        current_week = end_time

                    overdue_count = PurchaseOrder.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)\
                                                .filter(status="Overdue").count()
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"
                    context[key] = overdue_count
                            
                    
                
                return Response(context, status=status.HTTP_200_OK)

            else:
                overdue_count = PurchaseOrder.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(status="Overdue")\
                            .count()

                key = f"{start_date} - {end_date}"
                context[key] = overdue_count
                return Response(context, status=status.HTTP_200_OK)
                
        
        elif how == "months":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_months = int(((((interval.days*1440 + interval.seconds/60)/60)/24)/7)/4)

            if total_months > 0:
                for week in range(0, total_months+1):
                    start_time += timedelta(weeks=week*4)
                    current_week = start_time + timedelta(weeks=(week+1)*4)

                    if current_week > end_time:
                        current_week = end_time

                    overdue_count = PurchaseOrder.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)\
                                                .filter(status="Overdue").count()
                    
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"
                    context[key] = overdue_count
                    
                return Response(context, status=status.HTTP_200_OK)

            else:
                overdue_count = PurchaseOrder.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(status="Overdue").count()

                key = f"{start_date} - {end_date}"
                context[key] = overdue_count
                return Response(context, status=status.HTTP_200_OK)
                
        

        elif how == "custom date":
            overdue_count = PurchaseOrder.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(status="Overdue").count()
                
            key = f"{start_date} - {end_date}"
            context[key] = overdue_count
            return Response(context, status=status.HTTP_200_OK)


    # 4.8
    elif measure == "detail purchase overdue":
        context = {}
        how = request.query_params.get("how")

        if how == "hour":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_hours = int((interval.days*1440 + interval.seconds/60)/60)

            # total_data = {}
            for hour in range(0, total_hours+1):
                current_time = start_time + timedelta(hours=hour)
                invoices = PurchaseOrder.objects.filter(date_created__date=current_time.date())\
                                          .filter(date_created__hour=current_time.hour)\
                                          .filter(status="Overdue")\
                                            .order_by("date_created")
                invoice_ser = PurchaseOrderSerailizer(invoices, many=True)

                # context['message'] = invoice_ser.data
                context[current_time.strftime('%Y-%m-%d %I%p')] = invoice_ser.data

                # # for inv in invoice_ser.data:
                # total_amount = 0
                # for inv in invoice_ser.data:
                #         total_amount += float(inv['grand_total'])

            
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "day":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_days = int(((interval.days*1440 + interval.seconds/60)/60)/24)

            # total_data = {}
            for day in range(0, total_days+1):
                current_time = start_time + timedelta(days=day)
                invoices = PurchaseOrder.objects.filter(date_created__date=current_time.date())\
                                            .filter(status="Overdue")\
                                            .order_by("date_created")

                invoice_ser = PurchaseOrderSerailizer(invoices, many=True)

                # total_amount = 0
                # for inv in invoice_ser.data:
                #         total_amount += float(inv['grand_total'])

                context[current_time.strftime('%Y-%m-%d')] = invoice_ser.data
                
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "week":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_weeks = int((((interval.days*1440 + interval.seconds/60)/60)/24)/7)

            if total_weeks > 0:
                for week in range(0, total_weeks+1):
                    start_time += timedelta(weeks=week)
                    current_week = start_time + timedelta(weeks=week+1)

                    if current_week > end_time:
                        current_week = end_time

                    invoices = PurchaseOrder.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)\
                                                .filter(status="Overdue")\
                                                .order_by("date_created")
                    invoice_ser = PurchaseOrderSerailizer(invoices, many=True)
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    context[key] = invoice_ser.data                        
                
                return Response(context, status=status.HTTP_200_OK)

            else:
                invoices = PurchaseOrder.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(status="Overdue")\
                            .order_by("date_created")

                if len(invoices) > 0:
                    invoice_ser = PurchaseOrderSerailizer(invoices, many=True)
                    key = f"{start_date} - {end_date}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    # context[key] = total_amount
                    context[key] = invoice_ser.data

                    return Response(context, status=status.HTTP_200_OK)

                else:
                    context["message"] = "No purchase orders were created within this date range"
                    return Response(context, status=status.HTTP_404_NOT_FOUND)
            
            # return Response(context, status=status.HTTP_200_OK)
        
        elif how == "months":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_months = int(((((interval.days*1440 + interval.seconds/60)/60)/24)/7)/4)

            if total_months > 0:
                for week in range(0, total_months+1):
                    start_time += timedelta(weeks=week*4)
                    current_week = start_time + timedelta(weeks=(week+1)*4)

                    if current_week > end_time:
                        current_week = end_time

                    invoices = PurchaseOrder.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)\
                                                .filter(status="Overdue")\
                                                .order_by("date_created")

                    invoice_ser = PurchaseOrderSerailizer(invoices, many=True)
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"
                    # key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    # context[key] = total_amount
                    context[key] = invoice_ser.data
                return Response(context, status=status.HTTP_200_OK)

            else:
                invoices = PurchaseOrder.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(status="Overdue")\
                            .order_by("date_created")

                if len(invoices) > 0:
                    invoice_ser = PurchaseOrderSerailizer(invoices, many=True)
                    key = f"{start_date} - {end_date}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    # context[key] = total_amount
                    context[key] = invoice_ser.data

                    return Response(context, status=status.HTTP_200_OK)

                else:
                    context["message"] = "No purchase orders were created within this date range"
                    return Response(context, status=status.HTTP_404_NOT_FOUND)
            
            # return Response(context, status=status.HTTP_200_OK)
        

        elif how == "custom date":
            invoices = PurchaseOrder.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(status="Overdue")\
                            .order_by("date_created")

            if len(invoices) > 0:
                invoice_ser = PurchaseOrderSerailizer(invoices, many=True)
                key = f"{start_date} - {end_date}"

                # total_amount = 0
                # for inv in invoice_ser.data:
                #         total_amount += float(inv['grand_total'])

                # context[key] = total_amount
                context[key] = invoice_ser.data

                return Response(context, status=status.HTTP_200_OK)

            else:
                context["message"] = "No purchase orders were created within this date range"
                return Response(context, status=status.HTTP_404_NOT_FOUND)

    
    # 4.9
    elif measure == "detail purchase pending":
        context = {}
        how = request.query_params.get("how")

        if how == "hour":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_hours = int((interval.days*1440 + interval.seconds/60)/60)

            # total_data = {}
            for hour in range(0, total_hours+1):
                current_time = start_time + timedelta(hours=hour)
                invoices = PurchaseOrder.objects.filter(date_created__date=current_time.date())\
                                          .filter(date_created__hour=current_time.hour)\
                                          .filter(status="Pending")\
                                            .order_by("date_created")
                invoice_ser = PurchaseOrderSerailizer(invoices, many=True)

                # context['message'] = invoice_ser.data
                context[current_time.strftime('%Y-%m-%d %I%p')] = invoice_ser.data

                # # for inv in invoice_ser.data:
                # total_amount = 0
                # for inv in invoice_ser.data:
                #         total_amount += float(inv['grand_total'])

            
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "day":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_days = int(((interval.days*1440 + interval.seconds/60)/60)/24)

            # total_data = {}
            for day in range(0, total_days+1):
                current_time = start_time + timedelta(days=day)
                invoices = PurchaseOrder.objects.filter(date_created__date=current_time.date())\
                                            .filter(status="Pending")\
                                            .order_by("date_created")

                invoice_ser = PurchaseOrderSerailizer(invoices, many=True)

                # total_amount = 0
                # for inv in invoice_ser.data:
                #         total_amount += float(inv['grand_total'])

                context[current_time.strftime('%Y-%m-%d')] = invoice_ser.data
                
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "week":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_weeks = int((((interval.days*1440 + interval.seconds/60)/60)/24)/7)

            if total_weeks > 0:
                for week in range(0, total_weeks+1):
                    start_time += timedelta(weeks=week)
                    current_week = start_time + timedelta(weeks=week+1)

                    if current_week > end_time:
                        current_week = end_time

                    invoices = PurchaseOrder.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)\
                                                .filter(status="Pending")\
                                                .order_by("date_created")
                    invoice_ser = PurchaseOrderSerailizer(invoices, many=True)
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    context[key] = invoice_ser.data                        
                
                return Response(context, status=status.HTTP_200_OK)

            else:
                invoices = PurchaseOrder.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(status="Pending")\
                            .order_by("date_created")

                if len(invoices) > 0:
                    invoice_ser = PurchaseOrderSerailizer(invoices, many=True)
                    key = f"{start_date} - {end_date}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    # context[key] = total_amount
                    context[key] = invoice_ser.data

                    return Response(context, status=status.HTTP_200_OK)

                else:
                    context["message"] = "No purchase orders were created within this date range"
                    return Response(context, status=status.HTTP_404_NOT_FOUND)
            
            # return Response(context, status=status.HTTP_200_OK)
        
        elif how == "months":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_months = int(((((interval.days*1440 + interval.seconds/60)/60)/24)/7)/4)

            if total_months > 0:
                for week in range(0, total_months+1):
                    start_time += timedelta(weeks=week*4)
                    current_week = start_time + timedelta(weeks=(week+1)*4)

                    if current_week > end_time:
                        current_week = end_time

                    invoices = PurchaseOrder.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)\
                                                .filter(status="Pending")\
                                                .order_by("date_created")

                    invoice_ser = PurchaseOrderSerailizer(invoices, many=True)
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"
                    # key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    # context[key] = total_amount
                    context[key] = invoice_ser.data
                return Response(context, status=status.HTTP_200_OK)

            else:
                invoices = PurchaseOrder.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(status="Pending")\
                            .order_by("date_created")

                if len(invoices) > 0:
                    invoice_ser = PurchaseOrderSerailizer(invoices, many=True)
                    key = f"{start_date} - {end_date}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    # context[key] = total_amount
                    context[key] = invoice_ser.data

                    return Response(context, status=status.HTTP_200_OK)

                else:
                    context["message"] = "No purchase orders were created within this date range"
                    return Response(context, status=status.HTTP_404_NOT_FOUND)
            
            # return Response(context, status=status.HTTP_200_OK)
        

        elif how == "custom date":
            invoices = PurchaseOrder.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(status="Pending")\
                            .order_by("date_created")

            if len(invoices) > 0:
                invoice_ser = PurchaseOrderSerailizer(invoices, many=True)
                key = f"{start_date} - {end_date}"

                # total_amount = 0
                # for inv in invoice_ser.data:
                #         total_amount += float(inv['grand_total'])

                # context[key] = total_amount
                context[key] = invoice_ser.data

                return Response(context, status=status.HTTP_200_OK)

            else:
                context["message"] = "No purchase orders were created within this date range"
                return Response(context, status=status.HTTP_404_NOT_FOUND)





@api_view(["GET"])
@authentication_classes((MyAuthentication, ))
@permission_classes((IsAuthenticated, ))
def estimate_report(request):
    context = {}
    measure = request.query_params.get("measure", None)
    start_date = request.query_params.get("start", None)
    end_date = request.query_params.get("end", None)

    # 5.1
    if measure == "estimate search":
        invoices = Estimate.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date).all().order_by("date_created")
        if len(invoices) > 0:
            invoice_ser = EstimateSerailizer(invoices, many=True)
            context['message'] = invoice_ser.data

            return Response(context, status=status.HTTP_200_OK)

        else:
            context["message"] = "No estimates were created within this date range"
            return Response(context, status=status.HTTP_404_NOT_FOUND)
    
    # 5.2
    elif measure == "amount search":
        invoices = Estimate.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date).all().order_by("date_created")

        if len(invoices) > 0:
            invoice_ser = EstimateSerailizer(invoices, many=True)
            context['message'] = invoice_ser.data

            return Response(context, status=status.HTTP_200_OK)

        else:
            context["message"] = "No estimates were created within this date range"
            return Response(context, status=status.HTTP_404_NOT_FOUND)
    

    # 5.3
    elif measure == "per customer":
        invoices = Estimate.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date).all().order_by("date_created")

        if len(invoices) > 0:
            invoice_ser = EstimateSerailizer(invoices, many=True)
            total_data = {}
            for inv in invoice_ser.data:
                full_name = inv['customer']['first_name'] + " " + inv['customer']['last_name']
                if full_name in total_data:
                    total_data[full_name] += float(inv['grand_total'])
                else:
                    total_data[full_name] = 0
            
            final_data = []
            for k,v in total_data.items():
                final_data.append({"full_name": k, "total_amount": v})

            context['message'] = final_data


            return Response(context, status=status.HTTP_200_OK)

        else:
            context["message"] = "No estimates were created within this date range"
            return Response(context, status=status.HTTP_404_NOT_FOUND)
    
    # 5.4
    elif measure == "total per date":
        context = {}
        how = request.query_params.get("how")

        if how == "hour":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_hours = int((interval.days*1440 + interval.seconds/60)/60)

            # total_data = {}
            for hour in range(0, total_hours+1):
                current_time = start_time + timedelta(hours=hour)
                invoices = Estimate.objects.filter(date_created__date=current_time.date())\
                                          .filter(date_created__hour=current_time.hour)
                invoice_ser = EstimateSerailizer(invoices, many=True)

                # for inv in invoice_ser.data:
                total_amount = 0
                for inv in invoice_ser.data:
                        total_amount += float(inv['grand_total'])

                context[current_time.strftime('%Y-%m-%d %I%p')] = total_amount
            
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "day":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_days = int(((interval.days*1440 + interval.seconds/60)/60)/24)

            # total_data = {}
            for day in range(0, total_days+1):
                current_time = start_time + timedelta(days=day)
                invoices = Estimate.objects.filter(date_created__date=current_time.date())

                invoice_ser = EstimateSerailizer(invoices, many=True)

                total_amount = 0
                for inv in invoice_ser.data:
                        total_amount += float(inv['grand_total'])

                context[current_time.strftime('%Y-%m-%d')] = total_amount
                
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "week":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_weeks = int((((interval.days*1440 + interval.seconds/60)/60)/24)/7)

            if total_weeks > 0:
                for week in range(0, total_weeks+1):
                    start_time += timedelta(weeks=week)
                    current_week = start_time + timedelta(weeks=week+1)

                    if current_week > end_time:
                        current_week = end_time

                    invoices = Estimate.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)
                    invoice_ser = EstimateSerailizer(invoices, many=True)
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"

                    total_amount = 0
                    for inv in invoice_ser.data:
                            total_amount += float(inv['grand_total'])

                    context[key] = total_amount
                        
                    # context[key] = invoice_ser.data
                
                return Response(context, status=status.HTTP_200_OK)

            else:
                invoices = Estimate.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date).all().order_by("date_created")

                if len(invoices) > 0:
                    invoice_ser = EstimateSerailizer(invoices, many=True)
                    key = f"{start_date} - {end_date}"

                    total_amount = 0
                    for inv in invoice_ser.data:
                            total_amount += float(inv['grand_total'])

                    context[key] = total_amount
                    # context['message'] = invoice_ser.data

                    return Response(context, status=status.HTTP_200_OK)

                else:
                    context["message"] = "No estimates were created within this date range"
                    return Response(context, status=status.HTTP_404_NOT_FOUND)
            
            # return Response(context, status=status.HTTP_200_OK)
        
        elif how == "months":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_months = int(((((interval.days*1440 + interval.seconds/60)/60)/24)/7)/4)

            if total_months > 0:
                for week in range(0, total_months+1):
                    start_time += timedelta(weeks=week*4)
                    current_week = start_time + timedelta(weeks=(week+1)*4)

                    if current_week > end_time:
                        current_week = end_time

                    invoices = Estimate.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)
                    invoice_ser = EstimateSerailizer(invoices, many=True)
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"
                    # key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"

                    total_amount = 0
                    for inv in invoice_ser.data:
                            total_amount += float(inv['grand_total'])

                    context[key] = total_amount
                    # context[key] = invoice_ser.data
                return Response(context, status=status.HTTP_200_OK)

            else:
                invoices = Estimate.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date).all().order_by("date_created")

                if len(invoices) > 0:
                    invoice_ser = EstimateSerailizer(invoices, many=True)
                    key = f"{start_date} - {end_date}"

                    total_amount = 0
                    for inv in invoice_ser.data:
                            total_amount += float(inv['grand_total'])

                    context[key] = total_amount
                    # context['message'] = invoice_ser.data

                    return Response(context, status=status.HTTP_200_OK)

                else:
                    context["message"] = "No estimates were created within this date range"
                    return Response(context, status=status.HTTP_404_NOT_FOUND)
            
            # return Response(context, status=status.HTTP_200_OK)
        

        elif how == "custom date":
            invoices = Estimate.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date).all().order_by("date_created")

            if len(invoices) > 0:
                invoice_ser = EstimateSerailizer(invoices, many=True)
                key = f"{start_date} - {end_date}"

                total_amount = 0
                for inv in invoice_ser.data:
                        total_amount += float(inv['grand_total'])

                context[key] = total_amount
                # context['message'] = invoice_ser.data

                return Response(context, status=status.HTTP_200_OK)

            else:
                context["message"] = "No estimates were created within this date range"
                return Response(context, status=status.HTTP_404_NOT_FOUND)


    
    # 5.5
    elif measure == "count estimate email":
        context = {}
        how = request.query_params.get("how")

        if how == "hour":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_hours = int((interval.days*1440 + interval.seconds/60)/60)

            
            for hour in range(0, total_hours+1):
                current_time = start_time + timedelta(hours=hour)
                emailed_count = Estimate.objects.filter(date_created__date=current_time.date())\
                                          .filter(date_created__hour=current_time.hour)\
                                            .filter(emailed=True).count()
                
                context[current_time.strftime('%Y-%m-%d %I%p')] = emailed_count
                

            
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "day":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_days = int(((interval.days*1440 + interval.seconds/60)/60)/24)

            
            for day in range(0, total_days+1):
                current_time = start_time + timedelta(days=day)
                
                emailed_count = Estimate.objects.filter(date_created__date=current_time.date())\
                                            .filter(emailed=True).count()
                
                context[current_time.strftime('%Y-%m-%d')] = emailed_count

                

                
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "week":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_weeks = int((((interval.days*1440 + interval.seconds/60)/60)/24)/7)

            if total_weeks > 0:
                for week in range(0, total_weeks+1):
                    start_time += timedelta(weeks=week)
                    current_week = start_time + timedelta(weeks=week+1)

                    if current_week > end_time:
                        current_week = end_time

                    emailed_count = Estimate.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)\
                                                .filter(emailed=True).count()
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"
                    context[key] = emailed_count
                            
                    
                
                return Response(context, status=status.HTTP_200_OK)

            else:
                emailed_count = Estimate.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(emailed=True)\
                            .count()

                key = f"{start_date} - {end_date}"
                context[key] = emailed_count
                return Response(context, status=status.HTTP_200_OK)
                
        
        elif how == "months":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_months = int(((((interval.days*1440 + interval.seconds/60)/60)/24)/7)/4)

            if total_months > 0:
                for week in range(0, total_months+1):
                    start_time += timedelta(weeks=week*4)
                    current_week = start_time + timedelta(weeks=(week+1)*4)

                    if current_week > end_time:
                        current_week = end_time

                    emailed_count = Estimate.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)\
                                                .filter(emailed=True).count()
                    
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"
                    context[key] = emailed_count
                    
                return Response(context, status=status.HTTP_200_OK)

            else:
                emailed_count = Estimate.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(emailed=True).count()

                key = f"{start_date} - {end_date}"
                context[key] = emailed_count
                return Response(context, status=status.HTTP_200_OK)
                
        

        elif how == "custom date":
            emailed_count = Estimate.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(emailed=True).count()
                
            key = f"{start_date} - {end_date}"
            context[key] = emailed_count
            return Response(context, status=status.HTTP_200_OK)
    

    # 5.6
    elif measure == "detail estimate email":
        context = {}
        how = request.query_params.get("how")

        if how == "hour":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_hours = int((interval.days*1440 + interval.seconds/60)/60)

            # total_data = {}
            for hour in range(0, total_hours+1):
                current_time = start_time + timedelta(hours=hour)
                invoices = Estimate.objects.filter(date_created__date=current_time.date())\
                                          .filter(date_created__hour=current_time.hour)\
                                          .filter(emailed=True)
                invoice_ser = EstimateSerailizer(invoices, many=True)

                # context['message'] = invoice_ser.data
                context[current_time.strftime('%Y-%m-%d %I%p')] = invoice_ser.data

                # # for inv in invoice_ser.data:
                # total_amount = 0
                # for inv in invoice_ser.data:
                #         total_amount += float(inv['grand_total'])

            
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "day":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_days = int(((interval.days*1440 + interval.seconds/60)/60)/24)

            # total_data = {}
            for day in range(0, total_days+1):
                current_time = start_time + timedelta(days=day)
                invoices = Estimate.objects.filter(date_created__date=current_time.date())\
                                            .filter(emailed=True)

                invoice_ser = EstimateSerailizer(invoices, many=True)

                # total_amount = 0
                # for inv in invoice_ser.data:
                #         total_amount += float(inv['grand_total'])

                context[current_time.strftime('%Y-%m-%d')] = invoice_ser.data
                
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "week":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_weeks = int((((interval.days*1440 + interval.seconds/60)/60)/24)/7)

            if total_weeks > 0:
                for week in range(0, total_weeks+1):
                    start_time += timedelta(weeks=week)
                    current_week = start_time + timedelta(weeks=week+1)

                    if current_week > end_time:
                        current_week = end_time

                    invoices = Estimate.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)\
                                                .filter(emailed=True)
                    invoice_ser = EstimateSerailizer(invoices, many=True)
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    context[key] = invoice_ser.data                        
                
                return Response(context, status=status.HTTP_200_OK)

            else:
                invoices = Estimate.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(emailed=True)\
                            .order_by("date_created")

                if len(invoices) > 0:
                    invoice_ser = EstimateSerailizer(invoices, many=True)
                    key = f"{start_date} - {end_date}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    # context[key] = total_amount
                    context[key] = invoice_ser.data

                    return Response(context, status=status.HTTP_200_OK)

                else:
                    context["message"] = "No emailed invoices within this date range"
                    return Response(context, status=status.HTTP_404_NOT_FOUND)
            
            # return Response(context, status=status.HTTP_200_OK)
        
        elif how == "months":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_months = int(((((interval.days*1440 + interval.seconds/60)/60)/24)/7)/4)

            if total_months > 0:
                for week in range(0, total_months+1):
                    start_time += timedelta(weeks=week*4)
                    current_week = start_time + timedelta(weeks=(week+1)*4)

                    if current_week > end_time:
                        current_week = end_time

                    invoices = Estimate.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)\
                                                .filter(emailed=True)\
                                                .order_by("date_created")

                    invoice_ser = EstimateSerailizer(invoices, many=True)
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"
                    # key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    # context[key] = total_amount
                    context[key] = invoice_ser.data
                return Response(context, status=status.HTTP_200_OK)

            else:
                invoices = Estimate.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(emailed=True)\
                            .order_by("date_created")

                if len(invoices) > 0:
                    invoice_ser = EstimateSerailizer(invoices, many=True)
                    key = f"{start_date} - {end_date}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    # context[key] = total_amount
                    context[key] = invoice_ser.data

                    return Response(context, status=status.HTTP_200_OK)

                else:
                    context["message"] = "No estimates were created within this date range"
                    return Response(context, status=status.HTTP_404_NOT_FOUND)
            
            # return Response(context, status=status.HTTP_200_OK)
        

        elif how == "custom date":
            invoices = Estimate.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(emailed=True)\
                            .order_by("date_created")

            if len(invoices) > 0:
                invoice_ser = EstimateSerailizer(invoices, many=True)
                key = f"{start_date} - {end_date}"

                # total_amount = 0
                # for inv in invoice_ser.data:
                #         total_amount += float(inv['grand_total'])

                # context[key] = total_amount
                context[key] = invoice_ser.data

                return Response(context, status=status.HTTP_200_OK)

            else:
                context["message"] = "No estimates were created within this date range"
                return Response(context, status=status.HTTP_404_NOT_FOUND)


    

    # 5.7
    elif measure == "count estimate overdue":

        context = {}
        how = request.query_params.get("how")

        if how == "hour":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_hours = int((interval.days*1440 + interval.seconds/60)/60)

            
            for hour in range(0, total_hours+1):
                current_time = start_time + timedelta(hours=hour)
                overdue_count = Estimate.objects.filter(date_created__date=current_time.date())\
                                          .filter(date_created__hour=current_time.hour)\
                                            .filter(status="Overdue").count()
                
                context[current_time.strftime('%Y-%m-%d %I%p')] = overdue_count
                

            
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "day":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_days = int(((interval.days*1440 + interval.seconds/60)/60)/24)

            
            for day in range(0, total_days+1):
                current_time = start_time + timedelta(days=day)
                
                overdue_count = Estimate.objects.filter(date_created__date=current_time.date())\
                                            .filter(status="Overdue").count()
                
                context[current_time.strftime('%Y-%m-%d')] = overdue_count

                

                
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "week":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_weeks = int((((interval.days*1440 + interval.seconds/60)/60)/24)/7)

            if total_weeks > 0:
                for week in range(0, total_weeks+1):
                    start_time += timedelta(weeks=week)
                    current_week = start_time + timedelta(weeks=week+1)

                    if current_week > end_time:
                        current_week = end_time

                    overdue_count = Estimate.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)\
                                                .filter(status="Overdue").count()
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"
                    context[key] = overdue_count
                            
                    
                
                return Response(context, status=status.HTTP_200_OK)

            else:
                overdue_count = Estimate.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(status="Overdue")\
                            .count()

                key = f"{start_date} - {end_date}"
                context[key] = overdue_count
                return Response(context, status=status.HTTP_200_OK)
                
        
        elif how == "months":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_months = int(((((interval.days*1440 + interval.seconds/60)/60)/24)/7)/4)

            if total_months > 0:
                for week in range(0, total_months+1):
                    start_time += timedelta(weeks=week*4)
                    current_week = start_time + timedelta(weeks=(week+1)*4)

                    if current_week > end_time:
                        current_week = end_time

                    overdue_count = Estimate.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)\
                                                .filter(status="Overdue").count()
                    
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"
                    context[key] = overdue_count
                    
                return Response(context, status=status.HTTP_200_OK)

            else:
                overdue_count = Estimate.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(status="Overdue").count()

                key = f"{start_date} - {end_date}"
                context[key] = overdue_count
                return Response(context, status=status.HTTP_200_OK)
                
        

        elif how == "custom date":
            overdue_count = Estimate.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(status="Overdue").count()
                
            key = f"{start_date} - {end_date}"
            context[key] = overdue_count
            return Response(context, status=status.HTTP_200_OK)


    # 5.8
    elif measure == "detail estimate overdue":
        context = {}
        how = request.query_params.get("how")

        if how == "hour":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_hours = int((interval.days*1440 + interval.seconds/60)/60)

            # total_data = {}
            for hour in range(0, total_hours+1):
                current_time = start_time + timedelta(hours=hour)
                invoices = Estimate.objects.filter(date_created__date=current_time.date())\
                                          .filter(date_created__hour=current_time.hour)\
                                          .filter(status="Overdue")\
                                            .order_by("date_created")
                invoice_ser = EstimateSerailizer(invoices, many=True)

                # context['message'] = invoice_ser.data
                context[current_time.strftime('%Y-%m-%d %I%p')] = invoice_ser.data

                # # for inv in invoice_ser.data:
                # total_amount = 0
                # for inv in invoice_ser.data:
                #         total_amount += float(inv['grand_total'])

            
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "day":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_days = int(((interval.days*1440 + interval.seconds/60)/60)/24)

            # total_data = {}
            for day in range(0, total_days+1):
                current_time = start_time + timedelta(days=day)
                invoices = Estimate.objects.filter(date_created__date=current_time.date())\
                                            .filter(status="Overdue")\
                                            .order_by("date_created")

                invoice_ser = EstimateSerailizer(invoices, many=True)

                # total_amount = 0
                # for inv in invoice_ser.data:
                #         total_amount += float(inv['grand_total'])

                context[current_time.strftime('%Y-%m-%d')] = invoice_ser.data
                
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "week":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_weeks = int((((interval.days*1440 + interval.seconds/60)/60)/24)/7)

            if total_weeks > 0:
                for week in range(0, total_weeks+1):
                    start_time += timedelta(weeks=week)
                    current_week = start_time + timedelta(weeks=week+1)

                    if current_week > end_time:
                        current_week = end_time

                    invoices = Estimate.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)\
                                                .filter(status="Overdue")\
                                                .order_by("date_created")
                    invoice_ser = EstimateSerailizer(invoices, many=True)
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    context[key] = invoice_ser.data                        
                
                return Response(context, status=status.HTTP_200_OK)

            else:
                invoices = Estimate.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(status="Overdue")\
                            .order_by("date_created")

                if len(invoices) > 0:
                    invoice_ser = EstimateSerailizer(invoices, many=True)
                    key = f"{start_date} - {end_date}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    # context[key] = total_amount
                    context[key] = invoice_ser.data

                    return Response(context, status=status.HTTP_200_OK)

                else:
                    context["message"] = "No emailed invoices within this date range"
                    return Response(context, status=status.HTTP_404_NOT_FOUND)
            
            # return Response(context, status=status.HTTP_200_OK)
        
        elif how == "months":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_months = int(((((interval.days*1440 + interval.seconds/60)/60)/24)/7)/4)

            if total_months > 0:
                for week in range(0, total_months+1):
                    start_time += timedelta(weeks=week*4)
                    current_week = start_time + timedelta(weeks=(week+1)*4)

                    if current_week > end_time:
                        current_week = end_time

                    invoices = Estimate.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)\
                                                .filter(status="Overdue")\
                                                .order_by("date_created")

                    invoice_ser = EstimateSerailizer(invoices, many=True)
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"
                    # key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    # context[key] = total_amount
                    context[key] = invoice_ser.data
                return Response(context, status=status.HTTP_200_OK)

            else:
                invoices = Estimate.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(status="Overdue")\
                            .order_by("date_created")

                if len(invoices) > 0:
                    invoice_ser = EstimateSerailizer(invoices, many=True)
                    key = f"{start_date} - {end_date}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    # context[key] = total_amount
                    context[key] = invoice_ser.data

                    return Response(context, status=status.HTTP_200_OK)

                else:
                    context["message"] = "No emailed invoices within this date range"
                    return Response(context, status=status.HTTP_404_NOT_FOUND)
            
            # return Response(context, status=status.HTTP_200_OK)
        

        elif how == "custom date":
            invoices = Estimate.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(status="Overdue")\
                            .order_by("date_created")

            if len(invoices) > 0:
                invoice_ser = EstimateSerailizer(invoices, many=True)
                key = f"{start_date} - {end_date}"

                # total_amount = 0
                # for inv in invoice_ser.data:
                #         total_amount += float(inv['grand_total'])

                # context[key] = total_amount
                context[key] = invoice_ser.data

                return Response(context, status=status.HTTP_200_OK)

            else:
                context["message"] = "No estimates were created within this date range"
                return Response(context, status=status.HTTP_404_NOT_FOUND)

    
    # 5.9
    elif measure == "detail estimate pending":
        context = {}
        how = request.query_params.get("how")

        if how == "hour":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_hours = int((interval.days*1440 + interval.seconds/60)/60)

            # total_data = {}
            for hour in range(0, total_hours+1):
                current_time = start_time + timedelta(hours=hour)
                invoices = Estimate.objects.filter(date_created__date=current_time.date())\
                                          .filter(date_created__hour=current_time.hour)\
                                          .filter(status="Pending")\
                                            .order_by("date_created")
                invoice_ser = EstimateSerailizer(invoices, many=True)

                # context['message'] = invoice_ser.data
                context[current_time.strftime('%Y-%m-%d %I%p')] = invoice_ser.data

                # # for inv in invoice_ser.data:
                # total_amount = 0
                # for inv in invoice_ser.data:
                #         total_amount += float(inv['grand_total'])

            
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "day":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_days = int(((interval.days*1440 + interval.seconds/60)/60)/24)

            # total_data = {}
            for day in range(0, total_days+1):
                current_time = start_time + timedelta(days=day)
                invoices = Estimate.objects.filter(date_created__date=current_time.date())\
                                            .filter(status="Pending")\
                                            .order_by("date_created")

                invoice_ser = EstimateSerailizer(invoices, many=True)

                # total_amount = 0
                # for inv in invoice_ser.data:
                #         total_amount += float(inv['grand_total'])

                context[current_time.strftime('%Y-%m-%d')] = invoice_ser.data
                
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "week":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_weeks = int((((interval.days*1440 + interval.seconds/60)/60)/24)/7)

            if total_weeks > 0:
                for week in range(0, total_weeks+1):
                    start_time += timedelta(weeks=week)
                    current_week = start_time + timedelta(weeks=week+1)

                    if current_week > end_time:
                        current_week = end_time

                    invoices = Estimate.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)\
                                                .filter(status="Pending")\
                                                .order_by("date_created")
                    invoice_ser = EstimateSerailizer(invoices, many=True)
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    context[key] = invoice_ser.data                        
                
                return Response(context, status=status.HTTP_200_OK)

            else:
                invoices = Estimate.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(status="Pending")\
                            .order_by("date_created")

                if len(invoices) > 0:
                    invoice_ser = EstimateSerailizer(invoices, many=True)
                    key = f"{start_date} - {end_date}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    # context[key] = total_amount
                    context[key] = invoice_ser.data

                    return Response(context, status=status.HTTP_200_OK)

                else:
                    context["message"] = "No emailed estimate within this date range"
                    return Response(context, status=status.HTTP_404_NOT_FOUND)
            
            # return Response(context, status=status.HTTP_200_OK)
        
        elif how == "months":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_months = int(((((interval.days*1440 + interval.seconds/60)/60)/24)/7)/4)

            if total_months > 0:
                for week in range(0, total_months+1):
                    start_time += timedelta(weeks=week*4)
                    current_week = start_time + timedelta(weeks=(week+1)*4)

                    if current_week > end_time:
                        current_week = end_time

                    invoices = Estimate.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)\
                                                .filter(status="Pending")\
                                                .order_by("date_created")

                    invoice_ser = EstimateSerailizer(invoices, many=True)
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"
                    # key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    # context[key] = total_amount
                    context[key] = invoice_ser.data
                return Response(context, status=status.HTTP_200_OK)

            else:
                invoices = Estimate.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(status="Pending")\
                            .order_by("date_created")

                if len(invoices) > 0:
                    invoice_ser = EstimateSerailizer(invoices, many=True)
                    key = f"{start_date} - {end_date}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    # context[key] = total_amount
                    context[key] = invoice_ser.data

                    return Response(context, status=status.HTTP_200_OK)

                else:
                    context["message"] = "No emailed estimate within this date range"
                    return Response(context, status=status.HTTP_404_NOT_FOUND)
            
            # return Response(context, status=status.HTTP_200_OK)
        

        elif how == "custom date":
            invoices = Estimate.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(status="Pending")\
                            .order_by("date_created")

            if len(invoices) > 0:
                invoice_ser = EstimateSerailizer(invoices, many=True)
                key = f"{start_date} - {end_date}"

                # total_amount = 0
                # for inv in invoice_ser.data:
                #         total_amount += float(inv['grand_total'])

                # context[key] = total_amount
                context[key] = invoice_ser.data

                return Response(context, status=status.HTTP_200_OK)

            else:
                context["message"] = "No estimates were created within this date range"
                return Response(context, status=status.HTTP_404_NOT_FOUND)



    # 5.10
    # elif measure == "detial estimate accepted":






@api_view(["GET"])
@authentication_classes((MyAuthentication, ))
@permission_classes((IsAuthenticated, ))
def quote_report(request):
    context = {}
    measure = request.query_params.get("measure", None)
    start_date = request.query_params.get("start", None)
    end_date = request.query_params.get("end", None)

    # 6.1
    if measure == "quote search":
        invoices = Quote.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date).all().order_by("date_created")
        if len(invoices) > 0:
            invoice_ser = QuoteSerailizer(invoices, many=True)
            context['message'] = invoice_ser.data

            return Response(context, status=status.HTTP_200_OK)

        else:
            context["message"] = "No quotes were created within this date range"
            return Response(context, status=status.HTTP_404_NOT_FOUND)
    
    # 6.2
    elif measure == "amount search":
        invoices = Quote.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date).all().order_by("date_created")

        if len(invoices) > 0:
            invoice_ser = QuoteSerailizer(invoices, many=True)
            context['message'] = invoice_ser.data

            return Response(context, status=status.HTTP_200_OK)

        else:
            context["message"] = "No quotes were created within this date range"
            return Response(context, status=status.HTTP_404_NOT_FOUND)
    

    # 6.3
    elif measure == "per customer":
        invoices = Quote.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date).all().order_by("date_created")

        if len(invoices) > 0:
            invoice_ser = QuoteSerailizer(invoices, many=True)
            total_data = {}
            for inv in invoice_ser.data:
                full_name = inv['customer']['first_name'] + " " + inv['customer']['last_name']
                if full_name in total_data:
                    total_data[full_name] += float(inv['grand_total'])
                else:
                    total_data[full_name] = 0
            
            final_data = []
            for k,v in total_data.items():
                final_data.append({"full_name": k, "total_amount": v})

            context['message'] = final_data


            return Response(context, status=status.HTTP_200_OK)

        else:
            context["message"] = "No quotes were created within this date range"
            return Response(context, status=status.HTTP_404_NOT_FOUND)
    
    # 6.4
    elif measure == "total per date":
        context = {}
        how = request.query_params.get("how")

        if how == "hour":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_hours = int((interval.days*1440 + interval.seconds/60)/60)

            # total_data = {}
            for hour in range(0, total_hours+1):
                current_time = start_time + timedelta(hours=hour)
                invoices = Quote.objects.filter(date_created__date=current_time.date())\
                                          .filter(date_created__hour=current_time.hour)
                invoice_ser = QuoteSerailizer(invoices, many=True)

                # for inv in invoice_ser.data:
                total_amount = 0
                for inv in invoice_ser.data:
                        total_amount += float(inv['grand_total'])

                context[current_time.strftime('%Y-%m-%d %I%p')] = total_amount
            
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "day":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_days = int(((interval.days*1440 + interval.seconds/60)/60)/24)

            # total_data = {}
            for day in range(0, total_days+1):
                current_time = start_time + timedelta(days=day)
                invoices = Quote.objects.filter(date_created__date=current_time.date())

                invoice_ser = QuoteSerailizer(invoices, many=True)

                total_amount = 0
                for inv in invoice_ser.data:
                        total_amount += float(inv['grand_total'])

                context[current_time.strftime('%Y-%m-%d')] = total_amount
                
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "week":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_weeks = int((((interval.days*1440 + interval.seconds/60)/60)/24)/7)

            if total_weeks > 0:
                for week in range(0, total_weeks+1):
                    start_time += timedelta(weeks=week)
                    current_week = start_time + timedelta(weeks=week+1)

                    if current_week > end_time:
                        current_week = end_time

                    invoices = Quote.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)
                    invoice_ser = QuoteSerailizer(invoices, many=True)
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"

                    total_amount = 0
                    for inv in invoice_ser.data:
                            total_amount += float(inv['grand_total'])

                    context[key] = total_amount
                        
                    # context[key] = invoice_ser.data
                
                return Response(context, status=status.HTTP_200_OK)

            else:
                invoices = Quote.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date).all().order_by("date_created")

                if len(invoices) > 0:
                    invoice_ser = QuoteSerailizer(invoices, many=True)
                    key = f"{start_date} - {end_date}"

                    total_amount = 0
                    for inv in invoice_ser.data:
                            total_amount += float(inv['grand_total'])

                    context[key] = total_amount
                    # context['message'] = invoice_ser.data

                    return Response(context, status=status.HTTP_200_OK)

                else:
                    context["message"] = "No quotes were created within this date range"
                    return Response(context, status=status.HTTP_404_NOT_FOUND)
            
            # return Response(context, status=status.HTTP_200_OK)
        
        elif how == "months":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_months = int(((((interval.days*1440 + interval.seconds/60)/60)/24)/7)/4)

            if total_months > 0:
                for week in range(0, total_months+1):
                    start_time += timedelta(weeks=week*4)
                    current_week = start_time + timedelta(weeks=(week+1)*4)

                    if current_week > end_time:
                        current_week = end_time

                    invoices = Quote.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)
                    invoice_ser = QuoteSerailizer(invoices, many=True)
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"
                    # key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"

                    total_amount = 0
                    for inv in invoice_ser.data:
                            total_amount += float(inv['grand_total'])

                    context[key] = total_amount
                    # context[key] = invoice_ser.data
                return Response(context, status=status.HTTP_200_OK)

            else:
                invoices = Quote.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date).all().order_by("date_created")

                if len(invoices) > 0:
                    invoice_ser = QuoteSerailizer(invoices, many=True)
                    key = f"{start_date} - {end_date}"

                    total_amount = 0
                    for inv in invoice_ser.data:
                            total_amount += float(inv['grand_total'])

                    context[key] = total_amount
                    # context['message'] = invoice_ser.data

                    return Response(context, status=status.HTTP_200_OK)

                else:
                    context["message"] = "No quotes were created within this date range"
                    return Response(context, status=status.HTTP_404_NOT_FOUND)
            
            # return Response(context, status=status.HTTP_200_OK)
        

        elif how == "custom date":
            invoices = Quote.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date).all().order_by("date_created")

            if len(invoices) > 0:
                invoice_ser = QuoteSerailizer(invoices, many=True)
                key = f"{start_date} - {end_date}"

                total_amount = 0
                for inv in invoice_ser.data:
                        total_amount += float(inv['grand_total'])

                context[key] = total_amount
                # context['message'] = invoice_ser.data

                return Response(context, status=status.HTTP_200_OK)

            else:
                context["message"] = "No quotes were created within this date range"
                return Response(context, status=status.HTTP_404_NOT_FOUND)


    
    # 6.5
    elif measure == "count quote email":
        context = {}
        how = request.query_params.get("how")

        if how == "hour":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_hours = int((interval.days*1440 + interval.seconds/60)/60)

            
            for hour in range(0, total_hours+1):
                current_time = start_time + timedelta(hours=hour)
                emailed_count = Quote.objects.filter(date_created__date=current_time.date())\
                                          .filter(date_created__hour=current_time.hour)\
                                            .filter(emailed=True).count()
                
                context[current_time.strftime('%Y-%m-%d %I%p')] = emailed_count
                

            
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "day":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_days = int(((interval.days*1440 + interval.seconds/60)/60)/24)

            
            for day in range(0, total_days+1):
                current_time = start_time + timedelta(days=day)
                
                emailed_count = Quote.objects.filter(date_created__date=current_time.date())\
                                            .filter(emailed=True).count()
                
                context[current_time.strftime('%Y-%m-%d')] = emailed_count

                

                
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "week":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_weeks = int((((interval.days*1440 + interval.seconds/60)/60)/24)/7)

            if total_weeks > 0:
                for week in range(0, total_weeks+1):
                    start_time += timedelta(weeks=week)
                    current_week = start_time + timedelta(weeks=week+1)

                    if current_week > end_time:
                        current_week = end_time

                    emailed_count = Quote.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)\
                                                .filter(emailed=True).count()
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"
                    context[key] = emailed_count
                            
                    
                
                return Response(context, status=status.HTTP_200_OK)

            else:
                emailed_count = Quote.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(emailed=True)\
                            .count()

                key = f"{start_date} - {end_date}"
                context[key] = emailed_count
                return Response(context, status=status.HTTP_200_OK)
                
        
        elif how == "months":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_months = int(((((interval.days*1440 + interval.seconds/60)/60)/24)/7)/4)

            if total_months > 0:
                for week in range(0, total_months+1):
                    start_time += timedelta(weeks=week*4)
                    current_week = start_time + timedelta(weeks=(week+1)*4)

                    if current_week > end_time:
                        current_week = end_time

                    emailed_count = Quote.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)\
                                                .filter(emailed=True).count()
                    
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"
                    context[key] = emailed_count
                    
                return Response(context, status=status.HTTP_200_OK)

            else:
                emailed_count = Quote.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(emailed=True).count()

                key = f"{start_date} - {end_date}"
                context[key] = emailed_count
                return Response(context, status=status.HTTP_200_OK)
                
        

        elif how == "custom date":
            emailed_count = Quote.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(emailed=True).count()
                
            key = f"{start_date} - {end_date}"
            context[key] = emailed_count
            return Response(context, status=status.HTTP_200_OK)
    

    # 6.6
    elif measure == "detail quote email":
        context = {}
        how = request.query_params.get("how")

        if how == "hour":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_hours = int((interval.days*1440 + interval.seconds/60)/60)

            # total_data = {}
            for hour in range(0, total_hours+1):
                current_time = start_time + timedelta(hours=hour)
                invoices = Quote.objects.filter(date_created__date=current_time.date())\
                                          .filter(date_created__hour=current_time.hour)\
                                          .filter(emailed=True)
                invoice_ser = QuoteSerailizer(invoices, many=True)

                # context['message'] = invoice_ser.data
                context[current_time.strftime('%Y-%m-%d %I%p')] = invoice_ser.data

                # # for inv in invoice_ser.data:
                # total_amount = 0
                # for inv in invoice_ser.data:
                #         total_amount += float(inv['grand_total'])

            
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "day":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_days = int(((interval.days*1440 + interval.seconds/60)/60)/24)

            # total_data = {}
            for day in range(0, total_days+1):
                current_time = start_time + timedelta(days=day)
                invoices = Quote.objects.filter(date_created__date=current_time.date())\
                                            .filter(emailed=True)

                invoice_ser = QuoteSerailizer(invoices, many=True)

                # total_amount = 0
                # for inv in invoice_ser.data:
                #         total_amount += float(inv['grand_total'])

                context[current_time.strftime('%Y-%m-%d')] = invoice_ser.data
                
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "week":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_weeks = int((((interval.days*1440 + interval.seconds/60)/60)/24)/7)

            if total_weeks > 0:
                for week in range(0, total_weeks+1):
                    start_time += timedelta(weeks=week)
                    current_week = start_time + timedelta(weeks=week+1)

                    if current_week > end_time:
                        current_week = end_time

                    invoices = Quote.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)\
                                                .filter(emailed=True)
                    invoice_ser = QuoteSerailizer(invoices, many=True)
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    context[key] = invoice_ser.data                        
                
                return Response(context, status=status.HTTP_200_OK)

            else:
                invoices = Quote.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(emailed=True)\
                            .order_by("date_created")

                if len(invoices) > 0:
                    invoice_ser = QuoteSerailizer(invoices, many=True)
                    key = f"{start_date} - {end_date}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    # context[key] = total_amount
                    context[key] = invoice_ser.data

                    return Response(context, status=status.HTTP_200_OK)

                else:
                    context["message"] = "No emailed quotes within this date range"
                    return Response(context, status=status.HTTP_404_NOT_FOUND)
            
            # return Response(context, status=status.HTTP_200_OK)
        
        elif how == "months":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_months = int(((((interval.days*1440 + interval.seconds/60)/60)/24)/7)/4)

            if total_months > 0:
                for week in range(0, total_months+1):
                    start_time += timedelta(weeks=week*4)
                    current_week = start_time + timedelta(weeks=(week+1)*4)

                    if current_week > end_time:
                        current_week = end_time

                    invoices = Quote.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)\
                                                .filter(emailed=True)\
                                                .order_by("date_created")

                    invoice_ser = QuoteSerailizer(invoices, many=True)
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"
                    # key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    # context[key] = total_amount
                    context[key] = invoice_ser.data
                return Response(context, status=status.HTTP_200_OK)

            else:
                invoices = Quote.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(emailed=True)\
                            .order_by("date_created")

                if len(invoices) > 0:
                    invoice_ser = QuoteSerailizer(invoices, many=True)
                    key = f"{start_date} - {end_date}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    # context[key] = total_amount
                    context[key] = invoice_ser.data

                    return Response(context, status=status.HTTP_200_OK)

                else:
                    context["message"] = "No emailed quotes within this date range"
                    return Response(context, status=status.HTTP_404_NOT_FOUND)
            
            # return Response(context, status=status.HTTP_200_OK)
        

        elif how == "custom date":
            invoices = Quote.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(emailed=True)\
                            .order_by("date_created")

            if len(invoices) > 0:
                invoice_ser = QuoteSerailizer(invoices, many=True)
                key = f"{start_date} - {end_date}"

                # total_amount = 0
                # for inv in invoice_ser.data:
                #         total_amount += float(inv['grand_total'])

                # context[key] = total_amount
                context[key] = invoice_ser.data

                return Response(context, status=status.HTTP_200_OK)

            else:
                context["message"] = "No quote were created within this date range"
                return Response(context, status=status.HTTP_404_NOT_FOUND)


    

    # 6.7
    elif measure == "count quote overdue":

        context = {}
        how = request.query_params.get("how")

        if how == "hour":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_hours = int((interval.days*1440 + interval.seconds/60)/60)

            
            for hour in range(0, total_hours+1):
                current_time = start_time + timedelta(hours=hour)
                overdue_count = Quote.objects.filter(date_created__date=current_time.date())\
                                          .filter(date_created__hour=current_time.hour)\
                                            .filter(status="Overdue").count()
                
                context[current_time.strftime('%Y-%m-%d %I%p')] = overdue_count
                

            
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "day":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_days = int(((interval.days*1440 + interval.seconds/60)/60)/24)

            
            for day in range(0, total_days+1):
                current_time = start_time + timedelta(days=day)
                
                overdue_count = Quote.objects.filter(date_created__date=current_time.date())\
                                            .filter(status="Overdue").count()
                
                context[current_time.strftime('%Y-%m-%d')] = overdue_count

                

                
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "week":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_weeks = int((((interval.days*1440 + interval.seconds/60)/60)/24)/7)

            if total_weeks > 0:
                for week in range(0, total_weeks+1):
                    start_time += timedelta(weeks=week)
                    current_week = start_time + timedelta(weeks=week+1)

                    if current_week > end_time:
                        current_week = end_time

                    overdue_count = Quote.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)\
                                                .filter(status="Overdue").count()
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"
                    context[key] = overdue_count
                            
                    
                
                return Response(context, status=status.HTTP_200_OK)

            else:
                overdue_count = Quote.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(status="Overdue")\
                            .count()

                key = f"{start_date} - {end_date}"
                context[key] = overdue_count
                return Response(context, status=status.HTTP_200_OK)
                
        
        elif how == "months":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_months = int(((((interval.days*1440 + interval.seconds/60)/60)/24)/7)/4)

            if total_months > 0:
                for week in range(0, total_months+1):
                    start_time += timedelta(weeks=week*4)
                    current_week = start_time + timedelta(weeks=(week+1)*4)

                    if current_week > end_time:
                        current_week = end_time

                    overdue_count = Quote.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)\
                                                .filter(status="Overdue").count()
                    
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"
                    context[key] = overdue_count
                    
                return Response(context, status=status.HTTP_200_OK)

            else:
                overdue_count = Quote.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(status="Overdue").count()

                key = f"{start_date} - {end_date}"
                context[key] = overdue_count
                return Response(context, status=status.HTTP_200_OK)
                
        

        elif how == "custom date":
            overdue_count = Quote.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(status="Overdue").count()
                
            key = f"{start_date} - {end_date}"
            context[key] = overdue_count
            return Response(context, status=status.HTTP_200_OK)


    # 6.8
    elif measure == "detail quote overdue":
        context = {}
        how = request.query_params.get("how")

        if how == "hour":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_hours = int((interval.days*1440 + interval.seconds/60)/60)

            # total_data = {}
            for hour in range(0, total_hours+1):
                current_time = start_time + timedelta(hours=hour)
                invoices = Quote.objects.filter(date_created__date=current_time.date())\
                                          .filter(date_created__hour=current_time.hour)\
                                          .filter(status="Overdue")\
                                            .order_by("date_created")
                invoice_ser = QuoteSerailizer(invoices, many=True)

                # context['message'] = invoice_ser.data
                context[current_time.strftime('%Y-%m-%d %I%p')] = invoice_ser.data

                # # for inv in invoice_ser.data:
                # total_amount = 0
                # for inv in invoice_ser.data:
                #         total_amount += float(inv['grand_total'])

            
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "day":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_days = int(((interval.days*1440 + interval.seconds/60)/60)/24)

            # total_data = {}
            for day in range(0, total_days+1):
                current_time = start_time + timedelta(days=day)
                invoices = Quote.objects.filter(date_created__date=current_time.date())\
                                            .filter(status="Overdue")\
                                            .order_by("date_created")

                invoice_ser = QuoteSerailizer(invoices, many=True)

                # total_amount = 0
                # for inv in invoice_ser.data:
                #         total_amount += float(inv['grand_total'])

                context[current_time.strftime('%Y-%m-%d')] = invoice_ser.data
                
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "week":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_weeks = int((((interval.days*1440 + interval.seconds/60)/60)/24)/7)

            if total_weeks > 0:
                for week in range(0, total_weeks+1):
                    start_time += timedelta(weeks=week)
                    current_week = start_time + timedelta(weeks=week+1)

                    if current_week > end_time:
                        current_week = end_time

                    invoices = Quote.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)\
                                                .filter(status="Overdue")\
                                                .order_by("date_created")
                    invoice_ser = QuoteSerailizer(invoices, many=True)
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    context[key] = invoice_ser.data                        
                
                return Response(context, status=status.HTTP_200_OK)

            else:
                invoices = Quote.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(status="Overdue")\
                            .order_by("date_created")

                if len(invoices) > 0:
                    invoice_ser = QuoteSerailizer(invoices, many=True)
                    key = f"{start_date} - {end_date}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    # context[key] = total_amount
                    context[key] = invoice_ser.data

                    return Response(context, status=status.HTTP_200_OK)

                else:
                    context["message"] = "No overdue quotes within this date range"
                    return Response(context, status=status.HTTP_404_NOT_FOUND)
            
            # return Response(context, status=status.HTTP_200_OK)
        
        elif how == "months":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_months = int(((((interval.days*1440 + interval.seconds/60)/60)/24)/7)/4)

            if total_months > 0:
                for week in range(0, total_months+1):
                    start_time += timedelta(weeks=week*4)
                    current_week = start_time + timedelta(weeks=(week+1)*4)

                    if current_week > end_time:
                        current_week = end_time

                    invoices = Quote.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)\
                                                .filter(status="Overdue")\
                                                .order_by("date_created")

                    invoice_ser = QuoteSerailizer(invoices, many=True)
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"
                    # key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    # context[key] = total_amount
                    context[key] = invoice_ser.data
                return Response(context, status=status.HTTP_200_OK)

            else:
                invoices = Quote.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(status="Overdue")\
                            .order_by("date_created")

                if len(invoices) > 0:
                    invoice_ser = QuoteSerailizer(invoices, many=True)
                    key = f"{start_date} - {end_date}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    # context[key] = total_amount
                    context[key] = invoice_ser.data

                    return Response(context, status=status.HTTP_200_OK)

                else:
                    context["message"] = "No overdue quotes within this date range"
                    return Response(context, status=status.HTTP_404_NOT_FOUND)
            
            # return Response(context, status=status.HTTP_200_OK)
        

        elif how == "custom date":
            invoices = Quote.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(status="Overdue")\
                            .order_by("date_created")

            if len(invoices) > 0:
                invoice_ser = QuoteSerailizer(invoices, many=True)
                key = f"{start_date} - {end_date}"

                # total_amount = 0
                # for inv in invoice_ser.data:
                #         total_amount += float(inv['grand_total'])

                # context[key] = total_amount
                context[key] = invoice_ser.data

                return Response(context, status=status.HTTP_200_OK)

            else:
                context["message"] = "No overdue were created within this date range"
                return Response(context, status=status.HTTP_404_NOT_FOUND)

    
    # 6.9
    elif measure == "detail quote pending":
        context = {}
        how = request.query_params.get("how")

        if how == "hour":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_hours = int((interval.days*1440 + interval.seconds/60)/60)

            # total_data = {}
            for hour in range(0, total_hours+1):
                current_time = start_time + timedelta(hours=hour)
                invoices = Quote.objects.filter(date_created__date=current_time.date())\
                                          .filter(date_created__hour=current_time.hour)\
                                          .filter(status="Pending")\
                                            .order_by("date_created")
                invoice_ser = QuoteSerailizer(invoices, many=True)

                # context['message'] = invoice_ser.data
                context[current_time.strftime('%Y-%m-%d %I%p')] = invoice_ser.data

                # # for inv in invoice_ser.data:
                # total_amount = 0
                # for inv in invoice_ser.data:
                #         total_amount += float(inv['grand_total'])

            
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "day":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_days = int(((interval.days*1440 + interval.seconds/60)/60)/24)

            # total_data = {}
            for day in range(0, total_days+1):
                current_time = start_time + timedelta(days=day)
                invoices = Quote.objects.filter(date_created__date=current_time.date())\
                                            .filter(status="Pending")\
                                            .order_by("date_created")

                invoice_ser = QuoteSerailizer(invoices, many=True)

                # total_amount = 0
                # for inv in invoice_ser.data:
                #         total_amount += float(inv['grand_total'])

                context[current_time.strftime('%Y-%m-%d')] = invoice_ser.data
                
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "week":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_weeks = int((((interval.days*1440 + interval.seconds/60)/60)/24)/7)

            if total_weeks > 0:
                for week in range(0, total_weeks+1):
                    start_time += timedelta(weeks=week)
                    current_week = start_time + timedelta(weeks=week+1)

                    if current_week > end_time:
                        current_week = end_time

                    invoices = Quote.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)\
                                                .filter(status="Pending")\
                                                .order_by("date_created")
                    invoice_ser = QuoteSerailizer(invoices, many=True)
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    context[key] = invoice_ser.data                        
                
                return Response(context, status=status.HTTP_200_OK)

            else:
                invoices = Quote.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(status="Pending")\
                            .order_by("date_created")

                if len(invoices) > 0:
                    invoice_ser = QuoteSerailizer(invoices, many=True)
                    key = f"{start_date} - {end_date}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    # context[key] = total_amount
                    context[key] = invoice_ser.data

                    return Response(context, status=status.HTTP_200_OK)

                else:
                    context["message"] = "No pending quote within this date range"
                    return Response(context, status=status.HTTP_404_NOT_FOUND)
            
            # return Response(context, status=status.HTTP_200_OK)
        
        elif how == "months":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_months = int(((((interval.days*1440 + interval.seconds/60)/60)/24)/7)/4)

            if total_months > 0:
                for week in range(0, total_months+1):
                    start_time += timedelta(weeks=week*4)
                    current_week = start_time + timedelta(weeks=(week+1)*4)

                    if current_week > end_time:
                        current_week = end_time

                    invoices = Quote.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)\
                                                .filter(status="Pending")\
                                                .order_by("date_created")

                    invoice_ser = QuoteSerailizer(invoices, many=True)
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"
                    # key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    # context[key] = total_amount
                    context[key] = invoice_ser.data
                return Response(context, status=status.HTTP_200_OK)

            else:
                invoices = Quote.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(status="Pending")\
                            .order_by("date_created")

                if len(invoices) > 0:
                    invoice_ser = QuoteSerailizer(invoices, many=True)
                    key = f"{start_date} - {end_date}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    # context[key] = total_amount
                    context[key] = invoice_ser.data

                    return Response(context, status=status.HTTP_200_OK)

                else:
                    context["message"] = "No pending quote within this date range"
                    return Response(context, status=status.HTTP_404_NOT_FOUND)
            
            # return Response(context, status=status.HTTP_200_OK)
        

        elif how == "custom date":
            invoices = Quote.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(status="Pending")\
                            .order_by("date_created")

            if len(invoices) > 0:
                invoice_ser = QuoteSerailizer(invoices, many=True)
                key = f"{start_date} - {end_date}"

                # total_amount = 0
                # for inv in invoice_ser.data:
                #         total_amount += float(inv['grand_total'])

                # context[key] = total_amount
                context[key] = invoice_ser.data

                return Response(context, status=status.HTTP_200_OK)

            else:
                context["message"] = "No pending quote within this date range"
                return Response(context, status=status.HTTP_404_NOT_FOUND)






@api_view(["GET"])
@authentication_classes((MyAuthentication, ))
@permission_classes((IsAuthenticated, ))
def receipt_report(request):
    context = {}
    measure = request.query_params.get("measure", None)
    start_date = request.query_params.get("start", None)
    end_date = request.query_params.get("end", None)

    # 7.1
    if measure == "receipt search":
        invoices = Receipt.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date).all().order_by("date_created")
        if len(invoices) > 0:
            invoice_ser = ReceiptSerailizer(invoices, many=True)
            context['message'] = invoice_ser.data

            return Response(context, status=status.HTTP_200_OK)

        else:
            context["message"] = "No receipts were created within this date range"
            return Response(context, status=status.HTTP_404_NOT_FOUND)
    
    # 7.2
    elif measure == "amount search":
        invoices = Receipt.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date).all().order_by("date_created")

        if len(invoices) > 0:
            invoice_ser = ReceiptSerailizer(invoices, many=True)
            context['message'] = invoice_ser.data

            return Response(context, status=status.HTTP_200_OK)

        else:
            context["message"] = "No receipts were created within this date range"
            return Response(context, status=status.HTTP_404_NOT_FOUND)
    

    # 7.3
    elif measure == "per customer":
        invoices = Receipt.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date).all().order_by("date_created")

        if len(invoices) > 0:
            invoice_ser = ReceiptSerailizer(invoices, many=True)
            total_data = {}
            for inv in invoice_ser.data:
                full_name = inv['customer']['first_name'] + " " + inv['customer']['last_name']
                if full_name in total_data:
                    total_data[full_name] += float(inv['grand_total'])
                else:
                    total_data[full_name] = 0
            
            final_data = []
            for k,v in total_data.items():
                final_data.append({"full_name": k, "total_amount": v})

            context['message'] = final_data


            return Response(context, status=status.HTTP_200_OK)

        else:
            context["message"] = "No receipts were created within this date range"
            return Response(context, status=status.HTTP_404_NOT_FOUND)
    
    # 7.4
    elif measure == "total per date":
        context = {}
        how = request.query_params.get("how")

        if how == "hour":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_hours = int((interval.days*1440 + interval.seconds/60)/60)

            # total_data = {}
            for hour in range(0, total_hours+1):
                current_time = start_time + timedelta(hours=hour)
                invoices = Receipt.objects.filter(date_created__date=current_time.date())\
                                          .filter(date_created__hour=current_time.hour)
                invoice_ser = ReceiptSerailizer(invoices, many=True)

                # for inv in invoice_ser.data:
                total_amount = 0
                for inv in invoice_ser.data:
                        total_amount += float(inv['grand_total'])

                context[current_time.strftime('%Y-%m-%d %I%p')] = total_amount
            
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "day":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_days = int(((interval.days*1440 + interval.seconds/60)/60)/24)

            # total_data = {}
            for day in range(0, total_days+1):
                current_time = start_time + timedelta(days=day)
                invoices = Receipt.objects.filter(date_created__date=current_time.date())

                invoice_ser = ReceiptSerailizer(invoices, many=True)

                total_amount = 0
                for inv in invoice_ser.data:
                        total_amount += float(inv['grand_total'])

                context[current_time.strftime('%Y-%m-%d')] = total_amount
                
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "week":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_weeks = int((((interval.days*1440 + interval.seconds/60)/60)/24)/7)

            if total_weeks > 0:
                for week in range(0, total_weeks+1):
                    start_time += timedelta(weeks=week)
                    current_week = start_time + timedelta(weeks=week+1)

                    if current_week > end_time:
                        current_week = end_time

                    invoices = Receipt.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)
                    invoice_ser = ReceiptSerailizer(invoices, many=True)
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"

                    total_amount = 0
                    for inv in invoice_ser.data:
                            total_amount += float(inv['grand_total'])

                    context[key] = total_amount
                        
                    # context[key] = invoice_ser.data
                
                return Response(context, status=status.HTTP_200_OK)

            else:
                invoices = Receipt.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date).all().order_by("date_created")

                if len(invoices) > 0:
                    invoice_ser = ReceiptSerailizer(invoices, many=True)
                    key = f"{start_date} - {end_date}"

                    total_amount = 0
                    for inv in invoice_ser.data:
                            total_amount += float(inv['grand_total'])

                    context[key] = total_amount
                    # context['message'] = invoice_ser.data

                    return Response(context, status=status.HTTP_200_OK)

                else:
                    context["message"] = "No receipts were created within this date range"
                    return Response(context, status=status.HTTP_404_NOT_FOUND)
            
            # return Response(context, status=status.HTTP_200_OK)
        
        elif how == "months":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_months = int(((((interval.days*1440 + interval.seconds/60)/60)/24)/7)/4)

            if total_months > 0:
                for week in range(0, total_months+1):
                    start_time += timedelta(weeks=week*4)
                    current_week = start_time + timedelta(weeks=(week+1)*4)

                    if current_week > end_time:
                        current_week = end_time

                    invoices = Receipt.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)
                    invoice_ser = ReceiptSerailizer(invoices, many=True)
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"
                    # key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"

                    total_amount = 0
                    for inv in invoice_ser.data:
                            total_amount += float(inv['grand_total'])

                    context[key] = total_amount
                    # context[key] = invoice_ser.data
                return Response(context, status=status.HTTP_200_OK)

            else:
                invoices = Receipt.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date).all().order_by("date_created")

                if len(invoices) > 0:
                    invoice_ser = ReceiptSerailizer(invoices, many=True)
                    key = f"{start_date} - {end_date}"

                    total_amount = 0
                    for inv in invoice_ser.data:
                            total_amount += float(inv['grand_total'])

                    context[key] = total_amount
                    # context['message'] = invoice_ser.data

                    return Response(context, status=status.HTTP_200_OK)

                else:
                    context["message"] = "No receipts were created within this date range"
                    return Response(context, status=status.HTTP_404_NOT_FOUND)
            
            # return Response(context, status=status.HTTP_200_OK)
        

        elif how == "custom date":
            invoices = Receipt.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date).all().order_by("date_created")

            if len(invoices) > 0:
                invoice_ser = ReceiptSerailizer(invoices, many=True)
                key = f"{start_date} - {end_date}"

                total_amount = 0
                for inv in invoice_ser.data:
                        total_amount += float(inv['grand_total'])

                context[key] = total_amount
                # context['message'] = invoice_ser.data

                return Response(context, status=status.HTTP_200_OK)

            else:
                context["message"] = "No receipts were created within this date range"
                return Response(context, status=status.HTTP_404_NOT_FOUND)


    
    # 7.5
    elif measure == "count receipt email":
        context = {}
        how = request.query_params.get("how")

        if how == "hour":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_hours = int((interval.days*1440 + interval.seconds/60)/60)

            
            for hour in range(0, total_hours+1):
                current_time = start_time + timedelta(hours=hour)
                emailed_count = Receipt.objects.filter(date_created__date=current_time.date())\
                                          .filter(date_created__hour=current_time.hour)\
                                            .filter(emailed=True).count()
                
                context[current_time.strftime('%Y-%m-%d %I%p')] = emailed_count
                

            
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "day":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_days = int(((interval.days*1440 + interval.seconds/60)/60)/24)

            
            for day in range(0, total_days+1):
                current_time = start_time + timedelta(days=day)
                
                emailed_count = Receipt.objects.filter(date_created__date=current_time.date())\
                                            .filter(emailed=True).count()
                
                context[current_time.strftime('%Y-%m-%d')] = emailed_count

                

                
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "week":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_weeks = int((((interval.days*1440 + interval.seconds/60)/60)/24)/7)

            if total_weeks > 0:
                for week in range(0, total_weeks+1):
                    start_time += timedelta(weeks=week)
                    current_week = start_time + timedelta(weeks=week+1)

                    if current_week > end_time:
                        current_week = end_time

                    emailed_count = Receipt.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)\
                                                .filter(emailed=True).count()
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"
                    context[key] = emailed_count
                            
                    
                
                return Response(context, status=status.HTTP_200_OK)

            else:
                emailed_count = Receipt.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(emailed=True)\
                            .count()

                key = f"{start_date} - {end_date}"
                context[key] = emailed_count
                return Response(context, status=status.HTTP_200_OK)
                
        
        elif how == "months":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_months = int(((((interval.days*1440 + interval.seconds/60)/60)/24)/7)/4)

            if total_months > 0:
                for week in range(0, total_months+1):
                    start_time += timedelta(weeks=week*4)
                    current_week = start_time + timedelta(weeks=(week+1)*4)

                    if current_week > end_time:
                        current_week = end_time

                    emailed_count = Receipt.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)\
                                                .filter(emailed=True).count()
                    
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"
                    context[key] = emailed_count
                    
                return Response(context, status=status.HTTP_200_OK)

            else:
                emailed_count = Receipt.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(emailed=True).count()

                key = f"{start_date} - {end_date}"
                context[key] = emailed_count
                return Response(context, status=status.HTTP_200_OK)
                
        

        elif how == "custom date":
            emailed_count = Receipt.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(emailed=True).count()
                
            key = f"{start_date} - {end_date}"
            context[key] = emailed_count
            return Response(context, status=status.HTTP_200_OK)
    

    # 7.6
    elif measure == "detail receipt email":
        context = {}
        how = request.query_params.get("how")

        if how == "hour":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_hours = int((interval.days*1440 + interval.seconds/60)/60)

            # total_data = {}
            for hour in range(0, total_hours+1):
                current_time = start_time + timedelta(hours=hour)
                invoices = Receipt.objects.filter(date_created__date=current_time.date())\
                                          .filter(date_created__hour=current_time.hour)\
                                          .filter(emailed=True)
                invoice_ser = ReceiptSerailizer(invoices, many=True)

                # context['message'] = invoice_ser.data
                context[current_time.strftime('%Y-%m-%d %I%p')] = invoice_ser.data

                # # for inv in invoice_ser.data:
                # total_amount = 0
                # for inv in invoice_ser.data:
                #         total_amount += float(inv['grand_total'])

            
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "day":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_days = int(((interval.days*1440 + interval.seconds/60)/60)/24)

            # total_data = {}
            for day in range(0, total_days+1):
                current_time = start_time + timedelta(days=day)
                invoices = Receipt.objects.filter(date_created__date=current_time.date())\
                                            .filter(emailed=True)

                invoice_ser = ReceiptSerailizer(invoices, many=True)

                # total_amount = 0
                # for inv in invoice_ser.data:
                #         total_amount += float(inv['grand_total'])

                context[current_time.strftime('%Y-%m-%d')] = invoice_ser.data
                
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "week":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_weeks = int((((interval.days*1440 + interval.seconds/60)/60)/24)/7)

            if total_weeks > 0:
                for week in range(0, total_weeks+1):
                    start_time += timedelta(weeks=week)
                    current_week = start_time + timedelta(weeks=week+1)

                    if current_week > end_time:
                        current_week = end_time

                    invoices = Receipt.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)\
                                                .filter(emailed=True)
                    invoice_ser = ReceiptSerailizer(invoices, many=True)
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    context[key] = invoice_ser.data                        
                
                return Response(context, status=status.HTTP_200_OK)

            else:
                invoices = Receipt.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(emailed=True)\
                            .order_by("date_created")

                if len(invoices) > 0:
                    invoice_ser = ReceiptSerailizer(invoices, many=True)
                    key = f"{start_date} - {end_date}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    # context[key] = total_amount
                    context[key] = invoice_ser.data

                    return Response(context, status=status.HTTP_200_OK)

                else:
                    context["message"] = "No emailed receipts within this date range"
                    return Response(context, status=status.HTTP_404_NOT_FOUND)
            
            # return Response(context, status=status.HTTP_200_OK)
        
        elif how == "months":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_months = int(((((interval.days*1440 + interval.seconds/60)/60)/24)/7)/4)

            if total_months > 0:
                for week in range(0, total_months+1):
                    start_time += timedelta(weeks=week*4)
                    current_week = start_time + timedelta(weeks=(week+1)*4)

                    if current_week > end_time:
                        current_week = end_time

                    invoices = Receipt.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)\
                                                .filter(emailed=True)\
                                                .order_by("date_created")

                    invoice_ser = ReceiptSerailizer(invoices, many=True)
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"
                    # key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    # context[key] = total_amount
                    context[key] = invoice_ser.data
                return Response(context, status=status.HTTP_200_OK)

            else:
                invoices = Receipt.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(emailed=True)\
                            .order_by("date_created")

                if len(invoices) > 0:
                    invoice_ser = ReceiptSerailizer(invoices, many=True)
                    key = f"{start_date} - {end_date}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    # context[key] = total_amount
                    context[key] = invoice_ser.data

                    return Response(context, status=status.HTTP_200_OK)

                else:
                    context["message"] = "No emailed receipts within this date range"
                    return Response(context, status=status.HTTP_404_NOT_FOUND)
            
            # return Response(context, status=status.HTTP_200_OK)
        

        elif how == "custom date":
            invoices = Receipt.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(emailed=True)\
                            .order_by("date_created")

            if len(invoices) > 0:
                invoice_ser = ReceiptSerailizer(invoices, many=True)
                key = f"{start_date} - {end_date}"

                # total_amount = 0
                # for inv in invoice_ser.data:
                #         total_amount += float(inv['grand_total'])

                # context[key] = total_amount
                context[key] = invoice_ser.data

                return Response(context, status=status.HTTP_200_OK)

            else:
                context["message"] = "No emailed receipts within this date range"
                return Response(context, status=status.HTTP_404_NOT_FOUND)






@api_view(["GET"])
@authentication_classes((MyAuthentication, ))
@permission_classes((IsAuthenticated, ))
def credit_report(request):
    context = {}
    measure = request.query_params.get("measure", None)
    start_date = request.query_params.get("start", None)
    end_date = request.query_params.get("end", None)

    # 8.1
    if measure == "credit search":
        invoices = CreditNote.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date).all().order_by("date_created")
        if len(invoices) > 0:
            invoice_ser = CreditNoteSerailizer(invoices, many=True)
            context['message'] = invoice_ser.data

            return Response(context, status=status.HTTP_200_OK)

        else:
            context["message"] = "No credit notes were created within this date range"
            return Response(context, status=status.HTTP_404_NOT_FOUND)
    
    # 8.2
    elif measure == "amount search":
        invoices = CreditNote.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date).all().order_by("date_created")

        if len(invoices) > 0:
            invoice_ser = CreditNoteSerailizer(invoices, many=True)
            context['message'] = invoice_ser.data

            return Response(context, status=status.HTTP_200_OK)

        else:
            context["message"] = "No credit notes were created within this date range"
            return Response(context, status=status.HTTP_404_NOT_FOUND)
    

    # 8.3
    elif measure == "per customer":
        invoices = CreditNote.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date).all().order_by("date_created")

        if len(invoices) > 0:
            invoice_ser = CreditNoteSerailizer(invoices, many=True)
            total_data = {}
            for inv in invoice_ser.data:
                full_name = inv['customer']['first_name'] + " " + inv['customer']['last_name']
                if full_name in total_data:
                    total_data[full_name] += float(inv['grand_total'])
                else:
                    total_data[full_name] = 0
            
            final_data = []
            for k,v in total_data.items():
                final_data.append({"full_name": k, "total_amount": v})

            context['message'] = final_data


            return Response(context, status=status.HTTP_200_OK)

        else:
            context["message"] = "No credit notes were created within this date range"
            return Response(context, status=status.HTTP_404_NOT_FOUND)
    
    # 8.4
    elif measure == "total per date":
        context = {}
        how = request.query_params.get("how")

        if how == "hour":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_hours = int((interval.days*1440 + interval.seconds/60)/60)

            # total_data = {}
            for hour in range(0, total_hours+1):
                current_time = start_time + timedelta(hours=hour)
                invoices = CreditNote.objects.filter(date_created__date=current_time.date())\
                                          .filter(date_created__hour=current_time.hour)
                invoice_ser = CreditNoteSerailizer(invoices, many=True)

                # for inv in invoice_ser.data:
                total_amount = 0
                for inv in invoice_ser.data:
                        total_amount += float(inv['grand_total'])

                context[current_time.strftime('%Y-%m-%d %I%p')] = total_amount
            
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "day":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_days = int(((interval.days*1440 + interval.seconds/60)/60)/24)

            # total_data = {}
            for day in range(0, total_days+1):
                current_time = start_time + timedelta(days=day)
                invoices = CreditNote.objects.filter(date_created__date=current_time.date())

                invoice_ser = CreditNoteSerailizer(invoices, many=True)

                total_amount = 0
                for inv in invoice_ser.data:
                        total_amount += float(inv['grand_total'])

                context[current_time.strftime('%Y-%m-%d')] = total_amount
                
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "week":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_weeks = int((((interval.days*1440 + interval.seconds/60)/60)/24)/7)

            if total_weeks > 0:
                for week in range(0, total_weeks+1):
                    start_time += timedelta(weeks=week)
                    current_week = start_time + timedelta(weeks=week+1)

                    if current_week > end_time:
                        current_week = end_time

                    invoices = CreditNote.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)
                    invoice_ser = CreditNoteSerailizer(invoices, many=True)
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"

                    total_amount = 0
                    for inv in invoice_ser.data:
                            total_amount += float(inv['grand_total'])

                    context[key] = total_amount
                        
                    # context[key] = invoice_ser.data
                
                return Response(context, status=status.HTTP_200_OK)

            else:
                invoices = CreditNote.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date).all().order_by("date_created")

                if len(invoices) > 0:
                    invoice_ser = CreditNoteSerailizer(invoices, many=True)
                    key = f"{start_date} - {end_date}"

                    total_amount = 0
                    for inv in invoice_ser.data:
                            total_amount += float(inv['grand_total'])

                    context[key] = total_amount
                    # context['message'] = invoice_ser.data

                    return Response(context, status=status.HTTP_200_OK)

                else:
                    context["message"] = "No credit notes were created within this date range"
                    return Response(context, status=status.HTTP_404_NOT_FOUND)
            
            # return Response(context, status=status.HTTP_200_OK)
        
        elif how == "months":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_months = int(((((interval.days*1440 + interval.seconds/60)/60)/24)/7)/4)

            if total_months > 0:
                for week in range(0, total_months+1):
                    start_time += timedelta(weeks=week*4)
                    current_week = start_time + timedelta(weeks=(week+1)*4)

                    if current_week > end_time:
                        current_week = end_time

                    invoices = CreditNote.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)
                    invoice_ser = CreditNoteSerailizer(invoices, many=True)
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"
                    # key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"

                    total_amount = 0
                    for inv in invoice_ser.data:
                            total_amount += float(inv['grand_total'])

                    context[key] = total_amount
                    # context[key] = invoice_ser.data
                return Response(context, status=status.HTTP_200_OK)

            else:
                invoices = CreditNote.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date).all().order_by("date_created")

                if len(invoices) > 0:
                    invoice_ser = CreditNoteSerailizer(invoices, many=True)
                    key = f"{start_date} - {end_date}"

                    total_amount = 0
                    for inv in invoice_ser.data:
                            total_amount += float(inv['grand_total'])

                    context[key] = total_amount
                    # context['message'] = invoice_ser.data

                    return Response(context, status=status.HTTP_200_OK)

                else:
                    context["message"] = "No credit notes were created within this date range"
                    return Response(context, status=status.HTTP_404_NOT_FOUND)
            
            # return Response(context, status=status.HTTP_200_OK)
        

        elif how == "custom date":
            invoices = CreditNote.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date).all().order_by("date_created")

            if len(invoices) > 0:
                invoice_ser = CreditNoteSerailizer(invoices, many=True)
                key = f"{start_date} - {end_date}"

                total_amount = 0
                for inv in invoice_ser.data:
                        total_amount += float(inv['grand_total'])

                context[key] = total_amount
                # context['message'] = invoice_ser.data

                return Response(context, status=status.HTTP_200_OK)

            else:
                context["message"] = "No credit notes were created within this date range"
                return Response(context, status=status.HTTP_404_NOT_FOUND)


    
    # 8.5
    elif measure == "count credit email":
        context = {}
        how = request.query_params.get("how")

        if how == "hour":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_hours = int((interval.days*1440 + interval.seconds/60)/60)

            
            for hour in range(0, total_hours+1):
                current_time = start_time + timedelta(hours=hour)
                emailed_count = CreditNote.objects.filter(date_created__date=current_time.date())\
                                          .filter(date_created__hour=current_time.hour)\
                                            .filter(emailed=True).count()
                
                context[current_time.strftime('%Y-%m-%d %I%p')] = emailed_count
                

            
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "day":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_days = int(((interval.days*1440 + interval.seconds/60)/60)/24)

            
            for day in range(0, total_days+1):
                current_time = start_time + timedelta(days=day)
                
                emailed_count = CreditNote.objects.filter(date_created__date=current_time.date())\
                                            .filter(emailed=True).count()
                
                context[current_time.strftime('%Y-%m-%d')] = emailed_count

                

                
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "week":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_weeks = int((((interval.days*1440 + interval.seconds/60)/60)/24)/7)

            if total_weeks > 0:
                for week in range(0, total_weeks+1):
                    start_time += timedelta(weeks=week)
                    current_week = start_time + timedelta(weeks=week+1)

                    if current_week > end_time:
                        current_week = end_time

                    emailed_count = CreditNote.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)\
                                                .filter(emailed=True).count()
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"
                    context[key] = emailed_count
                            
                    
                
                return Response(context, status=status.HTTP_200_OK)

            else:
                emailed_count = CreditNote.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(emailed=True)\
                            .count()

                key = f"{start_date} - {end_date}"
                context[key] = emailed_count
                return Response(context, status=status.HTTP_200_OK)
                
        
        elif how == "months":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_months = int(((((interval.days*1440 + interval.seconds/60)/60)/24)/7)/4)

            if total_months > 0:
                for week in range(0, total_months+1):
                    start_time += timedelta(weeks=week*4)
                    current_week = start_time + timedelta(weeks=(week+1)*4)

                    if current_week > end_time:
                        current_week = end_time

                    emailed_count = CreditNote.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)\
                                                .filter(emailed=True).count()
                    
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"
                    context[key] = emailed_count
                    
                return Response(context, status=status.HTTP_200_OK)

            else:
                emailed_count = CreditNote.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(emailed=True).count()

                key = f"{start_date} - {end_date}"
                context[key] = emailed_count
                return Response(context, status=status.HTTP_200_OK)
                
        

        elif how == "custom date":
            emailed_count = CreditNote.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(emailed=True).count()
                
            key = f"{start_date} - {end_date}"
            context[key] = emailed_count
            return Response(context, status=status.HTTP_200_OK)
    

    # 8.6
    elif measure == "detail credit email":
        context = {}
        how = request.query_params.get("how")

        if how == "hour":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_hours = int((interval.days*1440 + interval.seconds/60)/60)

            # total_data = {}
            for hour in range(0, total_hours+1):
                current_time = start_time + timedelta(hours=hour)
                invoices = CreditNote.objects.filter(date_created__date=current_time.date())\
                                          .filter(date_created__hour=current_time.hour)\
                                          .filter(emailed=True)
                invoice_ser = CreditNoteSerailizer(invoices, many=True)

                # context['message'] = invoice_ser.data
                context[current_time.strftime('%Y-%m-%d %I%p')] = invoice_ser.data

                # # for inv in invoice_ser.data:
                # total_amount = 0
                # for inv in invoice_ser.data:
                #         total_amount += float(inv['grand_total'])

            
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "day":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_days = int(((interval.days*1440 + interval.seconds/60)/60)/24)

            # total_data = {}
            for day in range(0, total_days+1):
                current_time = start_time + timedelta(days=day)
                invoices = CreditNote.objects.filter(date_created__date=current_time.date())\
                                            .filter(emailed=True)

                invoice_ser = CreditNoteSerailizer(invoices, many=True)

                # total_amount = 0
                # for inv in invoice_ser.data:
                #         total_amount += float(inv['grand_total'])

                context[current_time.strftime('%Y-%m-%d')] = invoice_ser.data
                
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "week":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_weeks = int((((interval.days*1440 + interval.seconds/60)/60)/24)/7)

            if total_weeks > 0:
                for week in range(0, total_weeks+1):
                    start_time += timedelta(weeks=week)
                    current_week = start_time + timedelta(weeks=week+1)

                    if current_week > end_time:
                        current_week = end_time

                    invoices = CreditNote.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)\
                                                .filter(emailed=True)
                    invoice_ser = CreditNoteSerailizer(invoices, many=True)
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    context[key] = invoice_ser.data                        
                
                return Response(context, status=status.HTTP_200_OK)

            else:
                invoices = CreditNote.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(emailed=True)\
                            .order_by("date_created")

                if len(invoices) > 0:
                    invoice_ser = CreditNoteSerailizer(invoices, many=True)
                    key = f"{start_date} - {end_date}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    # context[key] = total_amount
                    context[key] = invoice_ser.data

                    return Response(context, status=status.HTTP_200_OK)

                else:
                    context["message"] = "No emailed credit notes within this date range"
                    return Response(context, status=status.HTTP_404_NOT_FOUND)
            
            # return Response(context, status=status.HTTP_200_OK)
        
        elif how == "months":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_months = int(((((interval.days*1440 + interval.seconds/60)/60)/24)/7)/4)

            if total_months > 0:
                for week in range(0, total_months+1):
                    start_time += timedelta(weeks=week*4)
                    current_week = start_time + timedelta(weeks=(week+1)*4)

                    if current_week > end_time:
                        current_week = end_time

                    invoices = CreditNote.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)\
                                                .filter(emailed=True)\
                                                .order_by("date_created")

                    invoice_ser = CreditNoteSerailizer(invoices, many=True)
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"
                    # key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    # context[key] = total_amount
                    context[key] = invoice_ser.data
                return Response(context, status=status.HTTP_200_OK)

            else:
                invoices = CreditNote.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(emailed=True)\
                            .order_by("date_created")

                if len(invoices) > 0:
                    invoice_ser = CreditNoteSerailizer(invoices, many=True)
                    key = f"{start_date} - {end_date}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    # context[key] = total_amount
                    context[key] = invoice_ser.data

                    return Response(context, status=status.HTTP_200_OK)

                else:
                    context["message"] = "No emailed credit notes within this date range"
                    return Response(context, status=status.HTTP_404_NOT_FOUND)
            
            # return Response(context, status=status.HTTP_200_OK)
        

        elif how == "custom date":
            invoices = CreditNote.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(emailed=True)\
                            .order_by("date_created")

            if len(invoices) > 0:
                invoice_ser = CreditNoteSerailizer(invoices, many=True)
                key = f"{start_date} - {end_date}"

                # total_amount = 0
                # for inv in invoice_ser.data:
                #         total_amount += float(inv['grand_total'])

                # context[key] = total_amount
                context[key] = invoice_ser.data

                return Response(context, status=status.HTTP_200_OK)

            else:
                context["message"] = "No credit notes were created within this date range"
                return Response(context, status=status.HTTP_404_NOT_FOUND)


    

    # 8.7
    elif measure == "count credit pending":

        context = {}
        how = request.query_params.get("how")

        if how == "hour":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_hours = int((interval.days*1440 + interval.seconds/60)/60)

            
            for hour in range(0, total_hours+1):
                current_time = start_time + timedelta(hours=hour)
                overdue_count = CreditNote.objects.filter(date_created__date=current_time.date())\
                                          .filter(date_created__hour=current_time.hour)\
                                            .filter(status="Pending").count()
                
                context[current_time.strftime('%Y-%m-%d %I%p')] = overdue_count
                

            
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "day":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_days = int(((interval.days*1440 + interval.seconds/60)/60)/24)

            
            for day in range(0, total_days+1):
                current_time = start_time + timedelta(days=day)
                
                overdue_count = CreditNote.objects.filter(date_created__date=current_time.date())\
                                            .filter(status="Pending").count()
                
                context[current_time.strftime('%Y-%m-%d')] = overdue_count

                

                
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "week":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_weeks = int((((interval.days*1440 + interval.seconds/60)/60)/24)/7)

            if total_weeks > 0:
                for week in range(0, total_weeks+1):
                    start_time += timedelta(weeks=week)
                    current_week = start_time + timedelta(weeks=week+1)

                    if current_week > end_time:
                        current_week = end_time

                    overdue_count = CreditNote.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)\
                                                .filter(status="Pending").count()
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"
                    context[key] = overdue_count
                            
                    
                
                return Response(context, status=status.HTTP_200_OK)

            else:
                overdue_count = CreditNote.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(status="Pending")\
                            .count()

                key = f"{start_date} - {end_date}"
                context[key] = overdue_count
                return Response(context, status=status.HTTP_200_OK)
                
        
        elif how == "months":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_months = int(((((interval.days*1440 + interval.seconds/60)/60)/24)/7)/4)

            if total_months > 0:
                for week in range(0, total_months+1):
                    start_time += timedelta(weeks=week*4)
                    current_week = start_time + timedelta(weeks=(week+1)*4)

                    if current_week > end_time:
                        current_week = end_time

                    overdue_count = CreditNote.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)\
                                                .filter(status="Pending").count()
                    
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"
                    context[key] = overdue_count
                    
                return Response(context, status=status.HTTP_200_OK)

            else:
                overdue_count = CreditNote.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(status="Pending").count()

                key = f"{start_date} - {end_date}"
                context[key] = overdue_count
                return Response(context, status=status.HTTP_200_OK)
                
        

        elif how == "custom date":
            overdue_count = CreditNote.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(status="Pending").count()
                
            key = f"{start_date} - {end_date}"
            context[key] = overdue_count
            return Response(context, status=status.HTTP_200_OK)


    # 8.8
    elif measure == "detail invoice pending":
        context = {}
        how = request.query_params.get("how")

        if how == "hour":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_hours = int((interval.days*1440 + interval.seconds/60)/60)

            # total_data = {}
            for hour in range(0, total_hours+1):
                current_time = start_time + timedelta(hours=hour)
                invoices = CreditNote.objects.filter(date_created__date=current_time.date())\
                                          .filter(date_created__hour=current_time.hour)\
                                          .filter(status="Pending")\
                                            .order_by("date_created")
                invoice_ser = CreditNoteSerailizer(invoices, many=True)

                # context['message'] = invoice_ser.data
                context[current_time.strftime('%Y-%m-%d %I%p')] = invoice_ser.data

                # # for inv in invoice_ser.data:
                # total_amount = 0
                # for inv in invoice_ser.data:
                #         total_amount += float(inv['grand_total'])

            
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "day":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_days = int(((interval.days*1440 + interval.seconds/60)/60)/24)

            # total_data = {}
            for day in range(0, total_days+1):
                current_time = start_time + timedelta(days=day)
                invoices = CreditNote.objects.filter(date_created__date=current_time.date())\
                                            .filter(status="Pending")\
                                            .order_by("date_created")

                invoice_ser = CreditNoteSerailizer(invoices, many=True)

                # total_amount = 0
                # for inv in invoice_ser.data:
                #         total_amount += float(inv['grand_total'])

                context[current_time.strftime('%Y-%m-%d')] = invoice_ser.data
                
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "week":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_weeks = int((((interval.days*1440 + interval.seconds/60)/60)/24)/7)

            if total_weeks > 0:
                for week in range(0, total_weeks+1):
                    start_time += timedelta(weeks=week)
                    current_week = start_time + timedelta(weeks=week+1)

                    if current_week > end_time:
                        current_week = end_time

                    invoices = CreditNote.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)\
                                                .filter(status="Pending")\
                                                .order_by("date_created")
                    invoice_ser = CreditNoteSerailizer(invoices, many=True)
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    context[key] = invoice_ser.data                        
                
                return Response(context, status=status.HTTP_200_OK)

            else:
                invoices = CreditNote.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(status="Pending")\
                            .order_by("date_created")

                if len(invoices) > 0:
                    invoice_ser = CreditNoteSerailizer(invoices, many=True)
                    key = f"{start_date} - {end_date}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    # context[key] = total_amount
                    context[key] = invoice_ser.data

                    return Response(context, status=status.HTTP_200_OK)

                else:
                    context["message"] = "No pending credit note within this date range"
                    return Response(context, status=status.HTTP_404_NOT_FOUND)
            
            # return Response(context, status=status.HTTP_200_OK)
        
        elif how == "months":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_months = int(((((interval.days*1440 + interval.seconds/60)/60)/24)/7)/4)

            if total_months > 0:
                for week in range(0, total_months+1):
                    start_time += timedelta(weeks=week*4)
                    current_week = start_time + timedelta(weeks=(week+1)*4)

                    if current_week > end_time:
                        current_week = end_time

                    invoices = CreditNote.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)\
                                                .filter(status="Pending")\
                                                .order_by("date_created")

                    invoice_ser = CreditNoteSerailizer(invoices, many=True)
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"
                    # key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    # context[key] = total_amount
                    context[key] = invoice_ser.data
                return Response(context, status=status.HTTP_200_OK)

            else:
                invoices = CreditNote.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(status="Pending")\
                            .order_by("date_created")

                if len(invoices) > 0:
                    invoice_ser = CreditNoteSerailizer(invoices, many=True)
                    key = f"{start_date} - {end_date}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    # context[key] = total_amount
                    context[key] = invoice_ser.data

                    return Response(context, status=status.HTTP_200_OK)

                else:
                    context["message"] = "No pending credit note within this date range"
                    return Response(context, status=status.HTTP_404_NOT_FOUND)
            
            # return Response(context, status=status.HTTP_200_OK)
        

        elif how == "custom date":
            invoices = CreditNote.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(status="Pending")\
                            .order_by("date_created")

            if len(invoices) > 0:
                invoice_ser = CreditNoteSerailizer(invoices, many=True)
                key = f"{start_date} - {end_date}"

                # total_amount = 0
                # for inv in invoice_ser.data:
                #         total_amount += float(inv['grand_total'])

                # context[key] = total_amount
                context[key] = invoice_ser.data

                return Response(context, status=status.HTTP_200_OK)

            else:
                context["message"] = "No pending credit note within this date range"
                return Response(context, status=status.HTTP_404_NOT_FOUND)






@api_view(["GET"])
@authentication_classes((MyAuthentication, ))
@permission_classes((IsAuthenticated, ))
def delivery_report(request):
    context = {}
    measure = request.query_params.get("measure", None)
    start_date = request.query_params.get("start", None)
    end_date = request.query_params.get("end", None)

    # 9.1
    if measure == "delivery search":
        invoices = DeliveryNote.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date).all().order_by("date_created")
        if len(invoices) > 0:
            invoice_ser = DNSerailizer(invoices, many=True)
            context['message'] = invoice_ser.data

            return Response(context, status=status.HTTP_200_OK)

        else:
            context["message"] = "No delivery notes were created within this date range"
            return Response(context, status=status.HTTP_404_NOT_FOUND)
    
    # # 9.2
    # elif measure == "amount search":
    #     invoices = DeliveryNote.objects.filter(vendor=request.user.id)\
    #                         .filter(date_created__gte=start_date)\
    #                         .filter(date_created__lte=end_date).all().order_by("date_created")

    #     if len(invoices) > 0:
    #         invoice_ser = DNSerailizer(invoices, many=True)
    #         context['message'] = invoice_ser.data

    #         return Response(context, status=status.HTTP_200_OK)

    #     else:
    #         context["message"] = "No invoices were created within this date range"
    #         return Response(context, status=status.HTTP_404_NOT_FOUND)
    

    # 9.2
    elif measure == "per customer":
        invoices = DeliveryNote.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date).all().order_by("date_created")

        if len(invoices) > 0:
            invoice_ser = DNSerailizer(invoices, many=True)
            total_data = {}
            for inv in invoice_ser.data:
                full_name = inv['customer']['first_name'] + " " + inv['customer']['last_name']
                if full_name in total_data:
                    total_data[full_name] += float(inv['grand_total'])
                else:
                    total_data[full_name] = 0
            
            final_data = []
            for k,v in total_data.items():
                final_data.append({"full_name": k, "total_amount": v})

            context['message'] = final_data


            return Response(context, status=status.HTTP_200_OK)

        else:
            context["message"] = "No delivery notes were created within this date range"
            return Response(context, status=status.HTTP_404_NOT_FOUND)
    
    # # 9.4
    # elif measure == "total per date":
    #     context = {}
    #     how = request.query_params.get("how")

    #     if how == "hour":
    #         start_time = datetime.strptime(start_date, "%Y-%m-%d")
    #         end_time = datetime.strptime(end_date, "%Y-%m-%d")

    #         interval = (end_time - start_time)
    #         total_hours = int((interval.days*1440 + interval.seconds/60)/60)

    #         # total_data = {}
    #         for hour in range(0, total_hours+1):
    #             current_time = start_time + timedelta(hours=hour)
    #             invoices = DeliveryNote.objects.filter(date_created__date=current_time.date())\
    #                                       .filter(date_created__hour=current_time.hour)
    #             invoice_ser = DNSerailizer(invoices, many=True)

    #             # for inv in invoice_ser.data:
    #             total_amount = 0
    #             for inv in invoice_ser.data:
    #                     total_amount += float(inv['grand_total'])

    #             context[current_time.strftime('%Y-%m-%d %I%p')] = total_amount
            
    #         return Response(context, status=status.HTTP_200_OK)
        
    #     elif how == "day":
    #         start_time = datetime.strptime(start_date, "%Y-%m-%d")
    #         end_time = datetime.strptime(end_date, "%Y-%m-%d")

    #         interval = (end_time - start_time)
    #         total_days = int(((interval.days*1440 + interval.seconds/60)/60)/24)

    #         # total_data = {}
    #         for day in range(0, total_days+1):
    #             current_time = start_time + timedelta(days=day)
    #             invoices = DeliveryNote.objects.filter(date_created__date=current_time.date())

    #             invoice_ser = DNSerailizer(invoices, many=True)

    #             total_amount = 0
    #             for inv in invoice_ser.data:
    #                     total_amount += float(inv['grand_total'])

    #             context[current_time.strftime('%Y-%m-%d')] = total_amount
                
    #         return Response(context, status=status.HTTP_200_OK)
        
    #     elif how == "week":
    #         start_time = datetime.strptime(start_date, "%Y-%m-%d")
    #         end_time = datetime.strptime(end_date, "%Y-%m-%d")

    #         interval = (end_time - start_time)
    #         total_weeks = int((((interval.days*1440 + interval.seconds/60)/60)/24)/7)

    #         if total_weeks > 0:
    #             for week in range(0, total_weeks+1):
    #                 start_time += timedelta(weeks=week)
    #                 current_week = start_time + timedelta(weeks=week+1)

    #                 if current_week > end_time:
    #                     current_week = end_time

    #                 invoices = DeliveryNote.objects.filter(date_created__gte=start_time)\
    #                                             .filter(date_created__lte=current_week)
    #                 invoice_ser = DNSerailizer(invoices, many=True)
    #                 key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"

    #                 total_amount = 0
    #                 for inv in invoice_ser.data:
    #                         total_amount += float(inv['grand_total'])

    #                 context[key] = total_amount
                        
    #                 # context[key] = invoice_ser.data
                
    #             return Response(context, status=status.HTTP_200_OK)

    #         else:
    #             invoices = DeliveryNote.objects.filter(vendor=request.user.id)\
    #                         .filter(date_created__gte=start_date)\
    #                         .filter(date_created__lte=end_date).all().order_by("date_created")

    #             if len(invoices) > 0:
    #                 invoice_ser = DNSerailizer(invoices, many=True)
    #                 key = f"{start_date} - {end_date}"

    #                 total_amount = 0
    #                 for inv in invoice_ser.data:
    #                         total_amount += float(inv['grand_total'])

    #                 context[key] = total_amount
    #                     # context['message'] = invoice_ser.data

    #                 return Response(context, status=status.HTTP_200_OK)

    #             else:
    #                 context["message"] = "No delivery notes were created within this date range"
    #                 return Response(context, status=status.HTTP_404_NOT_FOUND)
            
    #         # return Response(context, status=status.HTTP_200_OK)
        
    #     elif how == "months":
    #         start_time = datetime.strptime(start_date, "%Y-%m-%d")
    #         end_time = datetime.strptime(end_date, "%Y-%m-%d")

    #         interval = (end_time - start_time)
    #         total_months = int(((((interval.days*1440 + interval.seconds/60)/60)/24)/7)/4)

    #         if total_months > 0:
    #             for week in range(0, total_months+1):
    #                 start_time += timedelta(weeks=week*4)
    #                 current_week = start_time + timedelta(weeks=(week+1)*4)

    #                 if current_week > end_time:
    #                     current_week = end_time

    #                 invoices = DeliveryNote.objects.filter(date_created__gte=start_time)\
    #                                             .filter(date_created__lte=current_week)
    #                 invoice_ser = DNSerailizer(invoices, many=True)
    #                 key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"
    #                 # key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"

    #                 total_amount = 0
    #                 for inv in invoice_ser.data:
    #                         total_amount += float(inv['grand_total'])

    #                 context[key] = total_amount
    #                 # context[key] = invoice_ser.data
    #             return Response(context, status=status.HTTP_200_OK)

    #         else:
    #             invoices = DeliveryNote.objects.filter(vendor=request.user.id)\
    #                         .filter(date_created__gte=start_date)\
    #                         .filter(date_created__lte=end_date).all().order_by("date_created")

    #             if len(invoices) > 0:
    #                 invoice_ser = DNSerailizer(invoices, many=True)
    #                 key = f"{start_date} - {end_date}"

    #                 total_amount = 0
    #                 for inv in invoice_ser.data:
    #                         total_amount += float(inv['grand_total'])

    #                 context[key] = total_amount
    #                 # context['message'] = invoice_ser.data

    #                 return Response(context, status=status.HTTP_200_OK)

    #             else:
    #                 context["message"] = "No delivery notes were created within this date range"
    #                 return Response(context, status=status.HTTP_404_NOT_FOUND)
            
    #         # return Response(context, status=status.HTTP_200_OK)
        

    #     elif how == "custom date":
    #         invoices = DeliveryNote.objects.filter(vendor=request.user.id)\
    #                         .filter(date_created__gte=start_date)\
    #                         .filter(date_created__lte=end_date).all().order_by("date_created")

    #         if len(invoices) > 0:
    #             invoice_ser = DNSerailizer(invoices, many=True)
    #             key = f"{start_date} - {end_date}"

    #             total_amount = 0
    #             for inv in invoice_ser.data:
    #                     total_amount += float(inv['grand_total'])

    #             context[key] = total_amount
    #             # context['message'] = invoice_ser.data

    #             return Response(context, status=status.HTTP_200_OK)

    #         else:
    #             context["message"] = "No delivery notes were created within this date range"
    #             return Response(context, status=status.HTTP_404_NOT_FOUND)


    
    # 9.3
    elif measure == "count delivery email":
        context = {}
        how = request.query_params.get("how")

        if how == "hour":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_hours = int((interval.days*1440 + interval.seconds/60)/60)

            
            for hour in range(0, total_hours+1):
                current_time = start_time + timedelta(hours=hour)
                emailed_count = DeliveryNote.objects.filter(date_created__date=current_time.date())\
                                          .filter(date_created__hour=current_time.hour)\
                                            .filter(emailed=True).count()
                
                context[current_time.strftime('%Y-%m-%d %I%p')] = emailed_count
                

            
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "day":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_days = int(((interval.days*1440 + interval.seconds/60)/60)/24)

            
            for day in range(0, total_days+1):
                current_time = start_time + timedelta(days=day)
                
                emailed_count = DeliveryNote.objects.filter(date_created__date=current_time.date())\
                                            .filter(emailed=True).count()
                
                context[current_time.strftime('%Y-%m-%d')] = emailed_count

                

                
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "week":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_weeks = int((((interval.days*1440 + interval.seconds/60)/60)/24)/7)

            if total_weeks > 0:
                for week in range(0, total_weeks+1):
                    start_time += timedelta(weeks=week)
                    current_week = start_time + timedelta(weeks=week+1)

                    if current_week > end_time:
                        current_week = end_time

                    emailed_count = DeliveryNote.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)\
                                                .filter(emailed=True).count()
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"
                    context[key] = emailed_count
                            
                    
                
                return Response(context, status=status.HTTP_200_OK)

            else:
                emailed_count = DeliveryNote.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(emailed=True)\
                            .count()

                key = f"{start_date} - {end_date}"
                context[key] = emailed_count
                return Response(context, status=status.HTTP_200_OK)
                
        
        elif how == "months":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_months = int(((((interval.days*1440 + interval.seconds/60)/60)/24)/7)/4)

            if total_months > 0:
                for week in range(0, total_months+1):
                    start_time += timedelta(weeks=week*4)
                    current_week = start_time + timedelta(weeks=(week+1)*4)

                    if current_week > end_time:
                        current_week = end_time

                    emailed_count = DeliveryNote.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)\
                                                .filter(emailed=True).count()
                    
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"
                    context[key] = emailed_count
                    
                return Response(context, status=status.HTTP_200_OK)

            else:
                emailed_count = DeliveryNote.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(emailed=True).count()

                key = f"{start_date} - {end_date}"
                context[key] = emailed_count
                return Response(context, status=status.HTTP_200_OK)
                
        

        elif how == "custom date":
            emailed_count = DeliveryNote.objects.filter(vendor=request.user.id)\
                                .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(emailed=True).count()
                
            key = f"{start_date} - {end_date}"
            context[key] = emailed_count
            return Response(context, status=status.HTTP_200_OK)
    

    # 9.4
    elif measure == "detail delivery email":
        context = {}
        how = request.query_params.get("how")

        if how == "hour":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_hours = int((interval.days*1440 + interval.seconds/60)/60)

            # total_data = {}
            for hour in range(0, total_hours+1):
                current_time = start_time + timedelta(hours=hour)
                invoices = DeliveryNote.objects.filter(date_created__date=current_time.date())\
                                          .filter(date_created__hour=current_time.hour)\
                                              .filter(emailed=True)
                invoice_ser = DNSerailizer(invoices, many=True)

                # context['message'] = invoice_ser.data
                context[current_time.strftime('%Y-%m-%d %I%p')] = invoice_ser.data

                # # for inv in invoice_ser.data:
                # total_amount = 0
                # for inv in invoice_ser.data:
                #         total_amount += float(inv['grand_total'])

            
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "day":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_days = int(((interval.days*1440 + interval.seconds/60)/60)/24)

            # total_data = {}
            for day in range(0, total_days+1):
                current_time = start_time + timedelta(days=day)
                invoices = DeliveryNote.objects.filter(date_created__date=current_time.date())\
                                            .filter(emailed=True)

                invoice_ser = DNSerailizer(invoices, many=True)

                # total_amount = 0
                # for inv in invoice_ser.data:
                #         total_amount += float(inv['grand_total'])

                context[current_time.strftime('%Y-%m-%d')] = invoice_ser.data
                
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "week":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_weeks = int((((interval.days*1440 + interval.seconds/60)/60)/24)/7)

            if total_weeks > 0:
                for week in range(0, total_weeks+1):
                    start_time += timedelta(weeks=week)
                    current_week = start_time + timedelta(weeks=week+1)

                    if current_week > end_time:
                        current_week = end_time

                    invoices = DeliveryNote.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)\
                                                .filter(emailed=True)
                    invoice_ser = DNSerailizer(invoices, many=True)
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    context[key] = invoice_ser.data                        
                
                return Response(context, status=status.HTTP_200_OK)

            else:
                invoices = DeliveryNote.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(emailed=True)\
                            .order_by("date_created")

                if len(invoices) > 0:
                    invoice_ser = DNSerailizer(invoices, many=True)
                    key = f"{start_date} - {end_date}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    # context[key] = total_amount
                    context[key] = invoice_ser.data

                    return Response(context, status=status.HTTP_200_OK)

                else:
                    context["message"] = "No emailed delivery note within this date range"
                    return Response(context, status=status.HTTP_404_NOT_FOUND)
            
            # return Response(context, status=status.HTTP_200_OK)
        
        elif how == "months":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_months = int(((((interval.days*1440 + interval.seconds/60)/60)/24)/7)/4)

            if total_months > 0:
                for week in range(0, total_months+1):
                    start_time += timedelta(weeks=week*4)
                    current_week = start_time + timedelta(weeks=(week+1)*4)

                    if current_week > end_time:
                            current_week = end_time

                    invoices = DeliveryNote.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)\
                                                .filter(emailed=True)\
                                                .order_by("date_created")

                    invoice_ser = DNSerailizer(invoices, many=True)
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"
                    # key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    # context[key] = total_amount
                    context[key] = invoice_ser.data
                return Response(context, status=status.HTTP_200_OK)

            else:
                invoices = DeliveryNote.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(emailed=True)\
                            .order_by("date_created")

                if len(invoices) > 0:
                    invoice_ser = DNSerailizer(invoices, many=True)
                    key = f"{start_date} - {end_date}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    # context[key] = total_amount
                    context[key] = invoice_ser.data

                    return Response(context, status=status.HTTP_200_OK)

                else:
                    context["message"] = "No emailed delivery note within this date range"
                    return Response(context, status=status.HTTP_404_NOT_FOUND)
            
            # return Response(context, status=status.HTTP_200_OK)
        

        elif how == "custom date":
            invoices = DeliveryNote.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(emailed=True)\
                            .order_by("date_created")

            if len(invoices) > 0:
                invoice_ser = DNSerailizer(invoices, many=True)
                key = f"{start_date} - {end_date}"

                # total_amount = 0
                # for inv in invoice_ser.data:
                #         total_amount += float(inv['grand_total'])

                # context[key] = total_amount
                context[key] = invoice_ser.data

                return Response(context, status=status.HTTP_200_OK)

            else:
                context["message"] = "No emailed delivery note within this date range"
                return Response(context, status=status.HTTP_404_NOT_FOUND)


    

    # 9.5
    elif measure == "count delivery overdue":

        context = {}
        how = request.query_params.get("how")

        if how == "hour":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_hours = int((interval.days*1440 + interval.seconds/60)/60)

            
            for hour in range(0, total_hours+1):
                current_time = start_time + timedelta(hours=hour)
                overdue_count = DeliveryNote.objects.filter(date_created__date=current_time.date())\
                                          .filter(date_created__hour=current_time.hour)\
                                            .filter(status="Overdue").count()
                
                context[current_time.strftime('%Y-%m-%d %I%p')] = overdue_count
                

            
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "day":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_days = int(((interval.days*1440 + interval.seconds/60)/60)/24)

            
            for day in range(0, total_days+1):
                current_time = start_time + timedelta(days=day)
                
                overdue_count = DeliveryNote.objects.filter(date_created__date=current_time.date())\
                                            .filter(status="Overdue").count()
                
                context[current_time.strftime('%Y-%m-%d')] = overdue_count

                

                
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "week":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_weeks = int((((interval.days*1440 + interval.seconds/60)/60)/24)/7)

            if total_weeks > 0:
                for week in range(0, total_weeks+1):
                    start_time += timedelta(weeks=week)
                    current_week = start_time + timedelta(weeks=week+1)

                    if current_week > end_time:
                        current_week = end_time

                    overdue_count = DeliveryNote.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)\
                                                .filter(status="Overdue").count()
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"
                    context[key] = overdue_count
                            
                    
                
                return Response(context, status=status.HTTP_200_OK)

            else:
                overdue_count = DeliveryNote.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(status="Overdue")\
                            .count()

                key = f"{start_date} - {end_date}"
                context[key] = overdue_count
                return Response(context, status=status.HTTP_200_OK)
                
        
        elif how == "months":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_months = int(((((interval.days*1440 + interval.seconds/60)/60)/24)/7)/4)

            if total_months > 0:
                for week in range(0, total_months+1):
                    start_time += timedelta(weeks=week*4)
                    current_week = start_time + timedelta(weeks=(week+1)*4)

                    if current_week > end_time:
                        current_week = end_time

                    overdue_count = DeliveryNote.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)\
                                                .filter(status="Overdue").count()
                    
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"
                    context[key] = overdue_count
                    
                return Response(context, status=status.HTTP_200_OK)

            else:
                overdue_count = DeliveryNote.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(status="Overdue").count()

                key = f"{start_date} - {end_date}"
                context[key] = overdue_count
                return Response(context, status=status.HTTP_200_OK)
                
        

        elif how == "custom date":
            overdue_count = DeliveryNote.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                                .filter(date_created__lte=end_date)\
                            .filter(status="Overdue").count()
                
            key = f"{start_date} - {end_date}"
            context[key] = overdue_count
            return Response(context, status=status.HTTP_200_OK)

    # 9.6
    elif measure == "detail delivery overdue":
        context = {}
        how = request.query_params.get("how")

        if how == "hour":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_hours = int((interval.days*1440 + interval.seconds/60)/60)

            # total_data = {}
            for hour in range(0, total_hours+1):
                current_time = start_time + timedelta(hours=hour)
                invoices = DeliveryNote.objects.filter(date_created__date=current_time.date())\
                                          .filter(date_created__hour=current_time.hour)\
                                          .filter(status="Overdue")\
                                            .order_by("date_created")
                invoice_ser = DNSerailizer(invoices, many=True)

                # context['message'] = invoice_ser.data
                context[current_time.strftime('%Y-%m-%d %I%p')] = invoice_ser.data

                # # for inv in invoice_ser.data:
                # total_amount = 0
                # for inv in invoice_ser.data:
                #         total_amount += float(inv['grand_total'])

            
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "day":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_days = int(((interval.days*1440 + interval.seconds/60)/60)/24)

            # total_data = {}
            for day in range(0, total_days+1):
                current_time = start_time + timedelta(days=day)
                invoices = DeliveryNote.objects.filter(date_created__date=current_time.date())\
                                            .filter(status="Overdue")\
                                            .order_by("date_created")

                invoice_ser = DNSerailizer(invoices, many=True)

                # total_amount = 0
                # for inv in invoice_ser.data:
                #         total_amount += float(inv['grand_total'])

                context[current_time.strftime('%Y-%m-%d')] = invoice_ser.data
                
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "week":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_weeks = int((((interval.days*1440 + interval.seconds/60)/60)/24)/7)

            if total_weeks > 0:
                for week in range(0, total_weeks+1):
                    start_time += timedelta(weeks=week)
                    current_week = start_time + timedelta(weeks=week+1)

                    if current_week > end_time:
                        current_week = end_time

                    invoices = DeliveryNote.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)\
                                                .filter(status="Overdue")\
                                                .order_by("date_created")
                    invoice_ser = DNSerailizer(invoices, many=True)
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    context[key] = invoice_ser.data                        
                
                return Response(context, status=status.HTTP_200_OK)

            else:
                invoices = DeliveryNote.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(status="Overdue")\
                            .order_by("date_created")

                if len(invoices) > 0:
                    invoice_ser = DNSerailizer(invoices, many=True)
                    key = f"{start_date} - {end_date}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    # context[key] = total_amount
                    context[key] = invoice_ser.data

                    return Response(context, status=status.HTTP_200_OK)

                else:
                    context["message"] = "No overdue delivery note within this date range"
                    return Response(context, status=status.HTTP_404_NOT_FOUND)
            
            # return Response(context, status=status.HTTP_200_OK)
        
        elif how == "months":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_months = int(((((interval.days*1440 + interval.seconds/60)/60)/24)/7)/4)

            if total_months > 0:
                for week in range(0, total_months+1):
                    start_time += timedelta(weeks=week*4)
                    current_week = start_time + timedelta(weeks=(week+1)*4)

                    if current_week > end_time:
                        current_week = end_time

                    invoices = DeliveryNote.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)\
                                                .filter(status="Overdue")\
                                                .order_by("date_created")

                    invoice_ser = DNSerailizer(invoices, many=True)
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"
                    # key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    # context[key] = total_amount
                    context[key] = invoice_ser.data
                return Response(context, status=status.HTTP_200_OK)

            else:
                invoices = DeliveryNote.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(status="Overdue")\
                            .order_by("date_created")

                if len(invoices) > 0:
                    invoice_ser = DNSerailizer(invoices, many=True)
                    key = f"{start_date} - {end_date}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    # context[key] = total_amount
                    context[key] = invoice_ser.data

                    return Response(context, status=status.HTTP_200_OK)

                else:
                    context["message"] = "No overdue delivery note within this date range"
                    return Response(context, status=status.HTTP_404_NOT_FOUND)
            
            # return Response(context, status=status.HTTP_200_OK)
        

        elif how == "custom date":
            invoices = DeliveryNote.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(status="Overdue")\
                            .order_by("date_created")

            if len(invoices) > 0:
                invoice_ser = DNSerailizer(invoices, many=True)
                key = f"{start_date} - {end_date}"

                # total_amount = 0
                # for inv in invoice_ser.data:
                #         total_amount += float(inv['grand_total'])

                # context[key] = total_amount
                context[key] = invoice_ser.data

                return Response(context, status=status.HTTP_200_OK)

            else:
                context["message"] = "No overdue delivery note within this date range"
                return Response(context, status=status.HTTP_404_NOT_FOUND)
    

    # 9.7
    elif measure == "detail delivery pending":
        context = {}
        how = request.query_params.get("how")

        if how == "hour":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_hours = int((interval.days*1440 + interval.seconds/60)/60)

            # total_data = {}
            for hour in range(0, total_hours+1):
                current_time = start_time + timedelta(hours=hour)
                invoices = DeliveryNote.objects.filter(date_created__date=current_time.date())\
                                          .filter(date_created__hour=current_time.hour)\
                                          .filter(status="Pending")\
                                            .order_by("date_created")
                invoice_ser = DNSerailizer(invoices, many=True)

                # context['message'] = invoice_ser.data
                context[current_time.strftime('%Y-%m-%d %I%p')] = invoice_ser.data

                # # for inv in invoice_ser.data:
                # total_amount = 0
                # for inv in invoice_ser.data:
                #         total_amount += float(inv['grand_total'])

            
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "day":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_days = int(((interval.days*1440 + interval.seconds/60)/60)/24)

            # total_data = {}
            for day in range(0, total_days+1):
                current_time = start_time + timedelta(days=day)
                invoices = DeliveryNote.objects.filter(date_created__date=current_time.date())\
                                            .filter(status="Pending")\
                                            .order_by("date_created")

                invoice_ser = DNSerailizer(invoices, many=True)

                # total_amount = 0
                # for inv in invoice_ser.data:
                #         total_amount += float(inv['grand_total'])

                context[current_time.strftime('%Y-%m-%d')] = invoice_ser.data
                
            return Response(context, status=status.HTTP_200_OK)
        
        elif how == "week":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_weeks = int((((interval.days*1440 + interval.seconds/60)/60)/24)/7)

            if total_weeks > 0:
                for week in range(0, total_weeks+1):
                    start_time += timedelta(weeks=week)
                    current_week = start_time + timedelta(weeks=week+1)

                    if current_week > end_time:
                        current_week = end_time

                    invoices = DeliveryNote.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)\
                                                .filter(status="Pending")\
                                                .order_by("date_created")
                    invoice_ser = DNSerailizer(invoices, many=True)
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    context[key] = invoice_ser.data                        
                
                return Response(context, status=status.HTTP_200_OK)

            else:
                invoices = DeliveryNote.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(status="Pending")\
                            .order_by("date_created")

                if len(invoices) > 0:
                    invoice_ser = DNSerailizer(invoices, many=True)
                    key = f"{start_date} - {end_date}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    # context[key] = total_amount
                    context[key] = invoice_ser.data

                    return Response(context, status=status.HTTP_200_OK)

                else:
                    context["message"] = "No pending delivery note within this date range"
                    return Response(context, status=status.HTTP_404_NOT_FOUND)
            
            # return Response(context, status=status.HTTP_200_OK)
        
        elif how == "months":
            start_time = datetime.strptime(start_date, "%Y-%m-%d")
            end_time = datetime.strptime(end_date, "%Y-%m-%d")

            interval = (end_time - start_time)
            total_months = int(((((interval.days*1440 + interval.seconds/60)/60)/24)/7)/4)

            if total_months > 0:
                for week in range(0, total_months+1):
                    start_time += timedelta(weeks=week*4)
                    current_week = start_time + timedelta(weeks=(week+1)*4)

                    if current_week > end_time:
                        current_week = end_time

                    invoices = DeliveryNote.objects.filter(date_created__gte=start_time)\
                                                .filter(date_created__lte=current_week)\
                                                .filter(status="Pending")\
                                                .order_by("date_created")

                    invoice_ser = DNSerailizer(invoices, many=True)
                    key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"
                    # key = f"{start_time.strftime('%Y-%m-%d')} - {current_week.strftime('%Y-%m-%d')}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    # context[key] = total_amount
                    context[key] = invoice_ser.data
                return Response(context, status=status.HTTP_200_OK)

            else:
                invoices = DeliveryNote.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(status="Pending")\
                            .order_by("date_created")

                if len(invoices) > 0:
                    invoice_ser = DNSerailizer(invoices, many=True)
                    key = f"{start_date} - {end_date}"

                    # total_amount = 0
                    # for inv in invoice_ser.data:
                    #         total_amount += float(inv['grand_total'])

                    # context[key] = total_amount
                    context[key] = invoice_ser.data

                    return Response(context, status=status.HTTP_200_OK)

                else:
                    context["message"] = "No pending delivery note within this date range"
                    return Response(context, status=status.HTTP_404_NOT_FOUND)
            
            # return Response(context, status=status.HTTP_200_OK)
        

        elif how == "custom date":
            invoices = DeliveryNote.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(status="Pending")\
                            .order_by("date_created")

            if len(invoices) > 0:
                invoice_ser = DNSerailizer(invoices, many=True)
                key = f"{start_date} - {end_date}"

                # total_amount = 0
                # for inv in invoice_ser.data:
                #         total_amount += float(inv['grand_total'])

                # context[key] = total_amount
                context[key] = invoice_ser.data

                return Response(context, status=status.HTTP_200_OK)

            else:
                context["message"] = "No pending delivery note within this date range"
                return Response(context, status=status.HTTP_404_NOT_FOUND)








@api_view(["GET"])
@authentication_classes((MyAuthentication, ))
@permission_classes((IsAuthenticated, ))
def item_report(request):
    context = {}

    measure = request.query_params.get("measure", None)
    start_date = request.query_params.get("start", None)
    end_date = request.query_params.get("end", None)


    # 10.1
    if measure == "item search":
        items = Item.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date).all().order_by("date_created")
        
        if len(items) > 0:
            item_ser = ItemSerializer(items, many=True)

            context['message'] = item_ser.data
            
            return Response(context, status=status.HTTP_200_OK)
        else:
            context["message"] = "No items were created within this date range"
            return Response(context, status=status.HTTP_404_NOT_FOUND)



    # 10.2
    elif measure == "sales price search":

        items = Item.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .order_by("sales_price")\
                            .order_by("date_created")
        if len(items) > 0:
            item_ser = ItemSerializer(items, many=True)
            context['message'] = item_ser.data
            return Response(context, status=status.HTTP_200_OK)

        else:
            context["message"] = "No items matched the given parameters"
            return Response(context, status=status.HTTP_404_NOT_FOUND)

    
    # 10.3
    elif measure == "item search name":

        items = Item.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .order_by("name")
        if len(items) > 0:
            item_ser = ItemSerializer(items, many=True)
            context['message'] = item_ser.data
            return Response(context, status=status.HTTP_200_OK)

        else:
            context["message"] = "No items matched the given parameters"
            return Response(context, status=status.HTTP_404_NOT_FOUND)
    

    # 10.4
    elif measure == "items total":
        items_count = Item.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date).all().order_by("date_created").count()
        context["message"] = items_count
        return Response(context, status=status.HTTP_200_OK)



    # 10.5
    elif measure == "sales price range":
        upper_price = request.query_params.get("upper_price")
        lower_price = request.query_params.get("lower_price")

        items = Item.objects.filter(vendor=request.user.id)\
                            .filter(date_created__gte=start_date)\
                            .filter(date_created__lte=end_date)\
                            .filter(sales_price__gte=lower_price)\
                            .filter(sales_price__lte=upper_price)\
                            .order_by("date_created")
        if len(items) > 0:
            item_ser = ItemSerializer(items, many=True)
            context['message'] = item_ser.data
            return Response(context, status=status.HTTP_200_OK)

        else:
            context["message"] = "No items matched the given parameters"
            return Response(context, status=status.HTTP_404_NOT_FOUND)



    return Response(context, status=status.HTTP_200_OK)










@api_view(["GET"])
@authentication_classes((MyAuthentication, ))
@permission_classes((IsAuthenticated, ))
def dashboard(request):

    how = request.query_params.get("how", None)

    context = {}

    # stats

    # invoice
    context["new_invoice"] = Invoice.objects.filter(status="New")\
                                            .filter(vendor=request.user.id)\
                                            .count()
    context["unpaid_invoice"] = Invoice.objects.filter(status="Unpaid")\
                                            .filter(vendor=request.user.id)\
                                            .count()
    context["paid_invoice"] = Invoice.objects.filter(status="Paid")\
                                            .filter(vendor=request.user.id)\
                                            .count()
    context["emailed_invoice"] = Invoice.objects.filter(emailed=True)\
                                            .filter(vendor=request.user.id)\
                                            .count()
    context["overdue_invoice"] = Invoice.objects.filter(status="Overdue")\
                                            .filter(vendor=request.user.id)\
                                            .count()


    # proforma
    context["new_proforma"] = ProformaInvoice.objects.filter(status="New")\
                                            .filter(vendor=request.user.id)\
                                            .count()
    context["unpaid_proforma"] = ProformaInvoice.objects.filter(status="Unpaid")\
                                            .filter(vendor=request.user.id)\
                                            .count()
    context["paid_proforma"] = ProformaInvoice.objects.filter(status="Paid")\
                                            .filter(vendor=request.user.id)\
                                            .count()
    context["emailed_proforma"] = ProformaInvoice.objects.filter(emailed=True)\
                                            .filter(vendor=request.user.id)\
                                            .count()
    context["overdue_proforma"] = ProformaInvoice.objects.filter(status="Overdue")\
                                            .filter(vendor=request.user.id)\
                                            .count()


    # purchase
    context["new_purchase"] = PurchaseOrder.objects.filter(status="New")\
                                            .filter(vendor=request.user.id)\
                                            .count()
    context["unpaid_purchase"] = PurchaseOrder.objects.filter(status="Unpaid")\
                                            .filter(vendor=request.user.id)\
                                            .count()
    context["paid_purchase"] = PurchaseOrder.objects.filter(status="Paid")\
                                            .filter(vendor=request.user.id)\
                                            .count()
    context["emailed_purchase"] = PurchaseOrder.objects.filter(emailed=True)\
                                            .filter(vendor=request.user.id)\
                                            .count()
    context["overdue_purchase"] = PurchaseOrder.objects.filter(status="Overdue")\
                                            .filter(vendor=request.user.id)\
                                            .count()


    # estimate
    context["new_estimate"] = Estimate.objects.filter(status="New")\
                                            .filter(vendor=request.user.id)\
                                            .count()
    context["unpaid_estimate"] = Estimate.objects.filter(status="Unpaid")\
                                            .filter(vendor=request.user.id)\
                                            .count()
    context["paid_estimate"] = Estimate.objects.filter(status="Paid")\
                                            .filter(vendor=request.user.id)\
                                            .count()
    context["emailed_estimate"] = Estimate.objects.filter(emailed=True)\
                                            .filter(vendor=request.user.id)\
                                            .count()
    context["overdue_estimate"] = Estimate.objects.filter(status="Overdue")\
                                            .filter(vendor=request.user.id)\
                                            .count()


    # quote
    context["new_quote"] = Quote.objects.filter(status="New")\
                                            .filter(vendor=request.user.id)\
                                            .count()
    context["unpaid_quote"] = Quote.objects.filter(status="Unpaid")\
                                            .filter(vendor=request.user.id)\
                                            .count()
    context["paid_quote"] = Quote.objects.filter(status="Paid")\
                                            .filter(vendor=request.user.id)\
                                            .count()
    context["emailed_quote"] = Quote.objects.filter(emailed=True)\
                                            .filter(vendor=request.user.id)\
                                            .count()
    context["overdue_quote"] = Quote.objects.filter(status="Overdue")\
                                            .filter(vendor=request.user.id)\
                                            .count()


    # receipt
    context["new_receipt"] = Receipt.objects.filter(status="New")\
                                            .filter(vendor=request.user.id)\
                                            .count()
    context["unpaid_receipt"] = Receipt.objects.filter(status="Unpaid")\
                                            .filter(vendor=request.user.id)\
                                            .count()
    context["paid_receipt"] = Receipt.objects.filter(status="Paid")\
                                            .filter(vendor=request.user.id)\
                                            .count()
    context["emailed_receipt"] = Receipt.objects.filter(emailed=True)\
                                            .filter(vendor=request.user.id)\
                                            .count()
    context["overdue_receipt"] = Receipt.objects.filter(status="Overdue")\
                                            .filter(vendor=request.user.id)\
                                            .count()


    # credit
    context["new_credit"] = CreditNote.objects.filter(status="New")\
                                            .filter(vendor=request.user.id)\
                                            .count()
    context["unpaid_credit"] = CreditNote.objects.filter(status="Unpaid")\
                                            .filter(vendor=request.user.id)\
                                            .count()
    context["paid_credit"] = CreditNote.objects.filter(status="Paid")\
                                            .filter(vendor=request.user.id)\
                                            .count()
    context["emailed_credit"] = CreditNote.objects.filter(emailed=True)\
                                            .filter(vendor=request.user.id)\
                                            .count()
    context["overdue_credit"] = CreditNote.objects.filter(status="Overdue")\
                                            .filter(vendor=request.user.id)\
                                            .count()


    # delivery
    context["new_delivery"] = DeliveryNote.objects.filter(status="New")\
                                            .filter(vendor=request.user.id)\
                                            .count()
    context["unpaid_delivery"] = DeliveryNote.objects.filter(status="Unpaid")\
                                            .filter(vendor=request.user.id)\
                                            .count()
    context["paid_delivery"] = DeliveryNote.objects.filter(status="Paid")\
                                            .filter(vendor=request.user.id)\
                                            .count()
    context["emailed_delivery"] = DeliveryNote.objects.filter(emailed=True)\
                                            .filter(vendor=request.user.id)\
                                            .count()
    context["overdue_delivery"] = DeliveryNote.objects.filter(status="Overdue")\
                                            .filter(vendor=request.user.id)\
                                            .count()




    # graph
    how = request.query_params.get("how", "month")    
    
    if how == "week":
        context["week"] = {}
        today_date = datetime.now()
        start_month = datetime.strptime(f"{today_date.year}-{today_date.month}-1", "%Y-%m-%d")
        for week in range(0, 5):
            week_count = 0
            start_week = start_month + timedelta(weeks=week)
            end_week = start_month + timedelta(weeks=week+1)

            week_count += Invoice.objects.filter(vendor=request.user.id)\
                                            .filter(date_created__gte=start_week)\
                                            .filter(date_created__lt=end_week)\
                                            .count()
                                            
            week_count += ProformaInvoice.objects.filter(vendor=request.user.id)\
                                            .filter(date_created__gte=start_week)\
                                            .filter(date_created__lt=end_week)\
                                            .count()
                                            
            week_count += PurchaseOrder.objects.filter(vendor=request.user.id)\
                                            .filter(date_created__gte=start_week)\
                                            .filter(date_created__lt=end_week)\
                                            .count()
                                            
            week_count += Estimate.objects.filter(vendor=request.user.id)\
                                            .filter(date_created__gte=start_week)\
                                            .filter(date_created__lt=end_week)\
                                            .count()
                                            
            week_count += Quote.objects.filter(vendor=request.user.id)\
                                            .filter(date_created__gte=start_week)\
                                            .filter(date_created__lt=end_week)\
                                            .count()
                                            
            week_count += Receipt.objects.filter(vendor=request.user.id)\
                                            .filter(date_created__gte=start_week)\
                                            .filter(date_created__lt=end_week)\
                                            .count()
                                            
            week_count += CreditNote.objects.filter(vendor=request.user.id)\
                                            .filter(date_created__gte=start_week)\
                                            .filter(date_created__lt=end_week)\
                                            .count()
                                            
            week_count += DeliveryNote.objects.filter(vendor=request.user.id)\
                                            .filter(date_created__gte=start_week)\
                                            .filter(date_created__lt=end_week)\
                                            .count()
                                            

            context["month"][f"week {week+1}"] = week_count

    
    elif how == "month":
        context["month"] = {}
        year = datetime.now().year
        for month in range(1, 13):
            month_count = 0
            month_count += Invoice.objects.filter(vendor=request.user.id)\
                                            .filter(date_created__year=year)\
                                            .filter(date_created__month=month)\
                                            .count()

            month_count += ProformaInvoice.objects.filter(vendor=request.user.id)\
                                            .filter(date_created__year=year)\
                                            .filter(date_created__month=month)\
                                            .count()

            month_count += PurchaseOrder.objects.filter(vendor=request.user.id)\
                                            .filter(date_created__year=year)\
                                            .filter(date_created__month=month)\
                                            .count()

            month_count += Estimate.objects.filter(vendor=request.user.id)\
                                            .filter(date_created__year=year)\
                                            .filter(date_created__month=month)\
                                            .count()

            month_count += Quote.objects.filter(vendor=request.user.id)\
                                            .filter(date_created__year=year)\
                                            .filter(date_created__month=month)\
                                            .count()

            month_count += Receipt.objects.filter(vendor=request.user.id)\
                                            .filter(date_created__year=year)\
                                            .filter(date_created__month=month)\
                                            .count()

            month_count += CreditNote.objects.filter(vendor=request.user.id)\
                                            .filter(date_created__year=year)\
                                            .filter(date_created__month=month)\
                                            .count()

            month_count += DeliveryNote.objects.filter(vendor=request.user.id)\
                                            .filter(date_created__year=year)\
                                            .filter(date_created__month=month)\
                                            .count()


            context["month"][month] = month_count
                                        

    elif how == "year":
        context["year"] = {}
        current_year = datetime.now().year
        for year in range(2022, current_year+1):
            year_count = 0
            year_count += Invoice.objects.filter(vendor=request.user.id)\
                                            .filter(date_created__year=year)\
                                            .count()

            year_count += ProformaInvoice.objects.filter(vendor=request.user.id)\
                                            .filter(date_created__year=year)\
                                            .count()

            year_count += PurchaseOrder.objects.filter(vendor=request.user.id)\
                                            .filter(date_created__year=year)\
                                            .count()

            year_count += Estimate.objects.filter(vendor=request.user.id)\
                                            .filter(date_created__year=year)\
                                            .count()

            year_count += Quote.objects.filter(vendor=request.user.id)\
                                            .filter(date_created__year=year)\
                                            .count()

            year_count += Receipt.objects.filter(vendor=request.user.id)\
                                            .filter(date_created__year=year)\
                                            .count()

            year_count += CreditNote.objects.filter(vendor=request.user.id)\
                                            .filter(date_created__year=year)\
                                            .count()

            year_count += DeliveryNote.objects.filter(vendor=request.user.id)\
                                            .filter(date_created__year=year)\
                                            .count()


            context["year"][year] = year_count
        
        



    return Response(context, status=status.HTTP_200_OK)