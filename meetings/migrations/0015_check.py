# Generated by Django 2.1.2 on 2018-10-12 17:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0014_auto_20181012_1958'),
    ]

    operations = [
        migrations.CreateModel(
            name='Check',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.TextField(default='')),
                ('complete', models.IntegerField(default=0)),
                ('total', models.IntegerField(default=1)),
                ('meeting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meetings.Meeting', unique=True)),
            ],
        ),
    ]