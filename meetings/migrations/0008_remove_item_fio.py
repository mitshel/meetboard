# Generated by Django 2.1.2 on 2018-10-08 06:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0007_auto_20181008_0946'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='fio',
        ),
    ]
