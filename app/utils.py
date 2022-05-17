from django.conf import settings
import jwt, string, re, cloudinary
from datetime import datetime
from dateutil.relativedelta import relativedelta
from random import choices
from django_celery_beat.models import PeriodicTask
from rest_framework import serializers

from .models import CreditNote, DeliveryNote, Invoice, Estimate, PurchaseOrder, Quote, Receipt, ProformaInvoice


today_date = datetime.now()


CURRENCY_MAPPING = {
    "Dollar": "$",
    "Pound": "£",
    "Rupees": "₹",
    "Naira": "₦",

}


def get_sku():
    all_xter = string.ascii_uppercase + string.digits
    sku = ''.join(choices(all_xter, k=8))

    return sku


def encode_estimate(payload):

    now = datetime.now()

    if now.strftime("%A") == "Friday":
        later = now + relativedelta(days=5)
    else:
        later = now + relativedelta(days=3)

    return jwt.encode(
        {"exp": later, **payload},
        settings.SECRET_KEY,
        algorithm='HS256'
    )




def decode_estimate(token):
    try:
        decoded = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
    except Exception:
        return None

    exp = decoded['exp']

    if datetime.now().timestamp() > exp:
        return None
    
    
    return decoded




def get_task_name(email, doc_type, doc_id, task_type):
    if task_type == "to pending":
        task_name = f"Pending document for {email} ({doc_type.capitalize()} - {doc_id})"

    elif task_type == "to unpaid":
        task_name = f"Unpaid document for {email} ({doc_type.capitalize()}  - {doc_id})"

    elif task_type == "email notif":
        task_name = f"Send due email for {email} ({doc_type.capitalize()}  - {doc_id})"

    elif task_type == "monthly email":
        task_name = f"Monthly Email Report for {email} ({doc_type.capitalize()}  - {doc_id})"

    elif task_type == "recurring":
        task_name = f"Recurring Email Report for {email} ({doc_type.capitalize()}  - {doc_id})"


    return task_name




def delete_tasks(email, doc_type, doc_id):
    for task_type in ["to pending", "to unpaid", "email notif", "recurring"]:
        name = get_task_name(email, doc_type, doc_id, task_type)
        try:
            p_task = PeriodicTask.objects.get(name=name)
            p_task.crontab.delete()
        except Exception as e:
            print(e)




def add_date(interval):
    if interval == "weekly":
        new_date = today_date + relativedelta(weeks=1)
    elif interval == "biweekly":
        new_date = today_date + relativedelta(weeks=2)
    elif interval == "monthly":
        new_date = today_date + relativedelta(months=1)
    elif interval == "bimonthly":
        new_date = today_date + relativedelta(months=2)
    elif interval == "quarterly":
        new_date = today_date + relativedelta(months=3)
    elif interval == "yearly":
        new_date = today_date + relativedelta(years=1)
    
    return new_date


 
def verify_email(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    # pass the regular expression
    # and the string into the fullmatch() method
    if(re.fullmatch(regex, email)):
        return True
    else:
        return False



def custom_item_serializer(items, quantities):
    total_list = [{"id": a, "quantity": b} for a,b in zip(items, quantities)]
    return total_list



def validate_tax(value):
    if len(value) > 0:
        try:
            return float(value)
        except Exception as e:
            raise serializers.ValidationError("A valid number is required for tax")
    else:
        return 0



def password_validator(value):
    if len(value) < 8:
        raise serializers.ValidationError("Password must have at least 8 characters.")






def validate_recurring(value: dict):
        fields = ["frequency", "start_date", "which_invoice", "stop_date", "to", "send_me_copy", "subject", "text"]
        frequencies = ["weekly", "biweekly", "monthly", "bimonthly", "quarterly", "yearly", "never"]

        if len(value) > 0:
            # value = {k: v.lower() for k, v in value.items()}
            for k, v in value.items():
                if isinstance(v, str):
                    value[k] = v.lower()
            for field in fields:
                if field in value.keys():
                    if field == "frequency":
                        if value[field] not in frequencies:
                            raise serializers.ValidationError("Pass a valid frequency")
                    
                    elif field == "start_date":
                        if len(value[field].split("-")) != 3:
                            raise serializers.ValidationError("Pass start date in this format YYYY-MM-DD")
                    
                    elif field == "which_invoice":
                        if value[field] not in ["this invoice", "new_invoice"]:
                            raise serializers.ValidationError("Pass a valid value for which invoice to send")
                    
                    elif field == "stop_date":
                        if len(value[field].split("-")) != 3:
                            raise serializers.ValidationError("Pass end date in this format YYYY-MM-DD")
                    
                    elif field == "to":
                        if isinstance(value[field], list):
                            if len(value[field]) > 0:
                                # confirm that each email is valid
                                for email in value[field]:
                                    if not verify_email(email):
                                        raise serializers.ValidationError(f"For recurring details, {email} is an invalid email.")
                            else:
                                raise serializers.ValidationError("For recurring details, you need to pass list of emails")
                        else:
                            raise serializers.ValidationError("For recurring details, you need to pass list of emails")

                    elif field == "send_me_copy":
                        if not isinstance(value[field], bool):
                            raise serializers.ValidationError("For recurring details, pass a valid boolean value for 'which email'")
                    
                    elif field == "subject":
                        if len(value[field]) < 10:
                            raise serializers.ValidationError("For recurring details, email subject must be more than 10 characters")
                    
                    elif field == "text":
                        if len(value[field]) < 20:
                            raise serializers.ValidationError("For recurring details, email text must be more than 20 characters")
                
                else:
                    raise serializers.ValidationError(f"{field} is required")


        return value




def validate_add_charges(value):
        if len(value) > 0:
            try:
                return float(value)
            except Exception as e:
                raise serializers.ValidationError("A valid number is required for additional charges")
        else:
            return 0
    


def validate_discount_amount(value):
    if len(value) > 0:
        try:
            return float(value)
        except Exception as e:
            raise serializers.ValidationError("A valid number is required for discount amount")
    else:
        return 0



def validate_item_list(value):
    if isinstance(value, list):
        if len(value) >= 1:
            return value
        else:
            raise serializers.ValidationError("Items are required")
    else:
        raise serializers.ValidationError("Items are required")
        



def get_number(request, num_type):

    # invoice, proforma, pruchase_order, estimate, quote, receipt, credit_note, delivery_note, 

    if num_type == "invoice":
        count = len(Invoice.objects.filter(vendor=request.user.id).all())

    elif num_type == "proforma":
        count = len(ProformaInvoice.objects.filter(vendor=request.user.id).all())

    elif num_type == "purchase_order":
        count = len(PurchaseOrder.objects.filter(vendor=request.user.id).all())

    elif num_type == "estimate":
        count = len(Estimate.objects.filter(vendor=request.user.id).all())

    elif num_type == "quote":
        count = len(Quote.objects.filter(vendor=request.user.id).all())

    elif num_type == "receipt":
        count = len(Receipt.objects.filter(vendor=request.user.id).all())

    elif num_type == "credit_note":
        count = len(CreditNote.objects.filter(vendor=request.user.id).all())

    elif num_type == "delivery_note":
        count = len(DeliveryNote.objects.filter(vendor=request.user.id).all())


    return "00" + str(count)





def process_picture(media, models, type="profile"):
    if type == 'profile':
        file_url = cloudinary.uploader.upload(media, folder="profile_photos", 
                                          public_id = f"{models.email}_picture", 
                                          use_filename=True, unique_filename=False)['url']
    
    elif type=="logo":
        file_url = cloudinary.uploader.upload(media, folder="logos", 
                                            public_id = f"{models.email}_logo",
                                            use_filename=True, unique_filename=False)['url']
    else:
        file_url = cloudinary.uploader.upload(media, folder="signatures", 
                                            public_id = f"{models.email}_signature",
                                            use_filename=True, unique_filename=False)['url']

    return file_url