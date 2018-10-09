import datetime
import json
import os

from django.template.context_processors import csrf
from django.http import HttpResponse
from django.core import serializers
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.db.models import Count
from django.contrib.staticfiles.views import serve
from django.utils import timezone

from docxtpl import DocxTemplate


from meetings.models import MEETING_TYPE_CHOICES, Meeting, Dep, Member, Item, Studio, StudioList, mVideo

def home(request):
    args={}
    args['meetings'] = Meeting.objects.filter(meet_date__gte=timezone.now()).order_by('meet_date', '-meet_start')[0:3]
    return render(request,'mb_home.html', args)

def meet_table(request):
    args={}

    args['meetings'] = Meeting.objects.all().order_by('-meet_date','-meet_start')
    args['deps'] = Dep.objects.all().annotate(studios_cnt=Count('studio')).order_by('name')
    return render(request,'mt_table.html', args)

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
            #meet_place = request.POST.get('meetPlace','')
            meet_subj = request.POST.get('meetSubj')
            #meet_lead = request.POST.get('meetLead')
            meet_date = request.POST.get('meetDate')
            meet_date = datetime.datetime.strptime(meet_date, '%d.%m.%Y').date()
            meet_start = request.POST.get('meetStart')
            meet_end = request.POST.get('meetEnd')
            #meet_init = request.POST.get('meetInit')
            meet_acc = request.POST.get('meetAcc')
            meet_tel = request.POST.get('meetTel')
            meet_save = (request.POST.get('meetSave','0') == '1')
            meet_confident = (request.POST.get('meetConfident') == '1')

            if meet_id:
                Meeting.objects.filter(id=meet_id).update(meet_type=meet_type,meet_subj=meet_subj,
                                       meet_date=meet_date, meet_start=meet_start, meet_end=meet_end,
                                       meet_acc=meet_acc, meet_tel=meet_tel, meet_save=meet_save, meet_confident=meet_confident)
            else:
                Meeting.objects.create(meet_type=meet_type,meet_subj=meet_subj,
                                       meet_date=meet_date, meet_start=meet_start, meet_end=meet_end,
                                       meet_acc=meet_acc, meet_tel=meet_tel, meet_save=meet_save, meet_confident=meet_confident)

            # args['meetings'] = Meeting.objects.all().order_by('-meet_date', '-meet_start')
            # return render(request,'mt_table.html', args)
            #return meet_table(request)
            return redirect(reverse("meetings:table"))

    if meet_id:
        try:
            meet = Meeting.objects.get(id=meet_id)
        except Meeting.DoesNotExist:
            meet = None

    args['meet']=meet
    args['meet_id'] = meet_id if meet_id else 0
    args['meeting_type_choices'] = MEETING_TYPE_CHOICES

    return render(request,'mt_meetform.html', args)

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

    args['meet']=omt
    args['meet_id'] = None
    args['meeting_type_choices'] = MEETING_TYPE_CHOICES

    return render(request,'mt_meetform.html', args)

def members_update(request):
    res = 1
    if request.method == 'POST':
        if request.POST:
            res = 0
            id_list = []
            meet_id = int(request.POST.get('meet_id',0))
            rowOrder = request.POST.get('membersTable_rowOrder',None)
            if rowOrder and meet_id:
                rowOrder = map(int, rowOrder.split(',')) if rowOrder else None;
                for index, ordern in enumerate(rowOrder):
                    id = request.POST.get('membersTable_id_{}'.format(ordern),0)
                    dep = request.POST.get('membersTable_dep_{}'.format(ordern),'')
                    f = request.POST.get('membersTable_f_{}'.format(ordern),'')
                    i= request.POST.get('membersTable_i_{}'.format(ordern),'')
                    o = request.POST.get('membersTable_o_{}'.format(ordern),'')
                    fio = "{} {}{}{}{}".format(f,i[0:1],'.' if i!='' else '',o[0:1],'.' if o!='' else '')
                    dol = request.POST.get('membersTable_dol_{}'.format(ordern),'')
                    is_speaker = request.POST.get('membersTable_is_speaker_{}'.format(ordern),0)
                    is_init = request.POST.get('membersTable_is_init_{}'.format(ordern),0)
                    is_lead = request.POST.get('membersTable_is_lead_{}'.format(ordern),0)

                    if id:
                        Member.objects.update(id=id, dep=dep, f=f, i=i, o=o, dol=dol, fio = fio,
                                              is_speaker=is_speaker, is_lead=is_lead, is_init=is_init,
                                              meeting_id=meet_id, order_n=index)
                    else:
                        id=Member.objects.create(dep=dep, f=f, i=i, o=o, dol=dol, fio = fio,
                                              is_speaker=is_speaker, is_lead=is_lead, is_init=is_init,
                                              meeting_id=meet_id, order_n=index).id
                    id_list.append(id)
                    # print(id, dep, f, i, o, dol, is_speaker, fio,meet_id, index)

            Member.objects.filter(meeting_id=meet_id).exclude(id__in=id_list).delete()

    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps({'user':'admin','id':1,'result':res}))
    return response

def members_get(request, meet_id=None):
    if request.is_ajax():
        members = Member.objects.filter(meeting__id=int(meet_id) if meet_id else 0).values()
        #data = serializers.serialize('json', list(members), fields=('dep','f','i','o','dol','is_speaker','Id'))
        data = json.dumps([dict(item) for item in members])
        return HttpResponse(data,'json')

    return meet_table(request)

def members_doc(request, meet_id=None):
    try:
        meeting = Meeting.objects.get(id=meet_id)
    except:
        meeting = None

    if meeting:
        members = Member.objects.filter(meeting__id=int(meet_id) if meet_id else 0).order_by('order_n')

        deplist = [];  d = None
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
                    id = request.POST.get('itemsTable_id_{}'.format(ordern),0)
                    dep = request.POST.get('itemsTable_dep_{}'.format(ordern),'')
                    f = request.POST.get('itemsTable_f_{}'.format(ordern),'')
                    i= request.POST.get('itemsTable_i_{}'.format(ordern),'')
                    o = request.POST.get('itemsTable_o_{}'.format(ordern),'')
                    dol = request.POST.get('itemsTable_dol_{}'.format(ordern),'')
                    item_time = request.POST.get('itemsTable_item_time_{}'.format(ordern),0)
                    item_subj = request.POST.get('itemsTable_item_subj_{}'.format(ordern), 0)

                    if id:
                        Item.objects.update(id=id, dep=dep, f=f, i=i, o=o, dol=dol, item_time=item_time, item_subj = item_subj,
                                              meeting_id=meet_id, order_n=index)
                    else:
                        id=Item.objects.create(dep=dep, f=f, i=i, o=o, dol=dol, item_time=item_time, item_subj = item_subj,
                                              meeting_id=meet_id, order_n=index).id
                    id_list.append(id)
                    print(id, dep, f, i, o, dol, item_time, item_subj, meet_id, index)

            Item.objects.filter(meeting_id=meet_id).exclude(id__in=id_list).delete()

    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps({'user':'admin','id':1,'result':res}))
    return response

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


def studios_update(request):
    res = 1
    if request.method == 'POST':
        if request.POST:
            res = 0
            id_list = []
            meet_id = int(request.POST.get('meet_id', 0))
            rowOrder = request.POST.get('studiosTable_rowOrder', None)
            print('>>> {} {}'.format(meet_id, rowOrder))
            if rowOrder and meet_id:
                rowOrder = map(int, rowOrder.split(',')) if rowOrder else None;
                for index, ordern in enumerate(rowOrder):
                    id = int(request.POST.get('studiosTable_id_{}'.format(ordern), 0))
                    studio_id = int(request.POST.get('studiosTable_studio_id_{}'.format(ordern), 0))
                    if id:
                        StudioList.objects.update(id=id, studio_id=studio_id, meeting_id=meet_id, order_n=index)
                    else:
                        id = StudioList.objects.create(studio_id=studio_id, meeting_id=meet_id, order_n=index).id
                    id_list.append(id)
                    print(id, studio_id, meet_id, index)

            StudioList.objects.filter(meeting_id=meet_id).exclude(id__in=id_list).delete()

    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps({'user':'admin','id':1,'result':res}))
    return response

def studios_get(request, meet_id=None):
    if request.is_ajax():
        meet_id = int(meet_id) if meet_id else 0

        studios = StudioList.objects.filter(meeting__id=meet_id).order_by('order_n').values('id','meeting_id','studio__dep_id', 'studio_id')
        data = json.dumps([dict(item) for item in studios])
        print(data)
        return HttpResponse(data,'json')

    return meet_table(request)

def studios_get_bydep(request, dep_id=None):
    if request.is_ajax():
        dep_id = int(dep_id) if dep_id else 0

        studios = Studio.objects.filter(dep=dep_id)
        data = json.dumps([{'id':item.id,'studio_addr':item.studio_addr,'studio_type':item.studio_type} for item in studios])
        print('dep:{} data:{}'.format(dep_id,data))
        return HttpResponse(data,'json')

    return meet_table(request)

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

        filename='meet{}_req_{}.docx'.format(meet_id,timezone.now().strftime('%Y%m%d%H%M%S'))
        fullname="media/{}".format(filename)
        doc = DocxTemplate("media/req_tpl.docx")
        context = {'meeting': meeting,
                   'studios': studios,
                   'meet_date': meeting.meet_date.strftime('%d.%m.%Y'),
                   'meet_lead': meet_lead,
                   'meet_init': meet_init,
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
