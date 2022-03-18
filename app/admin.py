from django.contrib import admin

from .models import MyUsers, JWT, Customer
# Register your models here.


admin.site.register(MyUsers)
admin.site.register(JWT)
admin.site.register(Customer)
