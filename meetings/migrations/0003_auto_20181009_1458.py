# Generated by Django 2.1.2 on 2018-10-09 11:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0002_auto_20181009_1425'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meeting',
            name='meet_init',
        ),
        migrations.RemoveField(
            model_name='meeting',
            name='meet_lead',
        ),
        migrations.RemoveField(
            model_name='meeting',
            name='meet_place',
        ),
    ]