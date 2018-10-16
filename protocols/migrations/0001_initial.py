# Generated by Django 2.1.2 on 2018-10-16 10:51

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Decision',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dec_type', models.IntegerField(default=0)),
                ('dec_text', models.TextField(blank=True)),
                ('dec_date', models.DateField(db_index=True)),
                ('dec_always', models.IntegerField(default=0)),
                ('dec_dep', models.CharField(blank=True, max_length=64)),
                ('dec_performers', models.CharField(blank=True, max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Protocol',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('proto_header', models.CharField(max_length=256)),
                ('proto_regdate', models.DateField(db_index=True, default=django.utils.timezone.now)),
                ('proto_regnum', models.CharField(blank=True, db_index=True, max_length=16, null=True)),
                ('proto_place', models.CharField(max_length=32, null=True)),
                ('proto_date', models.CharField(max_length=32, null=True)),
                ('proto_preambula', models.TextField(blank=True)),
                ('proto_fabula', models.TextField(blank=True)),
                ('proto_fio', models.CharField(blank=True, max_length=64)),
                ('proto_dol', models.CharField(blank=True, max_length=128)),
            ],
            options={
                'verbose_name': 'Протокол',
                'verbose_name_plural': 'Протоколы',
            },
        ),
        migrations.AddField(
            model_name='decision',
            name='protocol',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='protocols.Protocol'),
        ),
    ]
