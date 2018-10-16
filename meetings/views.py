import datetime
import json
import os
from docxtpl import DocxTemplate

from django.template.context_processors import csrf
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.db.models import Count, F, Q
from django.utils import timezone

from mb_auth.views import mb_login

from meetings.models import MEETING_TYPE_CHOICES, Meeting, Dep, Member, Item, Studio, StudioList, Employee, Check

@mb_login(url='login')
def Home(request):
    args={}
    args['meetings'] = Meeting.objects.filter(meet_date__gte=timezone.now()). \
                           annotate(complete=F('check__complete'),
                                    total=F('check__total'),
                                    progress=(F('check__complete') * 100 /F('check__total') )). \
                           order_by('meet_date', '-meet_start')[0:3]
    return render(request,'mb_home.html', args)

@mb_login(url='login')
def meet_table(request):
    args={}

    args['employees'] = Employee.objects.all().order_by('f','i','o','dol')
    args['meetings'] = Meeting.objects.all().\
        annotate(members_cnt=Count('member'),items_cnt=Count('item'),studios_cnt=Count('studiolist')). \
        annotate(complete=F('check__complete'),
                 total=F('check__total'),
                 progress=(F('check__complete') * 100 / F('check__total') )). \
        order_by('-meet_date','-meet_start')
    args['deps'] = Dep.objects.all().annotate(studios_cnt=Count('studio')).order_by('name')
    return render(request,'mt_table.html', args)

@mb_login(url='login')
def meet_update(request, meet_id=None):
    args={}
    args.update(csrf(request))
    meet =  None
    try:
        meet_id=int(meet_id)
    except:
        meet_id=None

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        if request.POST:
            meet_type = request.POST.get('meetType')
            meet_subj = request.POST.get('meetSubj')
            meet_date = request.POST.get('meetDate')
            meet_date = datetime.datetime.strptime(meet_date, '%d.%m.%Y').date()
            meet_start = request.POST.get('meetStart')
            meet_end = request.POST.get('meetEnd')
            meet_acc = request.POST.get('meetAcc')
            meet_tel = request.POST.get('meetTel')
            meet_save = (request.POST.get('meetSave','0') == '1')
            meet_confident = (request.POST.get('meetConfident') == '1')

            # Если произошло копирование совещания, то omt_id содержит ID старого совещания
            try:
                omt_id = request.POST.get('omt_id',0)
            except:
                omt_id=0

            if meet_id:
                Meeting.objects.filter(id=meet_id).update(meet_type=meet_type,meet_subj=meet_subj,
                                       meet_date=meet_date, meet_start=meet_start, meet_end=meet_end,
                                       meet_acc=meet_acc, meet_tel=meet_tel, meet_save=meet_save, meet_confident=meet_confident)
            else:
                meet_id=Meeting.objects.create(meet_type=meet_type,meet_subj=meet_subj,
                                       meet_date=meet_date, meet_start=meet_start, meet_end=meet_end,
                                       meet_acc=meet_acc, meet_tel=meet_tel, meet_save=meet_save, meet_confident=meet_confident).id
                if omt_id:
                    #print('start bulk copy from id={} to id={}'.format(omt_id, meet_id))
                    old_members = Member.objects.filter(meeting_id=omt_id)
                    old_items = Item.objects.filter(meeting_id=omt_id)
                    old_studios = StudioList.objects.filter(meeting_id=omt_id)
                    Member.objects.bulk_create([Member(order_n=i.order_n, f=i.f,i=i.i,o=i.o,dep=i.dep,dol=i.dol,fio=i.fio,
                                                       is_speaker=i.is_speaker, is_presence=i.is_presence, is_init=i.is_init,
                                                       is_lead=i.is_lead, meeting_id=meet_id) for i in old_members])
                    Item.objects.bulk_create([Item(order_n=i.order_n, f=i.f,i=i.i,o=i.o,dep=i.dep,dol=i.dol,
                                                   item_subj=i.item_subj, item_time=i.item_time, meeting_id=meet_id) for i in old_items])
                    StudioList.objects.bulk_create([StudioList(order_n=i.order_n, meeting_id=meet_id, studio_id=i.studio_id) for i in old_studios])

            return redirect(reverse("meetings:table"))

    if meet_id:
        try:
            meet = Meeting.objects.get(id=meet_id)
        except Meeting.DoesNotExist:
            meet = None

    args['employees'] = Employee.objects.all().order_by('f', 'i', 'o').values('f', 'i', 'o','tel')
    args['meet']=meet
    args['meet_id'] = meet_id if meet_id else 0
    args['meeting_type_choices'] = MEETING_TYPE_CHOICES

    return render(request,'mt_meetform.html', args)

@mb_login(url='login')
def meet_delete(request, meet_id=None):
    Meeting.objects.filter(id=meet_id).delete()
    return redirect(reverse("meetings:table"))

def meet_copy(request, meet_id=None):
    args = {}
    omt =  None
    if meet_id:
        try:
            omt = Meeting.objects.get(id=int(meet_id))
        except Meeting.DoesNotExist:
            omt = None

    args['employees'] = Employee.objects.all().order_by('f', 'i', 'o').values('f', 'i', 'o', 'tel')
    args['meet']=omt
    args['meet_id'] = None
    args['meeting_type_choices'] = MEETING_TYPE_CHOICES

    return render(request,'mt_meetform.html', args)

@mb_login(url='login')
def members_update(request):
    res = 1
    if request.method == 'POST':
        if request.POST:
            #print(request.POST)
            res = 0
            id_list = []
            meet_id = int(request.POST.get('meet_id',0))
            rowOrder = request.POST.get('membersTable_rowOrder',None)
            if rowOrder and meet_id:
                rowOrder = map(int, rowOrder.split(',')) if rowOrder else None;
                for index, ordern in enumerate(rowOrder):
                    try:
                        id = int(request.POST.get('membersTable_id_{}'.format(ordern),0))
                    except:
                        id = 0

                    dep = request.POST.get('membersTable_dep_{}'.format(ordern),'')
                    f = request.POST.get('membersTable_f_{}'.format(ordern),'')
                    i= request.POST.get('membersTable_i_{}'.format(ordern),'')
                    o = request.POST.get('membersTable_o_{}'.format(ordern),'')
                    fio = "{} {}{}{}{}".format(f,i[0:1],'.' if i!='' else '',o[0:1],'.' if o!='' else '')
                    dol = request.POST.get('membersTable_dol_{}'.format(ordern),'')
                    is_speaker = request.POST.get('membersTable_is_speaker_{}'.format(ordern),0)
                    is_init = request.POST.get('membersTable_is_init_{}'.format(ordern),0)
                    is_lead = request.POST.get('membersTable_is_lead_{}'.format(ordern),0)
                    is_presence = request.POST.get('membersTable_is_presence_{}'.format(ordern), 0)

                    if id:
                        #print('Update')
                        Member.objects.filter(id=id).update(dep=dep, f=f, i=i, o=o, dol=dol, fio = fio,
                                              is_speaker=is_speaker, is_lead=is_lead, is_init=is_init,
                                              meeting_id=meet_id, order_n=index, is_presence=is_presence)
                    else:
                        #print('Create')
                        id=Member.objects.create(dep=dep, f=f, i=i, o=o, dol=dol, fio = fio,
                                                 is_speaker=is_speaker, is_lead=is_lead, is_init=is_init,
                                                 meeting_id=meet_id, order_n=index, is_presence=is_presence).id
                    id_list.append(id)
                    #print(id, dep, f, i, o, dol, is_speaker, fio,meet_id, index)

            Member.objects.filter(meeting_id=meet_id).exclude(id__in=id_list).delete()

    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps({'user':'admin','id':1,'result':res}))
    return response

@mb_login(url='login')
def members_get(request, meet_id=None):
    if request.is_ajax():
        members = Member.objects.filter(meeting__id=int(meet_id) if meet_id else 0).order_by('order_n').values()
        #data = serializers.serialize('json', list(members), fields=('dep','f','i','o','dol','is_speaker','Id'))
        data = json.dumps([dict(item) for item in members])
        return HttpResponse(data,'json')

    return meet_table(request)

@mb_login(url='login')
def members_doc(request, meet_id=None):
    try:
        meeting = Meeting.objects.get(id=meet_id)
    except:
        meeting = None

    if meeting:
        members = Member.objects.filter(meeting__id=int(meet_id) if meet_id else 0).order_by('order_n')

        deplist = [];  d = None; ml = [];
        for m in members:
            if (m.dep != d):
                if d: deplist.append({'name': d, 'members': ml})
                d = m.dep
                ml = []
            ml.append({'f': m.f, 'i': m.i, 'o': m.o, 'fio': m.fio, 'dep': m.dep, 'dol': m.dol})
        deplist.append({'name': d, 'members': ml})

        filename='meet{}_members_{}.docx'.format(meet_id,timezone.now().strftime('%Y%m%d%H%M%S'))
        fullname="media/{}".format(filename)
        doc = DocxTemplate("media/members_tpl.docx")
        context = {'meet_subj': meeting.meet_subj,
                   'meet_date':meeting.meet_date,
                   'deps':deplist}

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
def items_update(request):
    res = 1
    if request.method == 'POST':
        if request.POST:
            res = 0
            id_list = []
            meet_id = int(request.POST.get('meet_id',0))
            rowOrder = request.POST.get('itemsTable_rowOrder',None)
            if rowOrder and meet_id:
                rowOrder = map(int, rowOrder.split(',')) if rowOrder else None;
                for index, ordern in enumerate(rowOrder):
                    try:
                        id = int(request.POST.get('itemsTable_id_{}'.format(ordern),0))
                    except:
                        id = 0
                    dep = request.POST.get('itemsTable_dep_{}'.format(ordern),'')
                    f = request.POST.get('itemsTable_f_{}'.format(ordern),'')
                    i= request.POST.get('itemsTable_i_{}'.format(ordern),'')
                    o = request.POST.get('itemsTable_o_{}'.format(ordern),'')
                    dol = request.POST.get('itemsTable_dol_{}'.format(ordern),'')
                    item_time = request.POST.get('itemsTable_item_time_{}'.format(ordern),0)
                    item_subj = request.POST.get('itemsTable_item_subj_{}'.format(ordern), 0)

                    if id:
                        Item.objects.filter(id=id).update(dep=dep, f=f, i=i, o=o, dol=dol, item_time=item_time, item_subj = item_subj,
                                              meeting_id=meet_id, order_n=index)
                    else:
                        id=Item.objects.create(dep=dep, f=f, i=i, o=o, dol=dol, item_time=item_time, item_subj = item_subj,
                                              meeting_id=meet_id, order_n=index).id
                    id_list.append(id)
                    #print(id, dep, f, i, o, dol, item_time, item_subj, meet_id, index)

            Item.objects.filter(meeting_id=meet_id).exclude(id__in=id_list).delete()

    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps({'user':'admin','id':1,'result':res}))
    return response

@mb_login(url='login')
def items_get(request, meet_id=None):
    if request.is_ajax():
        meet_id = int(meet_id) if meet_id else 0
        items_count = Item.objects.filter(meeting__id=meet_id).count()
        if items_count==0:
            for index, m in enumerate(Member.objects.filter(meeting__id=meet_id, is_speaker=1).order_by('order_n')):
                Item.objects.create(dep=m.dep, f=m.f, i=m.i, o=m.o, dol=m.dol, meeting_id=meet_id, order_n=index)

        items = Item.objects.filter(meeting__id=meet_id).order_by('order_n').values()
        data = json.dumps([dict(item) for item in items])
        return HttpResponse(data,'json')

    return meet_table(request)

@mb_login(url='login')
def items_doc(request, meet_id=None):
    try:
        meeting = Meeting.objects.get(id=meet_id)
    except:
        meeting = None

    if meeting:
        items = Item.objects.filter(meeting__id=int(meet_id) if meet_id else 0).order_by('order_n')
        studio = ''
        try: studio = StudioList.objects.filter(meeting__id=int(meet_id)).order_by('order_n').values('studio__studio_addr')[0]['studio__studio_addr']
        except: pass
        try: meet_lead = Member.objects.filter(meeting__id=int(meet_id), is_lead=1)[0]
        except: meet_lead = None
        try: meet_init = Member.objects.filter(meeting__id=int(meet_id), is_init=1)[0]
        except: meet_init = None

        filename='meet{}_items_{}.docx'.format(meet_id,timezone.now().strftime('%Y%m%d%H%M%S'))
        fullname="media/{}".format(filename)
        doc = DocxTemplate("media/items_tpl.docx")
        context = {'meeting': meeting,
                   'items': items,
                   'studio': studio,
                   'meet_date': meeting.meet_date.strftime('%d.%m.%Y'),
                   'meet_lead': meet_lead,
                   'meet_init': meet_init}
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
def studios_update(request):
    res = 1
    if request.method == 'POST':
        if request.POST:
            res = 0
            id_list = []
            meet_id = int(request.POST.get('meet_id', 0))
            rowOrder = request.POST.get('studiosTable_rowOrder', None)
            #print('>>> {} {}'.format(meet_id, rowOrder))
            if rowOrder and meet_id:
                rowOrder = map(int, rowOrder.split(',')) if rowOrder else None;
                for index, ordern in enumerate(rowOrder):
                    try:
                        id = int(request.POST.get('studiosTable_id_{}'.format(ordern),0))
                    except:
                        id = 0

                    studio_id = int(request.POST.get('studiosTable_studio_id_{}'.format(ordern), 0))

                    if id:
                        StudioList.objects.filter(id=id).update(studio_id=studio_id, meeting_id=meet_id, order_n=index)
                    else:
                        id = StudioList.objects.create(studio_id=studio_id, meeting_id=meet_id, order_n=index).id
                    id_list.append(id)

            StudioList.objects.filter(meeting_id=meet_id).exclude(id__in=id_list).delete()

    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps({'user':'admin','id':1,'result':res}))
    return response

@mb_login(url='login')
def studios_get(request, meet_id=None):
    if request.is_ajax():
        meet_id = int(meet_id) if meet_id else 0

        studios = StudioList.objects.filter(meeting__id=meet_id).order_by('order_n').values('id','meeting_id','studio__dep_id', 'studio_id')
        data = json.dumps([dict(item) for item in studios])
        print(data)
        return HttpResponse(data,'json')

    return meet_table(request)

@mb_login(url='login')
def studios_get_bydep(request, dep_id=None):
    if request.is_ajax():
        dep_id = int(dep_id) if dep_id else 0

        studios = Studio.objects.filter(dep=dep_id)
        data = json.dumps([{'id':item.id,'studio_addr':item.studio_addr,'studio_type':item.studio_type} for item in studios])
        print('dep:{} data:{}'.format(dep_id,data))
        return HttpResponse(data,'json')

    return meet_table(request)

@mb_login(url='login')
def studios_doc(request, meet_id=None):
    try:
        meeting = Meeting.objects.get(id=meet_id)
    except:
        meeting = None

    if meeting:
        studios = StudioList.objects.filter(meeting__id=meet_id).order_by('order_n').values('id', 'meeting_id',
                                                                                            'studio__dep_id',
                                                                                            'studio__dep__name',
                                                                                            'studio__studio_addr',
                                                                                            'studio__studio_type',
                                                                                            'studio_id',)
        try: meet_lead = Member.objects.filter(meeting__id=int(meet_id), is_lead=1)[0]
        except: meet_lead = None
        try: meet_init = Member.objects.filter(meeting__id=int(meet_id), is_init=1)[0]
        except: meet_init = None
        try: studio = studios[0]
        except: studio = None

        filename='meet{}_req_{}.docx'.format(meet_id,timezone.now().strftime('%Y%m%d%H%M%S'))
        fullname="media/{}".format(filename)
        doc = DocxTemplate("media/req_tpl.docx")
        context = {'meeting': meeting,
                   'studios': studios,
                   'meet_date': meeting.meet_date.strftime('%d.%m.%Y'),
                   'meet_lead': meet_lead,
                   'meet_init': meet_init,
                   'studio' : studio,
                   'Z0': '' if meeting.meet_save else 'X',
                   'Z1': 'X' if meeting.meet_save else '',
                   'K0': '' if meeting.meet_confident else 'X',
                   'K1': 'X' if meeting.meet_confident else '',
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
def plan_doc(request):

        filename = 'meet_planning_{}.docx'.format(timezone.now().strftime('%Y%m%d%H%M%S'))
        fullname = "media/{}".format(filename)
        doc = DocxTemplate("media/planning_tpl.docx")
        context = {}

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
def checks_update(request, meet_id=None):
    args={}
    args.update(csrf(request))
    meet =  None
    try:
        meet_id=int(meet_id)
    except:
        meet_id=None

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        if request.POST:
            post = request.POST.copy()
            # Оставляем только параметры, которые начинаются на 'p"
            for key in list(post.keys()):
                if key[0:1]!='p':
                    del post[key]

            data = json.dumps(post)
            try:
                id = int(request.POST.get('id', 0))
            except:
                id = 0
            total = int(request.POST.get('total', 0))
            complete = int(request.POST.get('complete', 0))

            if id:
                Check.objects.filter(id=id).update(meeting_id=meet_id, data=data, total=total, complete=complete)
            else:
                id=Check.objects.create(meeting_id=meet_id, data=data, total=total, complete=complete)

            return redirect(reverse("meetings:table"))

    if meet_id:
        try:
            meet = Meeting.objects.get(id=meet_id)
        except Meeting.DoesNotExist:
            meet = None
        try:
            checks = Check.objects.get(meeting_id=meet_id)
        except Check.DoesNotExist:
            checks = None

    if checks:
        checks_json=json.loads(checks.data)
        args['id'] = checks.id
        args['total'] = checks.total
        args['complete'] = checks.complete
    else:
        checks_json = {}

    members=Member.objects.filter(meeting_id=meet_id)
    items = Item.objects.filter(meeting_id=meet_id)
    studios=meet.studios

    if studios:
        checks_json['p_studios'] = 'on'
        args['studios'] = studios
    if members:
        checks_json['p_members'] = 'on'
        args['members'] = members
        args['is_presence'] = members.filter(Q(is_presence=1) | Q(is_init=1)).count()
    if items:
        checks_json['p_items'] = 'on'
        args['items'] = items
    if meet:
        args['meet'] = meet

    args['checks'] = checks_json
    args['meet_id'] = meet_id if meet_id else 0
    args['meeting_type_choices'] = MEETING_TYPE_CHOICES

    return render(request,'mt_check.html', args)
