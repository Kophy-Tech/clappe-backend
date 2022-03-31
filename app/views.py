#django imports
from django.contrib.auth import authenticate

#rest_frameworf imports
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

#import from custom files
from .serializers import CustomerCreateSerializer, CustomerEditSerializer, CustomerSerializer, EstimateCreateSerializer, EstimateEditSerializer, EstimateSerailizer, InvoiceEditSerializer, \
                        InvoiceSerializer, PayEstimateSerializer, PayInvoiceSerializer, ProformaCreateSerializer, ProformaEditSerializer, \
                        ProformerInvoiceSerailizer, SignUpSerializer, LoginSerializer, UserSerializer, InvoiceCreate,\
                        PayProformaSerializer, PurchaseCreateSerializer, PurchaseEditSerializer, PurchaseOrderSerailizer, \
                        PayPurchaseSerializer


from .authentication import get_access_token, MyAuthentication
from .models import JWT, Customer, Estimate, Invoice, MyUsers, ProformaInvoice, PurchaseOrder





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
            print(serializer.errors)
            errors = {**serializer.errors}
            errors_list = [k[0] for k in errors.values()]
            context = {'message': errors_list[0], 'errors': errors_list}
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
            errors_list = [k[0] for k in errors.values()]
            context = {'message': errors_list[0], 'errors': errors_list}
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
            errors_list = [k[0] for k in errors.values()]
            context = {'message': errors_list[0], 'errors': errors_list}

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
            errors_list = [k[0] for k in errors.values()]
            context = {'message': errors_list[0], 'errors': errors_list}

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
            new_invoice = form.save(request)
            context['message'] = "success"
            context['invoice'] = {"id": new_invoice.id, **form.data}

            return Response(context, status=status.HTTP_200_OK)

        else:
            errors = {**form.errors}
            errors_list = [k[0] for k in errors.values()]
            context = {'message': errors_list[0], 'errors': errors_list}

            return Response(context, status=status.HTTP_400_BAD_REQUEST)
    else:
        context = {"message": "create invoice page", "required fields": [
            "first_name","last_name","address","email","phone_number","taxable","invoice_pref","theme","invoice_number",
            "invoice_date","po_number","due_date","ship_to","shipping_address","bill_to","billing_address","notes","items_json",
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

                return Response(context, status=status.HTTP_200_OK)

            else:
                errors = {**form.errors}
                errors_list = [k[0] for k in errors.values()]
                context = {'message': errors_list[0], 'errors': errors_list}

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
            errors_list = [k[0] for k in errors.values()]
            context = {'message': errors_list[0], 'errors': errors_list}

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

            return Response(context, status=status.HTTP_200_OK)

        else:
            errors = {**form.errors}
            errors_list = [k[0] for k in errors.values()]
            context = {'message': errors_list[0], 'errors': errors_list}

            return Response(context, status=status.HTTP_400_BAD_REQUEST)
    else:
        context = {"message": "create invoice page", "required fields": [
                "first_name", "last_name", "address", "email", "phone_number", "taxable", "invoice_pref", "theme", 
                    "invoice_number", "invoice_date", "po_number", "due_date", "notes", "attachment_path", "items_json", 
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

                return Response(context, status=status.HTTP_200_OK)

            else:
                errors = {**form.errors}
                errors_list = [k[0] for k in errors.values()]
                context = {'message': errors_list[0], 'errors': errors_list}

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
            errors_list = [k[0] for k in errors.values()]
            context = {'message': errors_list[0], 'errors': errors_list}

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

            return Response(context, status=status.HTTP_200_OK)

        else:
            errors = {**form.errors}
            errors_list = [k[0] for k in errors.values()]
            context = {'message': errors_list[0], 'errors': errors_list}

            return Response(context, status=status.HTTP_400_BAD_REQUEST)
    else:
        context = {"message": "create invoice page", "required fields": [
                "first_name", "last_name", "address", "email", "phone_number", "taxable", "po_pref", "theme", 
                    "po_number", "po_date", "ship_to", "notes", "shipping_address", "items_json", 
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

                return Response(context, status=status.HTTP_200_OK)

            else:
                errors = {**form.errors}
                errors_list = [k[0] for k in errors.values()]
                context = {'message': errors_list[0], 'errors': errors_list}

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
            errors_list = [k[0] for k in errors.values()]
            context = {'message': errors_list[0], 'errors': errors_list}

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

            return Response(context, status=status.HTTP_200_OK)

        else:
            errors = {**form.errors}
            errors_list = [k[0] for k in errors.values()]
            context = {'message': errors_list[0], 'errors': errors_list}

            return Response(context, status=status.HTTP_400_BAD_REQUEST)
    else:
        context = {"message": "create invoice page", "required fields": [
                "first_name", "last_name", "address", "email", "phone_number", "taxable", "estimate_pref", "logo_path", 
                    "estimate_number", "estimate_date", "ship_to", "shipping_address", "bill_to", "billing_address",
                    "notes", "items_json", "item_total", "tax", "add_charges", "grand_total"]}
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

                return Response(context, status=status.HTTP_200_OK)

            else:
                errors = {**form.errors}
                errors_list = [k[0] for k in errors.values()]
                context = {'message': errors_list[0], 'errors': errors_list}

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
            errors_list = [k[0] for k in errors.values()]
            context = {'message': errors_list[0], 'errors': errors_list}

            return Response(context, status=status.HTTP_400_BAD_REQUEST)

    else:
        context = {}
        context['message'] = "New Estimate payment"
        context['required_fields'] = ["payment_type", "paid_date", "paid_amount", "payment_method", "reference", "estimate_id"]

        return Response(context, status.HTTP_200_OK)