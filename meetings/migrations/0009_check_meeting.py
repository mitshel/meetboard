# Generated by Django 2.1.2 on 2018-10-11 07:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0008_check'),
    ]

    operations = [
        migrations.AddField(
            model_name='check',
            name='meeting',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='meetings.Meeting'),
        ),
    ]