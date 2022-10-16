from django.db import models

# Create your models here.
from datetime import datetime
from ckeditor.fields import RichTextField

import secrets

import uuid



class Company_Emails(models.Model):
    class Meta:
        verbose_name_plural = 'Emails'

    user_id = models.CharField(default='', max_length=255, blank=True, null=True)
    company_id = models.CharField(default='', max_length=255, blank=True, null=True)
    subscription_id = models.CharField(default='', max_length=255, blank=True, null=True)
    From = models.CharField(max_length=255, blank=True, null=True)
    To = models.CharField(max_length=255)
    Subject = models.CharField(max_length=255)
    Textbox = RichTextField(blank=True, null=True)
    email_status = (
        ("", ""),
        ("Draft", "Draft"),
        ("Send", "Send"),
        ("Bounced", "Bounced"),
    )
    Status = models.CharField(max_length=255, choices=email_status, default="")
    Time = models.DateTimeField(default=datetime.now(), blank=True)
    Seen = models.BooleanField(default=False)
    Seen_At = models.DateTimeField(default=None, blank=True, null=True)

    def __str__(self):
        return self.To



class track_mail_open(models.Model):
    email = models.ForeignKey(Company_Emails, on_delete=models.CASCADE, null=True, blank=True)
    key = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False)
    seen_at = models.DateTimeField(null=True, blank=True)
    request = models.TextField(null=True, blank=True)