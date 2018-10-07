import datetime

from django.shortcuts import render
from django.template.context_processors import csrf
from django.http import HttpResponse

from meetings.models import MEETING_TYPE_CHOICES, Meeting, MeetingForm, Dep, Member

def home(request):
    args={}
    return render(request,'mb_home.html', args)

def meet_table(request):
    args={}

    args['meetings'] = Meeting.objects.all().order_by('-meet_date','-meet_start')
    args['deps'] = Dep.objects.all().order_by('name')
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
            meet_place = request.POST.get('meetPlace')
            meet_subj = request.POST.get('meetSubj')
            meet_lead = request.POST.get('meetLead')
            meet_date = request.POST.get('meetDate')
            meet_date = datetime.datetime.strptime(meet_date, '%d.%m.%Y').date()
            meet_start = request.POST.get('meetStart')
            meet_end = request.POST.get('meetEnd')
            meet_init = request.POST.get('meetInit')
            meet_acc = request.POST.get('meetAcc')
            meet_tel = request.POST.get('meetTel')
            meet_save = (request.POST.get('meetSave','0') == '1')
            meet_confident = (request.POST.get('meetConfident') == '1')

            if meet_id:
                Meeting.objects.filter(id=meet_id).update(meet_type=meet_type,meet_place=meet_place,meet_subj=meet_subj,meet_lead=meet_lead,
                                       meet_date=meet_date, meet_start=meet_start, meet_end=meet_end, meet_init=meet_init,
                                       meet_acc=meet_acc, meet_tel=meet_tel, meet_save=meet_save, meet_confident=meet_confident)
            else:
                Meeting.objects.create(meet_type=meet_type,meet_place=meet_place,meet_subj=meet_subj,meet_lead=meet_lead,
                                       meet_date=meet_date, meet_start=meet_start, meet_end=meet_end, meet_init=meet_init,
                                       meet_acc=meet_acc, meet_tel=meet_tel, meet_save=meet_save, meet_confident=meet_confident)

            # args['meetings'] = Meeting.objects.all().order_by('-meet_date', '-meet_start')
            # return render(request,'mt_table.html', args)
            return meet_table(request)

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
    return meet_table(request)

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
            meet_id = int(request.POST.get('meet_id',None))
            rowOrder = request.POST.get('membersTable_rowOrder',None)
            rowOrder = map(int, rowOrder.split()) if rowOrder else None;
            for index,o in enumerate(rowOrder):
                id = request.POST.get('membersTable_id_{}'.format(o),0)
                dep = request.POST.get('membersTable_dep_{}'.format(o),'')
                f = request.POST.get('membersTable_f_{}'.format(o),'')
                i= request.POST.get('membersTable_i_{}'.format(o),'')
                o = request.POST.get('membersTable_o_{}'.format(o),'')
                fio = "{} {}.{}.".format(f,i[0:1],o[0:1])
                dol = request.POST.get('membersTable_dol_{}'.format(o),'')
                is_speaker = request.POST.get('membersTable_is_speaker_{}'.format(o),0)
                if id:
                    Member.objects.update(id=id, dep=dep, f=f, i=i, o=o, dol=dol, is_speaker=is_speaker, fio = fio,
                                          meeting__id=meet_id, order_n=index)
                    print('Update {} {} {} {} {} {} {} {} {}'.format(dep, f, i, o, dol, is_speaker, fio, meet_id, index))
                else:
                    Member.objects.create(dep=dep, f=f, i=i, o=o, dol=dol, is_speaker=is_speaker, fio=fio,
                                          meeting__id=meet_id, order_n=index)
                    print('Create {} {} {} {} {} {} {} {} {}'.format(dep, f, i, o, dol, is_speaker, fio, meet_id, index))

    print(request.POST)
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write("{user:%s,id:%s,result:%s}" % ('admin', 1, 1))
    return response