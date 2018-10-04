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
    members = models.ManyToManyField('Member', through='Meeting_Member')
    studios = models.ManyToManyField('Studio')

    def __str__(self):
         return  str(self.meet_date) +' | '+ self.meet_subj


class MeetingForm(ModelForm):
    class Meta:
        model = Meeting
        fields = ['meet_type', 'meet_subj', 'meet_date', 'meet_start','meet_end', 'meet_place', 'meet_lead', 'meet_init', 'meet_acc', 'meet_tel']

class Member(models.Model):
    f = models.CharField(max_length=32,db_index=True)
    i = models.CharField(max_length=32, db_index=True)
    o = models.CharField(max_length=32, db_index=True, blank=True)
    fio = models.CharField(max_length=64, db_index=True)
    dol = models.CharField(max_length=128, db_index=True)
    dep = models.ForeignKey('Dep',db_index=True, null=True, on_delete=models.SET_NULL)
    is_speaker = models.BooleanField(default=False);

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

class Item(models.Model):
    otv = models.ForeignKey('Member', db_index=True, null=True, on_delete=models.SET_NULL)
    meet = models.ForeignKey('Meeting', db_index=True, on_delete=models.CASCADE)
    description = models.CharField(max_length=256)
    tm = models.CharField(max_length=16, db_index=True)

    def __str__(self):
        return self.description

class Meeting_Member(models.Model):
    meeting = models.ForeignKey('Meeting', db_index=True, on_delete=models.CASCADE)
    member = models.ForeignKey('Member', db_index=True, on_delete=models.CASCADE)
    order_n = models.IntegerField(null=False, default=0)