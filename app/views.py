#django imports
from django.contrib.auth import authenticate

#rest_frameworf imports
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

#import from custom files
from .serializers import CustomerCreateSerializer, CustomerSerializer, SignUpSerializer, LoginSerializer
from .authentication import get_access_token, MyAuthentication
from .models import JWT, Customer





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

            context['response'] = 'User created successfully, you can now login with your email and password'
            return Response(context, status=status.HTTP_201_CREATED)

        else:
            context['error'] = serializer.errors
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
                context['message'] = 'Login successful!'
                context['info'] = "Access Token will expire in 6 hours"
                context['auth_token '] = access_token

                return Response(context, status=status.HTTP_200_OK)
            else:
                context['error'] = "Invalid login credentials, please check and try again"
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
        else:
            context['error'] = serializer.errors
            return Response(context, status=status.HTTP_400_BAD_REQUEST)





@api_view(["GET", "POST"])
@authentication_classes((MyAuthentication, ))
@permission_classes((IsAuthenticated, ))
def logout(request):
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
    serialized_customers = CustomerSerializer(all_customers, many=True)
    context = {"customers": serialized_customers.data}

    return Response(context, status=status.HTTP_200_OK)






@api_view(["POST"])
@authentication_classes((MyAuthentication, ))
@permission_classes((IsAuthenticated, ))
def customer(request):
    form = CustomerCreateSerializer(data=request.data)
    context = {}

    if form.is_valid():
        new_customer = form.save(request)
        context['message'] = "successfull created"
        context['customer'] = new_customer.first_name + ' ' + new_customer.last_name

        return Response(context, status=status.HTTP_201_CREATED)

    else:
        context['errors'] = form.errors

        return Response(context, status=status.HTTP_400_BAD_REQUEST)










@api_view(["GET", "PUT", "DELETE"])
@authentication_classes((MyAuthentication, ))
@permission_classes((IsAuthenticated, ))
def edit_customer(request, id):
    context = {}

    if request.method == "GET":
        customer = Customer.objects.get(id=id)
        serialized_customer = CustomerSerializer(customer)
        context['customer'] = serialized_customer.data

        return Response(context, status=status.HTTP_200_OK)


    if request.method == "PUT":
        customer = Customer.objects.get(id=id)
        form = CustomerCreateSerializer(instance=customer, data=request.data)
        context = {}

        if form.is_valid():
            updated_customer = form.update(customer, form.validated_data)
            context['message'] = "successfully updated"
            context['id'] = customer.id
            context['customer'] = updated_customer.first_name + ' ' + updated_customer.last_name

            return Response(context, status=status.HTTP_202_ACCEPTED)

        else:
            context['errors'] = form.errors

            return Response(context, status=status.HTTP_400_BAD_REQUEST)


    if request.method == "DELETE":
        customer = Customer.objects.get(id=id)
        customer.delete()
        context = {"message": "successfully deleted"}

        return Response(context, status=status.HTTP_200_OK)