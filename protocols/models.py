from django.db import models
from django.utils import timezone

# Create your models here.
class Protocol(models.Model):
    proto_header = models.CharField(max_length=256)
    proto_regdate = models.DateField(null=False, default=timezone.now, db_index=True)
    proto_regnum = models.CharField(max_length=16, null=True, db_index=True, blank=True)
    proto_place = models.CharField(max_length=32,null=True)
    proto_date = models.CharField(max_length=32, null=True)
    proto_preambula = models.TextField(blank=True)
    proto_fabula = models.TextField(blank=True)
    proto_fio = models.CharField(max_length=64, blank=True)
    proto_dol = models.CharField(max_length=128, blank=True)

    class Meta:
        verbose_name = 'Протокол'
        verbose_name_plural = 'Протоколы'

    def __str__(self):
         return  self.proto_header

class Decision(models.Model):
    protocol = models.ForeignKey('Protocol', on_delete=models.CASCADE)
    dec_type = models.IntegerField(default=0)
    dec_text = models.TextField(blank=True)
    dec_date = models.DateField(db_index=True)
    dec_always = models.IntegerField(default=0)
    dec_dep = models.CharField(max_length=64, blank=True)
    dec_performers = models.CharField(max_length=256, blank=True)