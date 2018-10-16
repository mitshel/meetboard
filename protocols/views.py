from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.db.models import Count, F, Q

from mb_auth.views import mb_login
from protocols.models import Protocol, Decision
from meetings.models import Employee

# Create your views here.
@mb_login(url='login')
def proto_table(request):
    args={}
    args['employees'] = Employee.objects.all().order_by('f','i','o','dol')
    args['protocols'] = Protocol.objects.all().\
        annotate(decisions_cnt=Count('decision')). \
        order_by('-proto_regdate','-proto_regnum')
    return render(request,'pt_table.html', args)

@mb_login(url='login')
def proto_delete(request, proto_id=None):
    Protocol.objects.filter(id=proto_id).delete()
    return redirect(reverse("protocols:table"))

@mb_login(url='login')
def proto_update(request, proto_id=None):
    return redirect(reverse("protocols:table"))

@mb_login(url='login')
def proto_copy(request, proto_id=None):
    return redirect(reverse("protocols:table"))

@mb_login(url='login')
def proto_check(request, proto_id=None):
    return redirect(reverse("protocols:table"))