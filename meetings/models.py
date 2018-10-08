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
    meet_place = models.CharField(max_length=128,db_index=True)
    meet_subj = models.CharField(max_length=128, db_index=True)
    meet_lead = models.CharField(max_length=128, db_index=True, blank=True)
    meet_date = models.DateField(null=False, default=timezone.now)
    meet_start = models.CharField(max_length=5,null=True)
    meet_end = models.CharField(max_length=5,null=True)
    meet_init = models.CharField(max_length=64, db_index=True, blank=True)
    meet_acc = models.CharField(max_length=64, db_index=True, blank=True)
    meet_tel = models.CharField(max_length=20, blank=True)
    meet_save = models.BooleanField(default=False)
    meet_confident = models.BooleanField(default=False)
    studios = models.ManyToManyField('Studio')

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
    order_n = models.PositiveIntegerField(null=False, default=0)

    def __str__(self):
         return  self.fio

class Dep(models.Model):
    name = models.CharField(max_length=64, db_index=True)

    def __str__(self):
        return self.name

class Studio(models.Model):
    dep = models.ForeignKey('Dep', db_index=True, null=True, on_delete=models.SET_NULL)
    studio_addr = models.CharField(max_length=256, db_index=True)
    studio_type = models.CharField(max_length=1, choices=STUDIO_TYPE_CHOICES, default=mVideo)

    def __str__(self):
        return self.studio_addr

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
        return self.description
