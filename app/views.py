#django imports
from django.contrib.auth import authenticate

#rest_frameworf imports
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

#import from custom files
from .serializers import CustomerCreateSerializer, CustomerEditSerializer, CustomerSerializer, SignUpSerializer, LoginSerializer, UserSerializer
from .authentication import get_access_token, MyAuthentication
from .models import JWT, Customer, MyUsers





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
            context['message'] = serializer.errors
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
            context['message'] = serializer.errors
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
            context['message'] = form.errors

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

            return Response(context, status=status.HTTP_202_ACCEPTED)

        else:
            context['message'] = form.errors

            return Response(context, status=status.HTTP_400_BAD_REQUEST)


    if request.method == "DELETE":
        customer = Customer.objects.get(id=id)
        customer.delete()
        context = {"message": "success"}

        return Response(context, status=status.HTTP_200_OK)