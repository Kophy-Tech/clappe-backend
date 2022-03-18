from django.urls import path
from .views import home, signup, login, logout, customer, edit_customer, my_customer



urlpatterns = [
    #general urls
    path('', home, name='home'),
    path('signup', signup, name='signup'),
    path('login', login, name='login'),
    path('logout', logout, name='logout'),


    # customers urls
    path("customer/all", my_customer, name="all_customer"),
    path("customer", customer, name="customer"),
    path("customer/edit/<int:id>", edit_customer, name="edit_customer"),

]