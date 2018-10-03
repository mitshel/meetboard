import datetime

from django.shortcuts import render
from django.template.context_processors import csrf

from meetings.models import MEETING_TYPE_CHOICES, Meeting, MeetingForm

def home(request):
    args={}
    return render(request,'mb_home.html', args)

def meet_table(request):
    args={}

    args['meetings'] = Meeting.objects.all().order_by('-meet_date','-meet_start')
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

            args['meetings'] = Meeting.objects.all().order_by('-meet_date', '-meet_start')
            return render(request,'mt_table.html', args)

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

