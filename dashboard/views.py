from django.shortcuts import render, redirect, HttpResponse
from companyadmin.models import company_subscription_admin
from companyadmin.encryption_util import *
from dashboard.models import Company_Emails, track_mail_open
# Create your views here.
from django.contrib import messages
from .forms import form_Company_Emails
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
import csv
from django.core import serializers
from django.http import JsonResponse
import json
import math
from django.core.mail import send_mail

from django.conf import settings
from django.template.loader import render_to_string

import html
from datetime import datetime

from django.conf import settings

from django.utils.translation import override
import json
import os
from django.http import HttpResponse


from django.contrib.sites.shortcuts import get_current_site



from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse
from PIL import Image
from rest_framework.decorators import api_view
from django.template import Context
from django.template.loader import get_template



def home(request):
    return render(request, 'error_pages/error-404.html')


def dashboard(request):
    # send_mail(
    #     'var_form.Subject',
    #     'var_form.Textbox',
    #     '',
    #     ['mdabdurrahmanchowdhury1122@gmail.com'],
    #     fail_silently=False,
    # )
    company_id = request.GET.get('company_id')
    subscription_id = request.GET.get('subscription_id')
    user = request.GET.get('user')
    try:
        if company_id[:10] == "encrypted-":
            user = decrypt(user)
            company_id = decrypt(company_id)
            subscription_id = decrypt(subscription_id)
        else:
            user = encrypt(user)
            company_id = encrypt(company_id)
            subscription_id = encrypt(subscription_id)
            return redirect(f'/dashboard/?user={user}&company_id={company_id}&subscription_id={subscription_id}')
    except:
        pass


    if company_subscription_admin.objects.filter(User_id=user, company_id=company_id, subscription_id=subscription_id):



        all_mails = Company_Emails.objects.filter(user_id=user, company_id=company_id,
                                                     subscription_id=subscription_id).count()

        qty_sents = Company_Emails.objects.filter(Status="Send", user_id=user, company_id=company_id,
                                                     subscription_id=subscription_id).count()

        qty_drafts = Company_Emails.objects.filter(Status="Draft", user_id=user, company_id=company_id,
                                                  subscription_id=subscription_id).count()

        qty_bounced = Company_Emails.objects.filter(Status="Bounced", user_id=user, company_id=company_id,
                                                  subscription_id=subscription_id).count()

        print('all_mails, qty_sents, qty_drafts, qty_bounced')
        print(all_mails, qty_sents, qty_drafts, qty_bounced)


        if all_mails == 0:
            sent_percantage = 0
            draft_percantage = 0
            bounce_percantage = 0
        else:
            sent_percantage = (qty_sents * 100)/all_mails
            sent_percantage = "{:.2f}".format(sent_percantage)
            draft_percantage = (qty_drafts * 100)/all_mails
            draft_percantage = "{:.2f}".format(draft_percantage)
            bounce_percantage = (qty_bounced * 100)/all_mails
            bounce_percantage = "{:.2f}".format(bounce_percantage)


        context = {'user':user, 'company_id':company_id, 'subscription_id':subscription_id, 'qty_sents':qty_sents, 'qty_drafts':qty_drafts, 'qty_bounced':qty_bounced, 'all_mails':all_mails, 'sent_percantage':sent_percantage, 'draft_percantage':draft_percantage, 'bounce_percantage':bounce_percantage}
        return render(request, 'dashboard/index.html', context)
    else:
        return render(request, 'error_pages/error.html')




def company_register(request):
    company_id = request.GET.get('company_id')
    subscription_id = request.GET.get('subscription_id')
    user = request.GET.get('user')

    if company_id[:10] == "encrypted-":
        user = decrypt(user)
        company_id = decrypt(company_id)
        subscription_id = decrypt(subscription_id)
    else:
        user = encrypt(user)
        company_id = encrypt(company_id)
        subscription_id = encrypt(subscription_id)
        return redirect(f'/dashboard/register?user={user}&company_id={company_id}&subscription_id={subscription_id}')
    if company_id and subscription_id and user:
        check_user = company_subscription_admin.objects.filter(company_id=company_id, subscription_id=subscription_id)
        if check_user:
            return HttpResponse('''Subscription Id is Already Exist!''')
        else:
            register_admin = company_subscription_admin(User_id=user, company_id=company_id, subscription_id=subscription_id)
            register_admin.save()
            messages.success(request, "Successfully Register As a Company Admin!")

            context = {'user': register_admin.User_id, 'company_id': company_id, 'subscription_id': subscription_id}
            # return render(request, 'admindashboard/admindashboard.html', context)
            return redirect(f'/dashboard/?user={register_admin.User_id}&company_id={company_id}&subscription_id={subscription_id}')
    else:
        return HttpResponse('''To Register You Have to pass user, company_id and subscription_id parameter!''')





def compose_mail(request):
    company_id = request.GET.get('company_id')
    subscription_id = request.GET.get('subscription_id')
    user = request.GET.get('user')


    if company_id[:10] == "encrypted-":
        user = decrypt(user)
        company_id = decrypt(company_id)
        subscription_id = decrypt(subscription_id)
    else:
        user = encrypt(user)
        company_id = encrypt(company_id)
        subscription_id = encrypt(subscription_id)
        return redirect(f'/dashboard/compose_mail?user={user}&company_id={company_id}&subscription_id={subscription_id}')

    if company_subscription_admin.objects.filter(User_id=user, company_id=company_id, subscription_id=subscription_id):
        form = form_Company_Emails()

        context = {'user':user, 'company_id':company_id, 'subscription_id':subscription_id, 'form':form}
        return render(request, 'dashboard/compose_mail.html', context)
    else:
        return render(request, 'error_pages/error.html')





def compose_single_email(request):
    company_id = request.POST.get('company_id')
    subscription_id = request.POST.get('subscription_id')
    user = request.POST.get('user')



    form = form_Company_Emails(request.POST)
    if form.is_valid():
        var_form = form.save(commit=False)
        var_form.user_id = user
        var_form.company_id = company_id
        var_form.subscription_id = subscription_id
        var_form.From = settings.EMAIL_HOST_USER
        var_form.save()

        var_status = var_form.Status
        body_content = var_form.Textbox


        email_text_plain = render_to_string('email_template/mail_body.txt', {'body_content':body_content})

        var_track_mail_open = track_mail_open(email=var_form)
        var_track_mail_open.save()

        site = get_current_site(request)
        domain = site.domain
        # print(domain)

        email_body = render_to_string('email_template/mail_body.html', {'body_content':body_content, 'var_track_mail_open':var_track_mail_open, 'domain':domain})
        mail_body_final = html.unescape(email_body)

        # mail_template = get_template("mail_template.html")

        # context_data_is = dict()
        # context_data_is["image_url"] = request.build_absolute_uri(("render_image"))
        # url_is = context_data_is["image_url"]
        # context_data_is['url_is'] = url_is


        # html_detail = mail_body_final.render(context_data_is)
        #
        # subject, from_email, to = "Greetings !!", 'postmaster@manojadhikary.com.np', [target_user_email]
        # msg = EmailMultiAlternatives(subject, html_detail, from_email, to)
        # msg.content_subtype = 'html'
        # msg.send()
        # return Response({"success": True})




        if var_status == "Send":
            send_mail(
                var_form.Subject,
                '',
                settings.EMAIL_HOST_USER,
                [var_form.To],
                html_message=mail_body_final,
                fail_silently=False,
            )
        elif var_status == "Draft":
            pass
        elif var_status == "Bounced":
            pass

        messages.success(request, f'Email {var_form.Status} Successfully !')

        return redirect(f'/dashboard/compose_mail?user={user}&company_id={company_id}&subscription_id={subscription_id}')






@csrf_exempt
def send_mail_save_data(request):
    var_to = request.POST.get('var_to')
    var_customer_name = request.POST.get('var_customer_name')

    var_id_user = request.POST.get('var_id_user')
    var_id_company_id = request.POST.get('var_id_company_id')
    var_id_subscription_id = request.POST.get('var_id_subscription_id')

    var_ckeditor_text = request.POST.get('var_ckeditor_text')
    # print(var_ckeditor_text)
    var_ckeditor_text = f'<h2>Hello {var_customer_name},</h2>' + var_ckeditor_text
    # print(var_ckeditor_text)

    var_bulk_subject_id = request.POST.get('var_bulk_subject_id')
    # print('var_ckeditor_text')
    # print(var_ckeditor_text)

    # print('var_to, var_subject, var_textbox, var_status')
    # print(var_to, var_subject, var_textbox, var_status)
    #
    # if var_status == "Draft" or var_status == "draft":
    #     var_status = "Draft"
    # elif var_status == "Send" or var_status == "send":
    #     var_status = "Send"
    # elif var_status == "Bounced" or var_status == "bounced":
    #     var_status = "Bounced"
    # else:
    #     var_status = "Send"

    var_Company_Emails = Company_Emails(user_id=var_id_user, company_id=var_id_company_id, subscription_id=var_id_subscription_id, From=settings.EMAIL_HOST_USER,To=var_to, Subject=var_bulk_subject_id, Textbox=var_ckeditor_text, Status="Send")
    var_Company_Emails.save()

    body_content = var_Company_Emails.Textbox

    var_track_mail_open = track_mail_open(email=var_Company_Emails)
    var_track_mail_open.save()

    site = get_current_site(request)
    domain = site.domain
    # print(domain)

    email_body = render_to_string('email_template/mail_body.html',
                                  {'body_content': body_content, 'var_track_mail_open':var_track_mail_open, 'domain':domain})
    mail_body_final = html.unescape(email_body)

    try:
        if var_Company_Emails.Status == "Send":
            send_mail(
                var_bulk_subject_id,
                '',
                settings.EMAIL_HOST_USER,
                [var_to],
                html_message=mail_body_final,
                fail_silently=False,
            )
    except:

        var_Company_Emails.Status = "Bounced"
        var_Company_Emails.save()



    # Company_Emails.objects.all().delete()

    finish_status = var_Company_Emails.Status

    # csv_file_data = serializers.serialize('json', finish_status)
    # return JsonResponse(csv_file_data, safe=False)
    return HttpResponse(finish_status)




def track_mail(request, key):

    META = {
        header: value
        for header, value in request.META.items()
        if header.startswith(("HTTP_", "REMOTE_"))
    }
    if track_mail_open.objects.filter(key=key, seen_at=None):
        var_tract_var = track_mail_open.objects.get(key=key, seen_at=None)
        var_tract_var.request = json.dumps(META)
        var_tract_var.seen_at = datetime.now()
        var_tract_var.save()

        get_email = Company_Emails.objects.get(id=var_tract_var.email.id)
        get_email.Seen = True
        get_email.Seen_At = datetime.now()
        get_email.save()
        print("Successfully Tracked")

    with open(f'{settings.BASE_DIR}/static/user_logo.png', "rb") as f:
        return HttpResponse(f.read(), content_type="image/png")




def email_seen(request, key):
    print(key)
    META = {
        header: value
        for header, value in request.META.items()
        if header.startswith(("HTTP_", "REMOTE_"))
    }
    track_mail_open.objects.filter(key=key, seen_at=None).update(
        request=json.dumps(META), seen_at=datetime.now()
    )
    print("Successfully Tracketd")
    with open(os.path.dirname(os.path.abspath(__file__)) + "/res/user_logo.png", "rb") as f:
        return HttpResponse(f.read(), content_type="image/png")




@csrf_exempt
def passing_csv_file(request):
    print('data')
    var_upload_csv_mails = request.FILES.get('file_name_mails_csv')
    print(var_upload_csv_mails)

    fs = FileSystemStorage(location='media/mails_csv/')
    filename = fs.save(var_upload_csv_mails.name, var_upload_csv_mails)
    url_file = fs.url(filename)
    print(filename)
    print(url_file)

    with open(f'media/mails_csv/{filename}') as file:
        reader = csv.reader(file)
        next(reader)

        list_1 = []
        print(reader)
        for row in reader:
            print(row)
            list_1.append(row)
        print(list_1)
        csv_file_data = serializers.serialize('json', list_1)
        return JsonResponse(csv_file_data, safe=False)
        # return HttpResponse(json.dumps(csv_file_data), content_type='application/json')





def sent_emails(request, template='dashboard/sent_emails.html', page_template='dashboard/sent_emails_pagination.html'):
    company_id = request.GET.get('company_id')
    subscription_id = request.GET.get('subscription_id')
    user = request.GET.get('user')
    if company_id[:10] == "encrypted-":
        user = decrypt(user)
        company_id = decrypt(company_id)
        subscription_id = decrypt(subscription_id)
    else:
        user = encrypt(user)
        company_id = encrypt(company_id)
        subscription_id = encrypt(subscription_id)
        return redirect(f'/dashboard/sent_emails?user={user}&company_id={company_id}&subscription_id={subscription_id}')

    if company_subscription_admin.objects.filter(User_id=user, company_id=company_id, subscription_id=subscription_id):
        my_mail_send = Company_Emails.objects.filter(Status="Send", user_id=user, company_id=company_id, subscription_id=subscription_id).order_by('-id')
        context = {'user':user,
                   'company_id':company_id,
                   'subscription_id':subscription_id,
                   'my_mails':my_mail_send,
                   'page_template': page_template,}
        if request.is_ajax():
            template = page_template
        return render(request, template, context)
    else:
        return render(request, 'error_pages/error.html')



def draft_mails(request, template='dashboard/draft_mails.html', page_template='dashboard/draft_mails_pagination.html'):
    company_id = request.GET.get('company_id')
    subscription_id = request.GET.get('subscription_id')
    user = request.GET.get('user')
    if company_id[:10] == "encrypted-":
        user = decrypt(user)
        company_id = decrypt(company_id)
        subscription_id = decrypt(subscription_id)
    else:
        user = encrypt(user)
        company_id = encrypt(company_id)
        subscription_id = encrypt(subscription_id)
        return redirect(f'/dashboard/draft_mails?user={user}&company_id={company_id}&subscription_id={subscription_id}')

    if company_subscription_admin.objects.filter(User_id=user, company_id=company_id, subscription_id=subscription_id):
        my_mail_draft = Company_Emails.objects.filter(Status="Draft", user_id=user, company_id=company_id, subscription_id=subscription_id).order_by('-id')
        context = {'user':user, 'company_id':company_id, 'subscription_id':subscription_id, 'my_mails':my_mail_draft, 'page_template': page_template,}
        if request.is_ajax():
            template = page_template
        return render(request, template, context)
    else:
        return render(request, 'error_pages/error.html')


def bounced_mails(request, template='dashboard/bounced_mails.html', page_template='dashboard/bounced_mails_pagination.html'):
    company_id = request.GET.get('company_id')
    subscription_id = request.GET.get('subscription_id')
    user = request.GET.get('user')

    if company_id[:10] == "encrypted-":
        user = decrypt(user)
        company_id = decrypt(company_id)
        subscription_id = decrypt(subscription_id)
    else:
        user = encrypt(user)
        company_id = encrypt(company_id)
        subscription_id = encrypt(subscription_id)
        return redirect(f'/dashboard/bounced_mails?user={user}&company_id={company_id}&subscription_id={subscription_id}')

    if company_subscription_admin.objects.filter(User_id=user, company_id=company_id, subscription_id=subscription_id):
        my_mail_send = Company_Emails.objects.filter(Status="Bounced", user_id=user, company_id=company_id,
                                                     subscription_id=subscription_id).order_by('-id')
        context = {'user':user, 'company_id':company_id, 'subscription_id':subscription_id, 'page_template': page_template, 'my_mails':my_mail_send}
        if request.is_ajax():
            template = page_template
        return render(request, template, context)
    else:
        return render(request, 'error_pages/error.html')



def search_bar(request, template='dashboard/search_result.html', page_template='dashboard/search_result_pagination.html'):
    search_value = request.GET.get('search_value')
    company_id = request.GET.get('company_id')
    subscription_id = request.GET.get('subscription_id')
    user = request.GET.get('user')

    if company_id[:10] == "encrypted-":
        user = decrypt(user)
        company_id = decrypt(company_id)
        subscription_id = decrypt(subscription_id)
    else:
        user = encrypt(user)
        company_id = encrypt(company_id)
        subscription_id = encrypt(subscription_id)
        return redirect(f'/dashboard/search_bar?search_value={search_value}&user={user}&company_id={company_id}&subscription_id={subscription_id}')

    if company_subscription_admin.objects.filter(User_id=user, company_id=company_id, subscription_id=subscription_id):
        my_mail_send = Company_Emails.objects.filter(To__icontains=search_value, user_id=user, company_id=company_id,
                                                     subscription_id=subscription_id).order_by('-id')
        count_search_results = my_mail_send.count()
        context = {'user':user, 'company_id':company_id, 'subscription_id':subscription_id, 'page_template': page_template, 'my_mails':my_mail_send, 'search_value':search_value, 'count_search_results':count_search_results}
        if request.is_ajax():
            template = page_template
        return render(request, template, context)
    else:
        return render(request, 'error_pages/error.html')




def delete_mail(request):
    mail_id = request.GET.get('mail_id')
    company_id = request.GET.get('company_id')
    subscription_id = request.GET.get('subscription_id')
    user = request.GET.get('user')


    if company_id[:10] == "encrypted-":
        mail_id = decrypt(mail_id)
        user = decrypt(user)
        company_id = decrypt(company_id)
        subscription_id = decrypt(subscription_id)
    else:
        mail_id = encrypt(mail_id)
        user = encrypt(user)
        company_id = encrypt(company_id)
        subscription_id = encrypt(subscription_id)
        return redirect(f'/dashboard/delete_mail?mail_id={mail_id}&user={user}&company_id={company_id}&subscription_id={subscription_id}')

    if company_subscription_admin.objects.filter(User_id=user, company_id=company_id, subscription_id=subscription_id):
        get_target_mail = Company_Emails.objects.get(id=mail_id, user_id=user, company_id=company_id, subscription_id=subscription_id).delete()
        # print(get_target_mail)
        print('ranja kaajia')
        last_url = request.META.get('HTTP_REFERER')
        print(last_url[22:])
        messages.success(request, "Successfully Deleted!")

        return redirect(last_url[21:])
        # return render(request, 'error_pages/error.html')
    else:
        return render(request, 'error_pages/error.html')



