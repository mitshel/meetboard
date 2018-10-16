import datetime

from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.db.models import Count, F, Q
from django.template.context_processors import csrf

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
    args={}
    args.update(csrf(request))
    proto =  None
    try:
        proto_id=int(proto_id)
    except:
        proto_id=0

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        if request.POST:
            proto_header = request.POST.get('proto_header')
            proto_regdate = request.POST.get('proto_regdate')
            proto_regdate = datetime.datetime.strptime(proto_regdate, '%d.%m.%Y').date()
            proto_regnum = request.POST.get('proto_regnum')
            proto_place = request.POST.get('proto_place')
            proto_date = request.POST.get('proto_date')
            proto_preambula = request.POST.get('proto_preambula')
            proto_fabula = request.POST.get('proto_fabula')
            proto_fio = request.POST.get('proto_fio')
            proto_dol = request.POST.get('proto_dol')

            # Если произошло копирование протокола, то opt_id содержит ID старого совещания
            try:
                opt_id = request.POST.get('opt_id',0)
            except:
                opt_id=0

            if proto_id:
                Protocol.objects.filter(id=proto_id).update(proto_header=proto_header,proto_regdate=proto_regdate,
                                                            proto_regnum=proto_regnum, proto_place=proto_place, proto_date=proto_date,
                                                            proto_preambula=proto_preambula, proto_fabula=proto_fabula,
                                                            proto_fio=proto_fio, proto_dol=proto_dol)
            else:
                proto_id=Protocol.objects.create(proto_header=proto_header,proto_regdate=proto_regdate,
                                                        proto_regnum=proto_regnum, proto_place=proto_place, proto_date=proto_date,
                                                        proto_preambula=proto_preambula, proto_fabula=proto_fabula,
                                                        proto_fio=proto_fio, proto_dol=proto_dol).id

            return redirect(reverse("protocols:table"))

    if proto_id:
        try:
            proto = Protocol.objects.get(id=proto_id)
        except Protocol.DoesNotExist:
            proto = None

    args['employees'] = Employee.objects.all().order_by('f', 'i', 'o').values('f', 'i', 'o','dol')
    args['proto']=proto
    args['proto_id'] = proto_id

    return render(request,'pt_protoform.html', args)


@mb_login(url='login')
def proto_copy(request, proto_id=None):
    args = {}
    opt =  None
    if proto_id:
        try:
            opt = Protocol.objects.get(id=int(proto_id))
        except Protocol.DoesNotExist:
            opt = None

    args['employees'] = Employee.objects.all().order_by('f', 'i', 'o').values('f', 'i', 'o', 'dol')
    args['proto']=opt
    args['proto_id'] = None

    return render(request,'pt_protoform.html', args)

@mb_login(url='login')
def proto_check(request, proto_id=None):
    return redirect(reverse("protocols:table"))