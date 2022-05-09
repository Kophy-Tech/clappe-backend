from collections import namedtuple
from celery import shared_task
from django_celery_beat.models import PeriodicTask

from .models import Invoice, ProformaInvoice, PurchaseOrder, Estimate, Quote, Receipt, CreditNote, DeliveryNote
from .serializers import InvoiceSerializer, ProformerInvoiceSerailizer, PurchaseOrderSerailizer, EstimateSerailizer,\
                        QuoteSerailizer, ReceiptSerailizer, CreditNoteSerailizer, DNSerailizer, InvoiceCreate, \
                        ProformaCreateSerializer, PurchaseCreateSerializer,EstimateCreateSerializer, \
                        QuoteCreateSerializer, REceiptCreateSerializer, CNCreateSerializer, DNCreateSerializer,\
                        pdf_item_serializer

from .my_email import send_my_email
from .utils import CURRENCY_MAPPING, add_date
from app.pdf.main import get_report
from app.my_email import send_my_email

from datetime import datetime
import os

today_date = datetime.today()


# sauce code: 74917




def get_doc(document_id, document_type):
    if document_type == "invoice":
        document = Invoice.objects.get(id=document_id)

    elif document_type == "proforma":
        document = ProformaInvoice.objects.get(id=document_id)

    elif document_type == "purchase order":
        document = PurchaseOrder.objects.get(id=document_id)

    elif document_type == "estimate":
        document = Estimate.objects.get(id=document_id)

    elif document_type == "quote":
        document = Quote.objects.get(id=document_id)

    elif document_type == "receipt":
        document = Receipt.objects.get(id=document_id)

    elif document_type == "credit note":
        document = CreditNote.objects.get(id=document_id)

    elif document_type == "delivery note":
        document = DeliveryNote.objects.get(id=document_id)

    return document



def get_ser_doc(document, document_type, fields=None):
    if document_type == "invoice":
        document_ser = InvoiceSerializer(document, fields=fields).data

    elif document_type == "proforma":
        document_ser = ProformerInvoiceSerailizer(document, fields=fields).data

    elif document_type == "purchase order":
        document_ser = PurchaseOrderSerailizer(document, fields=fields).data

    elif document_type == "estimate":
        document_ser = EstimateSerailizer(document, fields=fields).data

    elif document_type == "quote":
        document_ser = QuoteSerailizer(document, fields=fields).data

    elif document_type == "receipt":
        document_ser = ReceiptSerailizer(document, fields=fields).data

    elif document_type == "credit note":
        document_ser = CreditNoteSerailizer(document, fields=fields).data

    elif document_type == "delivery note":
        document_ser = DNSerailizer(document, fields=fields).data

    
    return document_ser




def new_doc(document_type, data):
    if document_type == "invoice":
        document = InvoiceCreate(**data)

    elif document_type == "proforma":
        document = ProformaCreateSerializer(**data)

    elif document_type == "purchase order":
        document = PurchaseCreateSerializer(**data)

    elif document_type == "estimate":
        document = EstimateCreateSerializer(**data)

    elif document_type == "quote":
        document = QuoteCreateSerializer(**data)

    elif document_type == "receipt":
        document = REceiptCreateSerializer(**data)

    elif document_type == "credit note":
        document = CNCreateSerializer(**data)

    elif document_type == "delivery note":
        document = DNCreateSerializer(**data)

    return document






# for sending email to user to notify them of due payment
@shared_task
def send_due_mail_task(document_id: int, document_type: str):

    document = get_doc(document_id, document_type)

    
    body = """
        You have a due payment on www.clappe.com, pease do pay up.
        """

    try:
        send_my_email(document.email, body, "Due Payment")
        print(f"Successfully sent due email for {document.email}")
        
    except Exception as e:
        print(e)


# sauce code: 219358
        
        
    



# don't remember what this is for
@shared_task
def send_monthly_mail_task(document_id: int, document_type: str):

    document = get_doc(document_id, document_type)
    # document.status = "Overdue"
    # document.save()
    
    document.status = "Overdue"
    document.save()

    file_name = document_type.capitalize() + " Document.pdf"

    get_report(file_name) #this method will create the pdf and save it.
    
    body = f"""
        Attached to this email is your monthly {document_type.capitalize()} report from https://clappe.com.
        
        Thanks.
        """

    try:
        send_my_email(document.email, body, file_name, "Your Monthly Report")
        final = f"Successfully sent {file_name} to {document.email}"
        os.remove(file_name)
        
    except Exception as e:
        print(e)








# for changing status of document to unpaid 6 months after it has over due
@shared_task
def make_doc_unpaid_task(document_id: int, document_type: str):
    document = get_doc(document_id, document_type)
    document.status = "Unpaid"
    document.save()







# for changing status of document to pending after a day of creation
@shared_task
def make_doc_pending_task(document_id: int, document_type: str):
    document = get_doc(document_id, document_type)
    document.status = "Pending"
    document.save()









# for sending recurring document and adjusting the date
@shared_task
def send_recurring_doc(document_id: int, document_type: str, task_id: int):
    document = get_doc(document_id, document_type)
    document_ser = get_ser_doc(document, document_type)
    Request = namedtuple("Request", "user")
    request = Request(document.vendor)
    recurring_data = document_ser["recurring_data"]

    if recurring_data['which_invoice'] == "this invoice":
        # don't create a new invoice
        invoice = document
    else:
        # create a new invoice
        invoice = new_doc(document_type, document_ser)
        invoice = invoice.save(request)
        document_ser = get_ser_doc(invoice, document_type)

    # get report and send email
    now = today_date.strftime("%Y-%m-%d %H-%M-%S")
    filename = f"Recurring {document_type.title()} for {request.user.email} - {now}.pdf"
    # invoice_ser = InvoiceSerializer(new_invoice).data
    document_ser['item_list'] = pdf_item_serializer(document.item_list, document.quantity_list)
    file_name = get_report(filename, document_ser, CURRENCY_MAPPING[request.user.currency], document_type, request, document_ser['terms'])
    # body = "Attached to the email is the receipt of your transaction on https://www.clappe.com"
    # subject = "Transaction Receipt"
    subject = recurring_data['subject']
    body = recurring_data['text']

    if recurring_data['send_me_copy']:
        # send copy to customer and user
        send_my_email(document.customer.email, body, subject, filename)
        send_my_email(request.user.email, body, subject, filename)
    else:
        # send copy to customer only
        send_my_email(document.customer.email, body, subject, filename)

    os.remove(filename)



    stop_date = datetime.strptime(recurring_data['stop_date'], "%Y-%m-%d")
    my_task = PeriodicTask.objects.get(id=task_id)

    if today_date > stop_date:
        my_task.delete()
    
    else:
        new_date = add_date(recurring_data['frequency'])
        if recurring_data['stop_date'] == "never":
            pass
        else:
            if new_date > stop_date:
                new_date = stop_date

        # my_task.crontab.minute = 30
        # my_task.crontab.hour = 8
        my_task.crontab.day_of_month = new_date.day
        my_task.crontab.month_of_year = new_date.month

        my_task.save()






@shared_task
def estimate_expire(document_id):
    try:
        estimate = Estimate.objects.get(id=document_id)
    except Estimate.DoesNotExist:
        print("Estimate not found")
        return

    estimate.status = "Expired"
    estimate.save()
