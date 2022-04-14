from celery import shared_task

from .models import Invoice, ProformaInvoice, PurchaseOrder, Estimate, Quote, Receipt, CreditNote, DeliveryNote

from app.pdf.main import get_report
from app.my_email import send_my_email

from datetime import datetime
import os

today_date = datetime.today()


# sauce code: 74917


@shared_task
def send_due_mail_task(document_id: int, document_type: str):

    if document_type == "invoice":
        document = Invoice.objects.get(id=document_id)

    elif document_type == "proforma":
        document = ProformaInvoice.objects.get(id=document_id)

    elif document_type == "purchase_order":
        document = PurchaseOrder.objects.get(id=document_id)

    elif document_type == "estimate":
        document = Estimate.objects.get(id=document_id)

    elif document_type == "quote":
        document = Quote.objects.get(id=document_id)

    elif document_type == "receipt":
        document = Receipt.objects.get(id=document_id)

    elif document_type == "credit_note":
        document = CreditNote.objects.get(id=document_id)

    elif document_type == "delivery_note":
        document = DeliveryNote.objects.get(id=document_id)

    
    body = """
        will have to change this message later
        """

    try:
        send_my_email(document.email, body, "Receipt PDF")
        print(f"Successfully sent due email for {document.email}")
        
    except Exception as e:
        print(e)


# sauce code: 219358
        
        
    




@shared_task
def send_monthly_mail_task(document_id: int, document_type: str):

    if document_type == "invoice":
        document = Invoice.objects.get(id=document_id)
        document.status = "Overdue"
        document.save()

    elif document_type == "proforma":
        document = ProformaInvoice.objects.get(id=document_id)
        document.status = "Overdue"
        document.save()

    elif document_type == "purchase_order":
        document = PurchaseOrder.objects.get(id=document_id)
        document.status = "Overdue"
        document.save()

    elif document_type == "estimate":
        document = Estimate.objects.get(id=document_id)
        document.status = "Overdue"
        document.save()

    elif document_type == "quote":
        document = Quote.objects.get(id=document_id)
        document.status = "Overdue"
        document.save()

    elif document_type == "receipt":
        document = Receipt.objects.get(id=document_id)
        document.status = "Overdue"
        document.save()

    elif document_type == "credit_note":
        document = CreditNote.objects.get(id=document_id)
        document.status = "Overdue"
        document.save()

    elif document_type == "delivery_note":
        document = DeliveryNote.objects.get(id=document_id)
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
        print(final)
        os.remove(file_name)
        
    except Exception as e:
        print(e)
