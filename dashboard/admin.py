from django.contrib import admin
from .models import Company_Emails, track_mail_open
# Register your models here.


class show_Company_Emails(admin.ModelAdmin):
    list_display = ['To', 'Subject', 'Time']
admin.site.register(Company_Emails, show_Company_Emails)

class show_track_mail_open(admin.ModelAdmin):
    list_display = ['email', 'seen_at', 'key', 'request']
admin.site.register(track_mail_open, show_track_mail_open)