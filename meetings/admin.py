from django.contrib import admin
from meetings.models import Meeting, Member, Dep, Studio, Item
# Register your models here.


class MemberInline(admin.TabularInline):
    model = Member
    extra = 1

class Meeting_admin(admin.ModelAdmin):
    list_display = ('meet_type', 'meet_place', 'meet_subj', 'meet_lead', 'meet_date')
    inlines = (MemberInline,)

class Member_admin(admin.ModelAdmin):
    list_display = ('fio', 'dol', 'dep')
    # inlines = (Meeting_MemberInline,)

class Dep_admin(admin.ModelAdmin):
    list_display = ('name',)

class Studio_admin(admin.ModelAdmin):
    list_display = ('dep', 'studio_addr', 'studio_type')

class Item_admin(admin.ModelAdmin):
    list_display = ('item_subj', 'item_time', 'dep', 'f', 'i', 'o', 'dol')


admin.site.register(Meeting, Meeting_admin)
admin.site.register(Member, Member_admin)
admin.site.register(Dep, Dep_admin)
admin.site.register(Studio, Studio_admin)
admin.site.register(Item, Item_admin)