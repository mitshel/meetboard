# Generated by Django 2.1.2 on 2018-10-18 13:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('protocols', '0008_protocol_meeting'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='protocol',
            name='meeting',
        ),
    ]
