# Generated by Django 2.1.2 on 2018-10-17 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('protocols', '0005_decision_order_n'),
    ]

    operations = [
        migrations.AddField(
            model_name='decision',
            name='dec_date',
            field=models.DateField(null=True),
        ),
    ]