from django.db import models
from django.forms import ModelForm
from django.utils import timezone

mVideo = 'V'
mAudio = 'A'
mInternal = 'I'

MEETING_TYPE_CHOICES = (
    (mVideo, 'Видео конференция'),
    (mAudio, 'Аудио селектор'),
    (mInternal, 'Очное совещание'),
)

STUDIO_TYPE_CHOICES = (
    (mVideo, 'Видео'),
    (mAudio, 'Аудио'),
)

class Meeting(models.Model):
    meet_type = models.CharField(max_length=1, choices=MEETING_TYPE_CHOICES, default=mInternal)
    meet_subj = models.CharField(max_length=128, db_index=True)
    meet_date = models.DateField(null=False, default=timezone.now)
    meet_start = models.CharField(max_length=5,null=True)
    meet_end = models.CharField(max_length=5,null=True)
    meet_acc = models.CharField(max_length=64, db_index=True, blank=True)
    meet_tel = models.CharField(max_length=20, blank=True)
    meet_save = models.BooleanField(default=False)
    meet_confident = models.BooleanField(default=False)
    studios = models.ManyToManyField('Studio', through='StudioList')

    class Meta:
        verbose_name = 'Совещание'
        verbose_name_plural = 'Совещания'

    def __str__(self):
         return  str(self.meet_date) +' | '+ self.meet_subj

class Member(models.Model):
    meeting = models.ForeignKey('Meeting', db_index=True, null=True, on_delete=models.CASCADE)
    dep = models.CharField(max_length=64, db_index=True, default='')
    f = models.CharField(max_length=32,db_index=True)
    i = models.CharField(max_length=32, db_index=True)
    o = models.CharField(max_length=32, db_index=True, blank=True)
    fio = models.CharField(max_length=64, db_index=True)
    dol = models.CharField(max_length=128, db_index=True)
    is_speaker = models.IntegerField(default=0)
    is_lead = models.IntegerField(default=0)
    is_init = models.IntegerField(default=0)
    order_n = models.PositiveIntegerField(null=False, default=0)

    def __str__(self):
         return  self.fio

class Employee(models.Model):
    dep = models.ForeignKey('Dep', db_index=True, null=True, on_delete=models.SET_NULL, verbose_name='Организация')
    f = models.CharField(max_length=32,db_index=True, verbose_name='Фамилия')
    i = models.CharField(max_length=32, db_index=True, verbose_name='Имя')
    o = models.CharField(max_length=32, db_index=True, blank=True, verbose_name='Отчество')
    dol = models.CharField(max_length=128, db_index=True, verbose_name='Должность')
    email = models.EmailField(verbose_name='E-Mail', blank=True)
    tel = models.CharField(max_length=16, verbose_name='Телефон', blank=True)

    def __str__(self):
         return  self.f+' '+self.i+' '+self.o+' '

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

class Dep(models.Model):
    name = models.CharField(max_length=64, db_index=True, verbose_name='Организация')

    class Meta:
        verbose_name = 'Организацию'
        verbose_name_plural = 'Организации'

    def __str__(self):
        return self.name

class Studio(models.Model):
    dep = models.ForeignKey('Dep', db_index=True, null=True, on_delete=models.SET_NULL, verbose_name='Организация')
    studio_addr = models.CharField(max_length=256, db_index=True, verbose_name='Адрес студии')
    studio_type = models.CharField(max_length=1, choices=STUDIO_TYPE_CHOICES, default=mVideo, verbose_name='Тип студии')

    class Meta:
        verbose_name = 'Студию'
        verbose_name_plural = 'Студии'

    def __str__(self):
        return self.dep.name+' / '+self.studio_addr+' / '+self.studio_type

class StudioList(models.Model):
    meeting = models.ForeignKey('Meeting', db_index=True, null=True, on_delete=models.CASCADE)
    studio = models.ForeignKey('Studio', db_index=True, null=True, on_delete=models.CASCADE)
    order_n = models.PositiveIntegerField(null=False, default=0)

class Item(models.Model):
    meeting = models.ForeignKey('Meeting', db_index=True, null=True, on_delete=models.CASCADE)
    item_subj = models.CharField(max_length=256)
    item_time = models.CharField(max_length=16, db_index=True)
    dep = models.CharField(max_length=64, db_index=True, default='')
    f = models.CharField(max_length=32,db_index=True)
    i = models.CharField(max_length=32, db_index=True)
    o = models.CharField(max_length=32, db_index=True, blank=True)
    dol = models.CharField(max_length=128, db_index=True)
    order_n = models.PositiveIntegerField(null=False, default=0)

    def __str__(self):
        return self.item_subj+' / '+self.item_time

class Check(models.Model):
    meeting = models.ForeignKey('Meeting', on_delete=models.CASCADE)
    p1_4 = models.IntegerField(default=0)
    p2_4 = models.IntegerField(default=0)
    p3_4 = models.IntegerField(default=0)
    p4_4 = models.IntegerField(default=0)
    p5_1 = models.IntegerField(default=0)
    p5_2 = models.IntegerField(default=0)
    p5_3 = models.IntegerField(default=0)
    p5_4 = models.IntegerField(default=0)
    p6_2 = models.IntegerField(default=0)
    p6_4 = models.IntegerField(default=0)
    p7_4 = models.IntegerField(default=0)
    p8_4 = models.IntegerField(default=0)
    p9_1 = models.IntegerField(default=0)
    p9_4 = models.IntegerField(default=0)
    p10_4 = models.IntegerField(default=0)
    p11_4 = models.IntegerField(default=0)
