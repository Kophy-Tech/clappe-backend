from django import forms
from django_celery_beat.models import CrontabSchedule, PeriodicTask
import json



class ScheduleForm(forms.Form):
    # time, docuemnt_type, document_id, task_type [one time or periodic], email
    date = forms.CharField()
    document_id = forms.IntegerField()
    document_type = forms.CharField()
    task_type = forms.CharField()
    email = forms.EmailField()

    def save(self):
        _, month, day = self.cleaned_data['date'].split("-")
        document_type = self.cleaned_data['document_type']
        document_id = self.cleaned_data['document_id']
        task_type = self.cleaned_data['task_type']
        email = self.cleaned_data['email']



        new_cron = CrontabSchedule()
        # time should be 8am
        new_cron.minute = 30
        new_cron.hour = 8
        new_cron.day_of_month = day
        new_cron.month_of_year = month

        new_cron.save()
        # print("New crontab created")

        new_task = PeriodicTask()
        new_task.crontab = new_cron

        new_task.args = json.dumps([document_id, document_type])

        if task_type == 'one_time':
            # for due email
            new_task.task = "app.tasks.send_due_mail_task"
            new_task.name = f"Email Notfication for {email} ({document_type.capitalize()} - {document_id})"
            new_task.one_off = True
            new_task.description = f"Email Notfication for {email} ({document_type.capitalize()})"
        
        else:
            # for monthly email
            new_task.task = "app.tasks.send_monthly_mail_task"
            new_task.name = f"Monthly Email Report for {email} ({document_type.capitalize()}  - {document_id})"
            new_task.one_off = False
            new_task.description = f"Monthly Email Report for {email} ({document_type.capitalize()})"

        new_task.save()
        print(f"periodic task created for {email}")

        return new_cron, new_task


    def update(self):

        # when editing a document

        _, month, day = self.cleaned_data['date'].split("-")
        document_type = self.cleaned_data['document_type']
        document_id = self.cleaned_data['document_id']
        task_type = self.cleaned_data['task_type']
        email = self.cleaned_data['email']

        my_task = PeriodicTask.objects.get(args=json.dumps([document_id, document_type]))

        my_task.crontab.minute = 30
        my_task.crontab.hour = 8
        my_task.crontab.day_of_month = day
        my_task.crontab.month_of_year = month

        my_task.save()

        return my_task

     
