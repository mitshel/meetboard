# Generated by Django 2.1.2 on 2018-10-16 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('protocols', '0002_auto_20181016_1619'),
    ]

    operations = [
        migrations.AlterField(
            model_name='decision',
            name='dec_type',
            field=models.IntegerField(choices=[(0, 'Пункт'), (1, 'Разделитель')], default=1),
        ),
    ]