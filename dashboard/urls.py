from django.urls import path
from . import views


urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('register', views.company_register, name="company_register"),
    path('compose_mail', views.compose_mail, name="compose_mail"),
    path('compose_single_email', views.compose_single_email, name="compose_single_email"),
    path('send_mail_save_data', views.send_mail_save_data, name="send_mail_save_data"),
    path('passing_csv_file', views.passing_csv_file, name="passing_csv_file"),
    path('sent_emails', views.sent_emails, name="sent_emails"),
    path('draft_mails', views.draft_mails, name="draft_mails"),
    path('bounced_mails', views.bounced_mails, name="bounced_mails"),
    path('search_bar', views.search_bar, name="search_bar"),
    path('delete_mail', views.delete_mail, name="delete_mail"),
    path('resend_mail', views.resend_mail, name="resend_mail"),
]