# Generated by Django 2.1.2 on 2018-10-07 08:54

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dep',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=256)),
                ('tm', models.CharField(db_index=True, max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meet_type', models.CharField(choices=[('V', 'Видео конференция'), ('A', 'Аудио селектор'), ('I', 'Очное совещание')], default='I', max_length=1)),
                ('meet_place', models.CharField(db_index=True, max_length=128)),
                ('meet_subj', models.CharField(db_index=True, max_length=128)),
                ('meet_lead', models.CharField(blank=True, db_index=True, max_length=128)),
                ('meet_date', models.DateField(default=django.utils.timezone.now)),
                ('meet_start', models.CharField(max_length=5, null=True)),
                ('meet_end', models.CharField(max_length=5, null=True)),
                ('meet_init', models.CharField(blank=True, db_index=True, max_length=64)),
                ('meet_acc', models.CharField(blank=True, db_index=True, max_length=64)),
                ('meet_tel', models.CharField(blank=True, max_length=20)),
                ('meet_save', models.BooleanField(default=False)),
                ('meet_confident', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Meeting_Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_n', models.IntegerField(default=0)),
                ('meeting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meetings.Meeting')),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('f', models.CharField(db_index=True, max_length=32)),
                ('i', models.CharField(db_index=True, max_length=32)),
                ('o', models.CharField(blank=True, db_index=True, max_length=32)),
                ('fio', models.CharField(db_index=True, max_length=64)),
                ('dol', models.CharField(db_index=True, max_length=128)),
                ('is_speaker', models.BooleanField(default=False)),
                ('dep', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='meetings.Dep')),
            ],
        ),
        migrations.CreateModel(
            name='Studio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('studio_addr', models.CharField(db_index=True, max_length=256)),
                ('studio_type', models.CharField(choices=[('V', 'Видео'), ('A', 'Аудио')], default='V', max_length=1)),
                ('dep', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='meetings.Dep')),
            ],
        ),
        migrations.AddField(
            model_name='meeting_member',
            name='member',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meetings.Member'),
        ),
        migrations.AddField(
            model_name='meeting',
            name='members',
            field=models.ManyToManyField(through='meetings.Meeting_Member', to='meetings.Member'),
        ),
        migrations.AddField(
            model_name='meeting',
            name='studios',
            field=models.ManyToManyField(to='meetings.Studio'),
        ),
        migrations.AddField(
            model_name='item',
            name='meet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meetings.Meeting'),
        ),
        migrations.AddField(
            model_name='item',
            name='otv',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='meetings.Member'),
        ),
    ]
