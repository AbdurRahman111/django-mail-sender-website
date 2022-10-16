# Generated by Django 3.2.16 on 2022-10-16 13:30

import datetime
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0010_auto_20221016_1838'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='track_mail_open',
            name='id',
        ),
        migrations.AlterField(
            model_name='company_emails',
            name='Time',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 16, 19, 30, 45, 243053)),
        ),
        migrations.AlterField(
            model_name='track_mail_open',
            name='key',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]