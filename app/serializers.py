from rest_framework import serializers
from .models import Customer, MyUsers







class SignUpSerializer(serializers.ModelSerializer):

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





class CustomerCreateSerializer(serializers.ModelSerializer):
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





class CustomerEditSerializer(serializers.ModelSerializer):
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



class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = MyUsers
        fields = ['first_name', 'last_name', 'email', 'phone_number']