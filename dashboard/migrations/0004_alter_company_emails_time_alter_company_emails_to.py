# Generated by Django 4.0.6 on 2022-10-08 11:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_alter_company_emails_time_alter_company_emails_to'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company_emails',
            name='Time',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 8, 17, 45, 7, 525536)),
        ),
        migrations.AlterField(
            model_name='company_emails',
            name='To',
            field=models.CharField(max_length=255),
        ),
    ]
