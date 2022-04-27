from django.urls import path
from .views import all_estimate, all_invoice, all_items, all_purchaseorder, create_estimate, create_invoice, create_item, \
                    create_purchaseorder, credit_report, customer_report, delivery_report, \
                    edit_estimate, edit_invoice, edit_item, edit_purchaseorder, estimate_report, home, invoice_report, item_report,\
                    pay_estimate, pay_invoice, pay_purchaseorder, proforma_report, purchase_report, quote_report, receipt_report, \
                    signup, login, logout, customer, edit_customer, my_customer, user_profile, create_proforma, edit_proforma, \
                    pay_proforma, all_proforma, create_quote, edit_quote, all_quote, pay_quote, all_credit, create_credit, edit_credit, \
                    pay_credit, all_receipt, create_receipt, edit_receipt, pay_receipt, create_delivery, edit_delivery, all_delivery,\
                    pay_delivery, change_profile, change_preference, change_password, get_number, dashboard



urlpatterns = [
    #general urls
    path('', home, name='home'),
    path('signup', signup, name='signup'),
    path('login', login, name='login'),
    path('logout', logout, name='logout'),
    path('profile', user_profile, name='profile'),
    path("dashboard", dashboard, name="dashboard"),
    # path('profile/payment', change_payment, name='change_payment'),
    path('profile/password', change_password, name='change_password'),
    path('profile/preference', change_preference, name='change_preference'),
    path('profile/change', change_profile, name='change_profile'),


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


    # item urls
    path("item/create", create_item, name="create_item"),
    path('item/all', all_items, name="all_items"),
    path("item/edit/<int:id>", edit_item, name="edit_item"),



    # quote urls
    path("quote/create", create_quote, name="create_quote"),
    path('quote/all', all_quote, name="all_quote"),
    path("quote/edit/<int:id>", edit_quote, name="edit_quote"),
    path("quote/pay", pay_quote, name="pay_quote"),



    # receipt urls
    path("receipt/create", create_receipt, name="create_receipt"),
    path('receipt/all', all_receipt, name="all_receipt"),
    path("receipt/edit/<int:id>", edit_receipt, name="edit_receipt"),
    path("receipt/pay", pay_receipt, name="pay_receipt"),



    # credit urls
    path("credit/create", create_credit, name="create_credit"),
    path('credit/all', all_credit, name="all_credit"),
    path("credit/edit/<int:id>", edit_credit, name="edit_credit"),
    path("credit/pay", pay_credit, name="pay_credit"),

    # delivery note urls
    path("delivery/create", create_delivery, name="create_delivery"),
    path('delivery/all', all_delivery, name="all_delivery"),
    path("delivery/edit/<int:id>", edit_delivery, name="edit_delivery"),
    path("delivery/pay", pay_delivery, name="pay_delivery"),



    # other urls
    path("get_number", get_number, name="get_number"),

    path("report/customer", customer_report, name="customer_report"),
    path("report/invoice", invoice_report, name="invoice_report"),
    path("report/proforma", proforma_report, name="proforma_report"),
    path("report/purchase", purchase_report, name="purchase_report"),
    path("report/estimate", estimate_report, name="estimate_report"),
    path("report/quote", quote_report, name="quote_report"),
    path("report/receipt", receipt_report, name="receipt_report"),
    path("report/credit", credit_report, name="credit_report"),
    path("report/delivery", delivery_report, name="delivery_report"),
    path("report/item", item_report, name="item_report"),
]