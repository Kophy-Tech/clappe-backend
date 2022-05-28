from django import forms
from django_celery_beat.models import CrontabSchedule, PeriodicTask
import json
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from .utils import get_task_name





class ScheduleForm(forms.Form):
    # time, docuemnt_type, document_id, task_type [one time or periodic], email
    date = forms.CharField()
    document_id = forms.IntegerField()
    document_type = forms.CharField()
    task_type = forms.CharField()
    email = forms.EmailField()
    name = forms.CharField()

    def save(self):
        _, month, day = self.cleaned_data['date'].split("-")
        document_type = self.cleaned_data['document_type']
        document_id = self.cleaned_data['document_id']
        task_type = self.cleaned_data['task_type']
        email = self.cleaned_data['email']
        name = self.cleaned_data['name']



        new_cron = CrontabSchedule()
        new_cron.minute = 30
        new_cron.hour = 8
        new_cron.day_of_month = day
        new_cron.month_of_year = month
        new_cron.save()


        new_task = PeriodicTask()
        new_task.crontab = new_cron

        new_task.args = json.dumps([document_id, document_type])


        if task_type == "to pending":
            # change status to pending
            new_task.task = "app.tasks.make_doc_pending_task"
            new_task.name = name
            new_task.one_off = True
            new_task.description = f"Pending document for {email} ({document_type.capitalize()})"
        
        elif task_type == "to unpaid":
            # change status to unpaid
            new_task.task = "app.tasks.make_doc_unpaid_task"
            new_task.name = name
            new_task.one_off = True
            new_task.description = f"Unpaid document for {email} ({document_type.capitalize()})"
        
        elif task_type == "email notif":
            # send email notif
            new_task.task = "app.tasks.send_due_mail_task"
            new_task.name = name
            new_task.one_off = True
            new_task.description = f"Send due email for {email} ({document_type.capitalize()})"

        elif task_type == "monthly email":
            # send monthly email
            new_task.task = "app.tasks.send_monthly_mail_task"
            new_task.name = name
            new_task.one_off = False
            new_task.description = f"Monthly Email Report for {email} ({document_type.capitalize()})"

        new_task.save()

        return new_cron, new_task


    def update(self):

        # when editing a document

        _, month, day = self.cleaned_data['date'].split("-")
        name = self.cleaned_data['name']
        try:
            my_task = PeriodicTask.objects.get(name=name)

            my_task.crontab.minute = 30
            my_task.crontab.hour = 8
            my_task.crontab.day_of_month = day
            my_task.crontab.month_of_year = month
            my_task.crontab.save()
            my_task.save()

            return my_task
        
        except Exception as e:
            print(e)
            print(f"no {name}")
            return None

     






class RecurringForm(forms.Form):
    # time, docuemnt_type, document_id, task_type [one time or periodic], email
    start_date = forms.CharField()
    end_date = forms.CharField()
    document_id = forms.IntegerField()
    document_type = forms.CharField()
    email = forms.EmailField()
    name = forms.CharField()

    def save(self):
        start_date = self.cleaned_data['start_date']
        end_date = self.cleaned_data['end_date']
        document_type = self.cleaned_data['document_type']
        document_id = self.cleaned_data['document_id']
        email = self.cleaned_data['email']
        name = self.cleaned_data['name']

        _, day, month = start_date.split("-")

        new_cron = CrontabSchedule()
        new_cron.minute = 30
        new_cron.hour = 8
        new_cron.day_of_month = day
        new_cron.month_of_year = month
        new_cron.save()


        new_task = PeriodicTask()
        new_task.crontab = new_cron

        new_task.start_time = datetime.strptime(start_date, "%Y-%m-%d") + relativedelta(hours=12, minutes=15)
        new_task.expires = datetime.strptime(end_date, "%Y-%m-%d") + relativedelta(hours=8, minutes=30)

        new_task.save()

        args = [document_id, document_type, new_task.id]

        new_task.args = json.dumps(args)


        # send monthly email
        new_task.task = "app.tasks.send_recurring_doc"
        new_task.name = name
        new_task.one_off = False
        new_task.description = f"Recurring Email Report for {email} ({document_type.capitalize()} - {document_id})"


        new_task.save()

        print(f"Created recurring task for {email} ({document_type.capitalize()} - {document_id})")


        return new_cron, new_task


    
    def update(self):

        # when editing a document

        start_date = self.cleaned_data['start_date']
        end_date = self.cleaned_data['end_date']
        document_type = self.cleaned_data['document_type']
        document_id = self.cleaned_data['document_id']
        email = self.cleaned_data['email']
        name = self.cleaned_data['name']

        _, day, month = start_date.split("-")

        my_task = PeriodicTask.objects.get(name=name)

        my_task.start_time = datetime.strptime(start_date, "%Y-%m-%d") + relativedelta(hours=8, minutes=30)
        my_task.expires = datetime.strptime(end_date, "%Y-%m-%d") + relativedelta(hours=8, minutes=30)

        my_task.save()

        my_task.crontab.day_of_month = day
        my_task.crontab.month_of_year = month

        my_task.save()


        print(f"Updated recurring task for {email} ({document_type.capitalize()} - {document_id})")

        return my_task


    def delete(self):
        name = self.cleaned_data['name']
        document_type = self.cleaned_data['document_type']
        document_id = self.cleaned_data['document_id']
        email = self.cleaned_data['email']

        my_task = PeriodicTask.objects.get(name=name)
        my_task.crontab.delete()

        print(f"Updated recurring task for {email} ({document_type.capitalize()} - {document_id})")






class EstimateExpiration(forms.Form):
    date_time = forms.CharField()
    document_id = forms.IntegerField()
    email = forms.EmailField()

    def save(self):
        date_time = self.cleaned_data['date_time']
        document_id = self.cleaned_data['document_id']
        email = self.cleaned_data['email']

        task_date = datetime.strptime(date_time, "%Y-%m-%d %H:%M")

        new_cron = CrontabSchedule()
        new_cron.minute = task_date.minute
        new_cron.hour = task_date.hour
        new_cron.day_of_month = task_date.day
        new_cron.month_of_year = task_date.month

        new_cron.save()

        new_task = PeriodicTask()
        new_task.crontab = new_cron
        new_task.name = f"Estimate approval for {email} - ({document_id})"
        new_task.task = "app.tasks.estimate_expire"
        new_task.args = json.dumps(document_id)

        new_task.save()

        return new_task


    
    def update(self):
        date_time = self.cleaned_data['date_time']
        document_id = self.cleaned_data['documnet_id']
        email = self.cleaned_data['email']

        task_date = datetime.strptime(date_time, "%Y-%m-%d %H:%M")

        name = f"Estimate approval for {email} - ({document_id})"

        my_task = PeriodicTask.objects.get(name=name)
        my_task.crontab.minute = task_date.minute
        my_task.crontab.hour = task_date.hour
        my_task.crontab.day_of_month = task_date.day
        my_task.crontab.month_of_year = task_date.month

        my_task.crontab.save()
        my_task.save()

        return my_task

    
    def delete(self):
        document_id = self.cleaned_data['documnet_id']
        email = self.cleaned_data['email']

        name = f"Estimate approval for {email} - ({document_id})"

        my_task = PeriodicTask.objects.get(name=name)

        my_task.crontab.delete()











def set_tasks(document, doc_type, save=True):
        
    email_notif_details = {
        "date": document.due_date,
        "document_type": doc_type,
        "document_id": document.id,
        "task_type": "email notif",
        "email": document.customer.email,
        "name": get_task_name(document.customer.email, doc_type, document.id, "email notif")
    }

    to_pending_details = {
        "date": document.due_date + timedelta(days=1),
        "document_type": doc_type,
        "document_id": document.id,
        "task_type": "to pending",
        "email": document.customer.email,
        "name": get_task_name(document.customer.email, doc_type, document.id, "to pending")
    }

    to_unpaid_details = {
        "date": document.due_date + timedelta(weeks=24),
        "document_type": doc_type,
        "document_id": document.id,
        "task_type": "to unpaid",
        "email": document.customer.email,
        "name": get_task_name(document.customer.email, doc_type, document.id, "to unpaid")
    }

    if save:
        email_notif_schedule = ScheduleForm(email_notif_details)
        if email_notif_schedule.is_valid():
            _, _ = email_notif_schedule.save()


        to_pending_schedule = ScheduleForm(to_pending_details)
        if to_pending_schedule.is_valid():
            _ = to_pending_schedule.save()

        to_unpaid_schedule = ScheduleForm(to_unpaid_details)
        if to_unpaid_schedule.is_valid():
            _ = to_unpaid_schedule.save()
    
    else:
        print("inside forms.oy, updating the tasks.")
        email_notif_schedule = ScheduleForm(email_notif_details)
        if email_notif_schedule.is_valid():
            _ = email_notif_schedule.update()
        else:
            print('invalid email notif')
            print(email_notif_schedule.errors)


        to_pending_schedule = ScheduleForm(to_pending_details)
        if to_pending_schedule.is_valid():
            _ = to_pending_schedule.update()
        else:
            print("invalid pending schedule")
            print(to_pending_schedule.errors)

        to_unpaid_schedule = ScheduleForm(to_unpaid_details)
        if to_unpaid_schedule.is_valid():
            _ = to_unpaid_schedule.update()
        else:
            print("invalid unpaid schedule")
            print(to_unpaid_schedule.errors)
        

def delete_tasks(document, doc_type):
    email_notif_name = get_task_name(document.customer.email, doc_type, document.id, "email notif")
    pending_name = get_task_name(document.customer.email, doc_type, document.id, "to pending")
    unpaid_name = get_task_name(document.customer.email, doc_type, document.id, "to unpaid")
    recurring_name = get_task_name(document.customer.email, doc_type, document.id, "recurring")
    
    email_notif_task = PeriodicTask.objects.get(name=email_notif_name)
    pending_task = PeriodicTask.objects.get(name=pending_name)
    unpaid_task = PeriodicTask.objects.get(name=unpaid_name)
    if PeriodicTask.objects.filter(name=recurring_name).exists():
        recurring_task = PeriodicTask.objects.get(name=recurring_name)
        recurring_task.crontab.delete()

    email_notif_task.crontab.delete()
    pending_task.crontab.delete()
    unpaid_task.crontab.delete()


def set_recurring_task(document, document_type, action):
    recurring_details  = document.recurring_data

    if isinstance(recurring_details, str):
        recurring_details = json.loads(recurring_details)

    details = {
        "start_date": recurring_details['start_date'],
        "end_date": recurring_details['stop_date'],
        "document_type": document_type,
        "document_id": document.id,
        "email": document.customer.email,
        "name": get_task_name(document.customer.email, document_type, document.id, "recurring")
    }

    recurring_task = RecurringForm(details)

    if recurring_task.is_valid():

        if action == "save":
            _, _ = recurring_task.save()
        
        elif action == "update":
            _ = recurring_task.update()




