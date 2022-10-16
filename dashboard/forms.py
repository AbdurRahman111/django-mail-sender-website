from django.forms import ModelForm
from .models import Company_Emails


class form_Company_Emails(ModelForm):
    class Meta:
        model = Company_Emails
        fields = ['To', 'Subject', 'Textbox', 'Status']

