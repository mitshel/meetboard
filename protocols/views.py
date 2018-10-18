import datetime
import json
import os
import re

from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.db.models import Count, Avg, F, Q
from django.template.context_processors import csrf
from django.http import HttpResponse
from django.utils import timezone

from meetings.models import Meeting

from mb_auth.views import mb_login
from meetings.models import Employee
from protocols.models import DECISIONS_TYPE_CHOICES, pItem, fabula_prefix, decisions_prefix, Protocol, Decision
from docxtpl import DocxTemplate, RichText

# Create your views here.
@mb_login(url='login')
def proto_table(request, archive=None):
    if archive==None:
        try:
            archive = request.session['proto_archive']
        except:
            archive = 0

    try:
        archive = int(archive)
    except:
        archive = 0

    request.session['proto_archive'] = archive

    args={}
    args['employees'] = Employee.objects.all().order_by('f','i','o','dol')
    args['protocols'] = Protocol.objects.filter(proto_off=archive).\
        annotate(decisions_cnt=Count('decision')). \
        annotate(progress=Avg('decision__dec_progress',filter=Q(decision__dec_type=0))).\
        order_by('-proto_regdate','-proto_regnum')
    args['dec_type_choices'] = DECISIONS_TYPE_CHOICES

    args['proto_archive'] = archive

    return render(request,'pt_table.html', args)

@mb_login(url='login')
def proto_delete(request, proto_id=None):
    try:
        proto = Protocol.objects.get(id=proto_id)
    except:
        proto = None
    if proto:
        if proto.proto_off:
            proto.delete()
        else:
            proto.proto_off = 1
            proto.save()

    return redirect(reverse("protocols:table"))

@mb_login(url='login')
def proto_update(request, proto_id=None, meet_id=None):
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
            proto_header = request.POST.get('proto_header','')
            proto_regdate = request.POST.get('proto_regdate')
            proto_regdate = datetime.datetime.strptime(proto_regdate, '%d.%m.%Y').date()
            proto_regnum = request.POST.get('proto_regnum','')
            proto_place = request.POST.get('proto_place','')
            proto_date = request.POST.get('proto_date','')
            proto_preambula = request.POST.get('proto_preambula','')
            proto_fabula = request.POST.get('proto_fabula','')
            proto_fio = request.POST.get('proto_fio','')
            proto_dol = request.POST.get('proto_dol','')
            proto_fabula_prefix = request.POST.get('proto_fabula_prefix','')
            proto_decisions_prefix = request.POST.get('proto_decisions_prefix', '')
            proto_off = 1 if (request.POST.get('proto_off')) else 0
            try:
                meet_id = int(request.POST.get('proto_meet',None))
            except:
                meet_id = None

            # Если произошло копирование протокола, то opt_id содержит ID старого совещания
            try:
                opt_id = request.POST.get('opt_id',0)
            except:
                opt_id=0

            if proto_id:
                print(meet_id)
                Protocol.objects.filter(id=proto_id).update(proto_header=proto_header,proto_regdate=proto_regdate,
                                                            proto_regnum=proto_regnum, proto_place=proto_place, proto_date=proto_date,
                                                            proto_preambula=proto_preambula, proto_fabula=proto_fabula,
                                                            proto_fio=proto_fio, proto_dol=proto_dol,
                                                            proto_fabula_prefix=proto_fabula_prefix, proto_decisions_prefix=proto_decisions_prefix,
                                                            proto_off=proto_off, meeting_id=meet_id)
            else:
                proto_id=Protocol.objects.create(proto_header=proto_header,proto_regdate=proto_regdate,
                                                        proto_regnum=proto_regnum, proto_place=proto_place, proto_date=proto_date,
                                                        proto_preambula=proto_preambula, proto_fabula=proto_fabula,
                                                        proto_fio=proto_fio, proto_dol=proto_dol,
                                                        proto_fabula_prefix=proto_fabula_prefix, proto_decisions_prefix=proto_decisions_prefix,
                                                        proto_off=proto_off, meeting_id=meet_id).id

            return redirect(reverse("protocols:table"))

    if proto_id:
        try:
            proto = Protocol.objects.get(id=proto_id)
        except Protocol.DoesNotExist:
            proto = None

    args['employees'] = Employee.objects.all().order_by('f', 'i', 'o').values('f', 'i', 'o','dol')
    args['proto']=proto
    args['fabula_prefix']=fabula_prefix
    args['decisions_prefix']=decisions_prefix
    args['proto_id'] = proto_id

    if meet_id:
        args['meet_id'] = meet_id
    elif proto:
        args['meet_id'] = proto.meeting.id if proto.meeting else 0
    else:
        args['meet_id'] = 0

    args['meet'] = Meeting.objects.filter(Q(protocol__meeting_id__isnull=True) | Q(id=args['meet_id'])).order_by('-meet_date')

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
def decisions_update(request):
    res = 1
    if request.method == 'POST':
        if request.POST:
            res = 0
            id_list = []
            proto_id = int(request.POST.get('proto_id',0))
            rowOrder = request.POST.get('decisionsTable_rowOrder',None)
            if rowOrder and proto_id:
                rowOrder = map(int, rowOrder.split(',')) if rowOrder else None
                for index, ordern in enumerate(rowOrder):
                    try:
                        id = int(request.POST.get('decisionsTable_id_{}'.format(ordern),0))
                    except:
                        id = 0

                    dec_performers = request.POST.get('decisionsTable_dec_performers_{}'.format(ordern),'')
                    dec_type = request.POST.get('decisionsTable_dec_type_{}'.format(ordern),'')
                    dec_text = request.POST.get('decisionsTable_dec_text_{}'.format(ordern),'')
                    dec_term = request.POST.get('decisionsTable_dec_term_{}'.format(ordern), '')
                    try:
                        dec_date = datetime.datetime.strptime(dec_term, "%d.%m.%Y").date()
                    except:
                        dec_date = None

                    if id:
                        Decision.objects.filter(id=id).update(dec_performers=dec_performers, dec_type=dec_type,
                                                              dec_text=dec_text, dec_term=dec_term, order_n=index,
                                                              protocol_id=proto_id, dec_date=dec_date)
                    else:
                        id=Decision.objects.create(dec_performers=dec_performers, dec_type=dec_type,
                                                   dec_text=dec_text, dec_term=dec_term, order_n=index,
                                                   protocol_id=proto_id, dec_date=dec_date).id
                    id_list.append(id)

                Decision.objects.filter(protocol_id=proto_id).exclude(id__in=id_list).delete()

    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps({'user':'admin','id':1,'result':res}))
    return response

@mb_login(url='login')
def proto_doc(request, proto_id=None):
    proto_id = int(proto_id) if proto_id else 0
    try:
        protocol = Protocol.objects.get(id=proto_id)
    except:
        protocol = None

    if protocol:
        try: decisions = Decision.objects.filter(protocol__id=proto_id).order_by('order_n')
        except: decisions = []

        filename='protocol{}_{}.docx'.format(proto_id,timezone.now().strftime('%Y%m%d%H%M%S'))
        fullname="media/{}".format(filename)
        doc = DocxTemplate("media/protocol_tpl.docx")
        context = {'protocol': protocol,
                   'decisions': decisions,
                   'proto_header': RichText(protocol.proto_header,size=28,font='Times New Roman'),
                   'proto_preambula': RichText(protocol.proto_preambula,size=28,font='Times New Roman'),
                   'proto_fabula': RichText(protocol.proto_fabula,size=28,font='Times New Roman')
                   }
        doc.render(context)
        doc.save(fullname)

        f = open(fullname, "rb")
        s = f.read()
        response = HttpResponse()
        response["Content-Type"] = '{}; name="{}"'.format('application/msword', filename)
        response["Content-Disposition"] = 'attachment; filename="{}"'.format(filename)
        response["Content-Transfer-Encoding"] = 'binary'
        response["Content-Length"] = str(len(s))
        response.write(s)
        f.close()
        os.remove(fullname)
        return response

@mb_login(url='login')
def decisions_get(request, proto_id=None):
    if request.is_ajax():
        proto_id = int(proto_id) if proto_id else 0

        decisions = Decision.objects.filter(protocol_id=proto_id).order_by('order_n').\
                    values('id','dec_type','dec_text','dec_term','dec_performers','dec_progress','dec_comment','order_n')
        data = json.dumps([dict(item) for item in decisions])
        return HttpResponse(data,'json')

    return proto_table(request)

@mb_login(url='login')
def proto_check(request, proto_id=None):
    args = {}
    proto_id = int(proto_id) if proto_id else 0
    try:
        protocol = Protocol.objects.get(id=proto_id)
    except:
        protocol = None

    decisions = []
    if protocol:
        try: decisions = Decision.objects.filter(protocol__id=proto_id, dec_type=pItem).order_by('order_n')
        except: pass

    args['proto'] = protocol
    args['decisions'] = decisions
    return render(request,'pt_deccheck.html', args)

@mb_login(url='login')
def check_update(request):
    args={}
    args.update(csrf(request))
    res = 1
    if request.method == 'POST':
        if request.POST:
            res = 0
            rowOrder = request.POST.get('rowOrder',None)
            if rowOrder:
                rowOrder = map(int, rowOrder.split(',')) if rowOrder else None
                for index, id in enumerate(rowOrder):
                    dec_progress = int(request.POST.get('dec_progress_{}'.format(id),0))
                    dec_comment = request.POST.get('dec_comment_{}'.format(id), '')
                    Decision.objects.filter(id=id).update(dec_progress=dec_progress, dec_comment=dec_comment)

    return redirect(reverse("protocols:table"))

@mb_login(url='login')
def dec_table(request, complete=2):
    args={}
    decisions = Decision.objects.filter(protocol__proto_off=0, dec_type=0)
    if (complete == 0):
        # Невыполненные поручения
        decisions = decisions.filter(dec_progress__lt=100)
    elif (complete == 1):
        # Выполненные поручения
        decisions = decisions.filter(dec_progress=100)
    elif (complete == 3):
        # Просроченные поручения
        decisions = decisions.filter(dec_progress__lt=100, dec_date__lt=timezone.now())

    decisions = decisions.order_by('-dec_date', '-dec_term')
    args['decisions'] = decisions
    args['complete'] = complete

    return render(request,'pt_decisions.html', args)

@mb_login(url='login')
def store_check(request):
    res = 1
    args={}
    args.update(csrf(request))
    if request.method == 'POST':
        if request.POST:
            res = 0
            dec_id = int(request.POST.get('dec_id', 0))
            dec_progress = int(request.POST.get('dec_progress', 0))
            dec_comment = request.POST.get('dec_comment', '')

            Decision.objects.filter(id=dec_id).update(dec_progress=dec_progress, dec_comment=dec_comment)

    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps({'user': 'admin', 'id': 1, 'result': res}))
    return response

