# Generated by Django 4.0.6 on 2022-10-07 16:47

import ckeditor.fields
import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company_Emails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('From', models.CharField(max_length=255)),
                ('To', models.CharField(max_length=255)),
                ('Subject', models.CharField(max_length=255)),
                ('Textbox', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('Status', models.CharField(choices=[('Draft', 'Draft'), ('Send', 'Send')], default='', max_length=255)),
                ('Time', models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 7, 22, 47, 13, 632170))),
            ],
            options={
                'verbose_name_plural': 'Emails',
            },
        ),
    ]
