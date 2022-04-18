#django imports
from django.contrib.auth import authenticate

#rest_frameworf imports
from rest_framework.decorators import api_view, authentication_classes, permission_classes
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
                        PayPurchaseSerializer, ProfileSerializer, PasswordChangeSerializer, PreferenceSerializer, PaymentSerializer,\
                        custom_item_serializer


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
        context["message"] = invoices.data
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
            new_invoice, pdf_file = form.save(request)
            context['message'] = "success"
            context['invoice'] = {"id": new_invoice.id, **form.data}
            # context['invoice']['item_list'] = [{"id": a, "quantity": b} for a,b in zip(new_invoice.iten_list, new_invoice.quantity_list)]
            # context['invoice']['item_list'] = custom_item_serializer(new_invoice.item_list, new_invoice.quantity_list)

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
        try:
            invoice = Invoice.objects.get(id=id)
            form = InvoiceEditSerializer(instance=invoice, data=request.data)
            context = {}

            if form.is_valid():
                updated_invoice = form.update(invoice, form.validated_data)
                context['message'] = "success"
                context['invoice'] = {"id": updated_invoice.id, **form.data}
                # context['invoice']['item_list'] = custom_item_serializer(updated_invoice.item_list, updated_invoice.quantity_list)

                return Response(context, status=status.HTTP_200_OK)

            else:
                errors = {**form.errors}
                new_errors = {key: value[0] for key,value in errors.items()}
                errors_list = [k for k in new_errors.values()]
                context = {'message': errors_list[0], 'errors': new_errors}

                return Response(context, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            print(e)
            context = {'message' :"Invoice not found"}
            return Response(context, status=status.HTTP_404_NOT_FOUND)

    
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
            pay_invoice = form.save()
            if pay_invoice:
                context['message'] = "success"
                context['pay_invoice'] = {"id": pay_invoice.id, **form.data}

                return Response(context, status=status.HTTP_200_OK)
            else:
                context['message'] = "Invalid Invoice ID"
                return Response(context, status=status.HTTP_400_BAD_REQUEST)

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
        context = {"message": invoices.data}
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
            context['invoice']['item_list'] = custom_item_serializer(new_invoice.item_list, new_invoice.quantity_list)

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
                    "invoice_number", "invoice_date", "po_number", "due_date", "notes", "attachment_path", "item_list", 
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
                context['proforma'] = {"id": updated_proforma.id, **form.data}
                context['proforma']['item_list'] = custom_item_serializer(updated_proforma.item_list, updated_proforma.quantity_list)

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
            pay_proforma = form.save()
            if pay_proforma:
                context['message'] = "success"
                context['pay_proforma'] = {"id": pay_proforma.id, **form.data}

                return Response(context, status=status.HTTP_200_OK)
            else:
                context['message'] = "Invalid Proforma ID"
                return Response(context, status=status.HTTP_400_BAD_REQUEST)

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
        context = {"message": pos.data}
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
            context['invoice']['item_list'] = custom_item_serializer(new_po.item_list, new_po.quantity_list)

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
                context['message']['item_list'] = custom_item_serializer(serialized_purchase.item_list, serialized_purchase.quantity_list)
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
                updated_proforma = form.update(purchase, form.validated_data)
                context['message'] = "success"
                context['purchase'] = {"id": updated_proforma.id, **form.data}
                context['purchase']['item_list'] = custom_item_serializer(updated_proforma.item_list, updated_proforma.quantity_list)

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
            pay_purchase = form.save()
            if pay_purchase:
                context['message'] = "success"
                context['pay_purchase'] = {"id": pay_purchase.id, **form.data}

                return Response(context, status=status.HTTP_200_OK)
            else:
                context['message'] = "Invalid Purchase order ID"
                return Response(context, status=status.HTTP_400_BAD_REQUEST)

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
        context = {"message": estimates.data}
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
            context['estimate']['item_list'] = custom_item_serializer(new_estimate.item_list, new_estimate.quantity_list)

            return Response(context, status=status.HTTP_200_OK)

        else:
            errors = {**form.errors}
            new_errors = {key: value[0] for key,value in errors.items()}
            errors_list = [k for k in new_errors.values()]
            context = {'message': errors_list[0], 'errors': new_errors}

            return Response(context, status=status.HTTP_400_BAD_REQUEST)
    else:
        context = {"message": "create estimate page", "required fields": [
                "first_name", "last_name", "address", "email", "phone_number", "taxable", "estimate_pref", "logo_path", 
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
                context['estimate'] = {"id": updated_estimate.id, **form.data}
                context['estimate']['item_list'] = custom_item_serializer(updated_estimate.item_list, updated_estimate.quantity_list)

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
            pay_estimate = form.save()
            if pay_estimate:
                context['message'] = "success"
                context['pay_estimate'] = {"id": pay_estimate.id, **form.data}

                return Response(context, status=status.HTTP_200_OK)
            else:
                context['message'] = "Invalid Estimate ID"
                return Response(context, status=status.HTTP_400_BAD_REQUEST)

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
        context = {"message": quotes.data}
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
            context['quote']['item_list'] = custom_item_serializer(new_quote.item_list, new_quote.quantity_list)

            return Response(context, status=status.HTTP_200_OK)

        else:
            errors = {**form.errors}
            new_errors = {key: value[0] for key,value in errors.items()}
            errors_list = [k for k in new_errors.values()]
            context = {'message': errors_list[0], 'errors': new_errors}

            return Response(context, status=status.HTTP_400_BAD_REQUEST)
    else:
        context = {"message": "create quote page", "required fields": [
                "first_name", "last_name", "address", "email", "phone_number", "taxable", "quote_pref", "logo_path", 
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
                context['quote'] = {"id": updated_quote.id, **form.data}
                context['quote']['item_list'] = custom_item_serializer(updated_quote.item_list, updated_quote.quantity_list)

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
            pay_quote = form.save()
            if pay_quote:
                context['message'] = "success"
                context['pay_quote'] = {"id": pay_quote.id, **form.data}

                return Response(context, status=status.HTTP_200_OK)
            else:
                context['message'] = "Invalid Quote ID"
                return Response(context, status=status.HTTP_400_BAD_REQUEST)

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
        context = {"message": receipts.data}
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
            context['receipt']['item_list'] = custom_item_serializer(new_receipt.item_list, new_receipt.quantity_list)

            return Response(context, status=status.HTTP_200_OK)

        else:
            errors = {**form.errors}
            new_errors = {key: value[0] for key,value in errors.items()}
            errors_list = [k for k in new_errors.values()]
            context = {'message': errors_list[0], 'errors': new_errors}

            return Response(context, status=status.HTTP_400_BAD_REQUEST)
    else:
        context = {"message": "create receipt page", "required fields": [
                "first_name", "last_name", "address", "email", "phone_number", "taxable", "receipt_pref", "logo_path", 
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
                context['receipt'] = {"id": updated_receipt.id, **form.data}
                context['receipt']['item_list'] = custom_item_serializer(updated_receipt.item_list, updated_receipt.quantity_list)

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
            pay_receipt = form.save()
            if pay_receipt:
                context['message'] = "success"
                context['pay_receipt'] = {"id": pay_receipt.id, **form.data}

                return Response(context, status=status.HTTP_200_OK)
            else:
                context['message'] = "Invalid receipt ID"
                return Response(context, status=status.HTTP_400_BAD_REQUEST)

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
        context = {"message": credits.data}
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
            context['credit']['item_list'] = custom_item_serializer(new_credit.item_list, new_credit.quantity_list)

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
                context['credit'] = {"id": updated_credit.id, **form.data}
                context['credit']['item_list'] = custom_item_serializer(updated_credit.item_list, updated_credit.quantity_list)

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
            pay_credit = form.save()
            if pay_credit:
                context['message'] = "success"
                context['pay_credit'] = {"id": pay_credit.id, **form.data}

                return Response(context, status=status.HTTP_200_OK)
            else:
                context['message'] = "Invalid credit ID"
                return Response(context, status=status.HTTP_400_BAD_REQUEST)

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
        context = {"message": deliverys.data}
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
            context['delivery']['item_list'] = custom_item_serializer(new_delivery.item_list, new_delivery.quantity_list)

            return Response(context, status=status.HTTP_200_OK)

        else:
            errors = {**form.errors}
            new_errors = {key: value[0] for key,value in errors.items()}
            errors_list = [k for k in new_errors.values()]
            context = {'message': errors_list[0], 'errors': new_errors}

            return Response(context, status=status.HTTP_400_BAD_REQUEST)
    else:
        context = {"message": "create delivery note page", "required fields": [
                 "first_name", "last_name", "address", "email", "phone_number", "taxable", "dn_pref", "logo_path", 
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
                context['delivery'] = {"id": updated_delivery.id, **form.data}
                context['delivery']['item_list'] = custom_item_serializer(updated_delivery.item_list, updated_delivery.quantity_list)

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
            pay_delivery = form.save()
            if pay_delivery:
                context['message'] = "success"
                context['pay_delivery'] = {"id": pay_delivery.id, **form.data}

                return Response(context, status=status.HTTP_200_OK)
            else:
                context['message'] = "Invalid delivery ID"
                return Response(context, status=status.HTTP_400_BAD_REQUEST)

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
                context['messgae'] = message
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
            result = pref_ser.update(request)

            context['message'] = "Preference Saved successfully"
            context['preference'] = {**pref_ser.validated_data}

            return Response(context, status=status.HTTP_200_OK)

        else:

            errors = {**pref_ser.errors}
            new_errors = {key: value[0] for key,value in errors.items()}
            errors_list = [k for k in new_errors.values()]
            context = {'message': errors_list[0], 'errors': new_errors}

            return Response(context, status=status.HTTP_400_BAD_REQUEST)











@api_view(["GET", "POST"])
@authentication_classes((MyAuthentication, ))
@permission_classes((IsAuthenticated, ))
def change_payment(request):

    my_preference = PaymentSerializer(instance=request.user)


    if request.method == "GET":
            context = {**my_preference.data}
            return Response(context, status=status.HTTP_200_OK)
    

    if request.method == "POST":
        context = {}
        payment_info = PaymentSerializer(instance=my_preference, data=request.data)

        if payment_info.is_valid():
            result = payment_info.update(request)

            context['message'] = "Payment info Saved successfully"
            context['preference'] = {**payment_info.validated_data}

            return Response(context, status=status.HTTP_200_OK)

        else:

            errors = {**payment_info.errors}
            new_errors = {key: value[0] for key,value in errors.items()}
            errors_list = [k for k in new_errors.values()]
            context = {'message': errors_list[0], 'errors': new_errors}

            return Response(context, status=status.HTTP_400_BAD_REQUEST)






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


