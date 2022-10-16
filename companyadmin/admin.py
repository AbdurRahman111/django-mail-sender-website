from django.contrib import admin
from .models import company_subscription_admin

from import_export.admin import ImportExportModelAdmin



# Register your models here.
class search_bar(ImportExportModelAdmin):
    search_fields = ('company_id', 'subscription_id')

admin.site.register(company_subscription_admin, search_bar)