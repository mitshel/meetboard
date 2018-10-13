# Generated by Django 2.1.2 on 2018-10-10 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0003_auto_20181009_1458'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dep', models.CharField(db_index=True, default='', max_length=64)),
                ('f', models.CharField(db_index=True, max_length=32)),
                ('i', models.CharField(db_index=True, max_length=32)),
                ('o', models.CharField(blank=True, db_index=True, max_length=32)),
                ('dol', models.CharField(db_index=True, max_length=128)),
                ('email', models.EmailField(max_length=254)),
                ('tel', models.CharField(max_length=16)),
            ],
            options={
                'verbose_name': 'Сотрудник',
                'verbose_name_plural': 'Сотрудники',
            },
        ),
        migrations.AlterModelOptions(
            name='dep',
            options={'verbose_name': 'Организацию', 'verbose_name_plural': 'Организации'},
        ),
        migrations.AlterModelOptions(
            name='meeting',
            options={'verbose_name': 'Совещание', 'verbose_name_plural': 'Совещания'},
        ),
        migrations.AlterModelOptions(
            name='studio',
            options={'verbose_name': 'Студию', 'verbose_name_plural': 'Студии'},
        ),
    ]