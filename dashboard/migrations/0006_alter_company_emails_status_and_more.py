# Generated by Django 4.0.6 on 2022-10-09 13:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_alter_company_emails_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company_emails',
            name='Status',
            field=models.CharField(choices=[('Draft', 'Draft'), ('Send', 'Send'), ('Bounced', 'Bounced')], default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='company_emails',
            name='Time',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 9, 19, 8, 21, 705297)),
        ),
    ]
