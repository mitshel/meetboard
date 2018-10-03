# Generated by Django 2.1.2 on 2018-10-03 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0003_auto_20181003_1558'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meeting',
            name='meet_attrs',
        ),
        migrations.AddField(
            model_name='meeting',
            name='meet_confident',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='meeting',
            name='meet_save',
            field=models.BooleanField(default=False),
        ),
    ]
