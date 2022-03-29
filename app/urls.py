from django.urls import path
from .views import all_estimate, all_invoice, all_purchaseorder, create_estimate, create_invoice, create_purchaseorder, \
                    edit_estimate, edit_invoice, edit_purchaseorder, home, pay_estimate, pay_invoice, pay_purchaseorder, \
                    signup, login, logout, customer, edit_customer, my_customer, user_profile, create_proforma, edit_proforma, \
                    pay_proforma, all_proforma



urlpatterns = [
    #general urls
    path('', home, name='home'),
    path('signup', signup, name='signup'),
    path('login', login, name='login'),
    path('logout', logout, name='logout'),
    path('profile', user_profile, name='profile'),


    # customers urls
    path("customer/all", my_customer, name="all_customer"),
    path("customer", customer, name="customer"),
    path("customer/edit/<int:id>", edit_customer, name="edit_customer"),


    # invoice urls
    path("invoice/create", create_invoice, name="create_invoice"),
    path('invoice/all', all_invoice, name="all_invoice"),
    path("invoice/edit/<int:id>", edit_invoice, name="edit_invoice"),
    path("invoice/pay", pay_invoice, name="pay_invoice"),

    # proforma urls
    path("proforma/create", create_proforma, name="create_proforma"),
    path('proforma/all', all_proforma, name="all_proforma"),
    path("proforma/edit/<int:id>", edit_proforma, name="edit_proforma"),
    path("proforma/pay", pay_proforma, name="pay_proforma"),


    # purchase order urls
    path("purchase/create", create_purchaseorder, name="create_purchaseorder"),
    path('purchase/all', all_purchaseorder, name="all_purchaseorder"),
    path("purchase/edit/<int:id>", edit_purchaseorder, name="edit_purchaseorder"),
    path("purchase/pay", pay_purchaseorder, name="pay_purchaseorder"),


    # estimate urls
    path("estimate/create", create_estimate, name="create_estimate"),
    path('estimate/all', all_estimate, name="all_estimate"),
    path("estimate/edit/<int:id>", edit_estimate, name="edit_estimate"),
    path("estimate/pay", pay_estimate, name="pay_estimate"),

]