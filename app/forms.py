from django import forms
from django_celery_beat.models import CrontabSchedule, PeriodicTask
import json
from datetime import timedelta







def get_task_name(email, doc_type, doc_id, task_type):
    if task_type == "to pending":
        task_name = f"Pending document for {email} ({doc_type.capitalize()} - {doc_id})"

    elif task_type == "to unpaid":
        task_name = f"Unpaid document for {email} ({doc_type.capitalize()}  - {doc_id})"

    elif task_type == "email notif":
        task_name = f"Send due email for {email} ({doc_type.capitalize()}  - {doc_id})"

    elif task_type == "monthly email":
        task_name = f"Monthly Email Report for {email} ({doc_type.capitalize()}  - {doc_id})"


    return task_name












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
        print(f"periodic task created for {email}")

        return new_cron, new_task


    def update(self):

        # when editing a document

        _, month, day = self.cleaned_data['date'].split("-")
        # document_type = self.cleaned_data['document_type']
        # document_id = self.cleaned_data['document_id']
        # task_type = self.cleaned_data['task_type']
        # email = self.cleaned_data['email']
        name = self.cleaned_data['name']

        my_task = PeriodicTask.objects.get(name=name)

        my_task.crontab.minute = 30
        my_task.crontab.hour = 8
        my_task.crontab.day_of_month = day
        my_task.crontab.month_of_year = month

        my_task.save()

        return my_task

     




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
            _, _ = to_pending_schedule.save()

        to_unpaid_schedule = ScheduleForm(to_unpaid_details)
        if to_unpaid_schedule.is_valid():
            _, _ = to_unpaid_schedule.save()
    
    else:
        email_notif_schedule = ScheduleForm(email_notif_details)
        if email_notif_schedule.is_valid():
            _, _ = email_notif_schedule.update()


        to_pending_schedule = ScheduleForm(to_pending_details)
        if to_pending_schedule.is_valid():
            _, _ = to_pending_schedule.update()

        to_unpaid_schedule = ScheduleForm(to_unpaid_details)
        if to_unpaid_schedule.is_valid():
            _, _ = to_unpaid_schedule.update()



def delete_tasks(email, doc_type, doc_id):
    for task_type in ["to pending", "to unpaid", "email notif"]:
        name = get_task_name(email, doc_type, doc_id, task_type)
        try:
            p_task = PeriodicTask.objects.get(name=name)
            p_task.delete()
        except Exception as e:
            print(e)

