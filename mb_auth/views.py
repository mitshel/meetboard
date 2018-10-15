from django.contrib.auth import authenticate, login, logout, REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.conf import settings
from django.urls import reverse, reverse_lazy
from django.template.context_processors import csrf
from django.shortcuts import render, redirect

# Create your models here.
def mb_login(function=None, redirect_field_name=REDIRECT_FIELD_NAME, url=None):
    actual_decorator = user_passes_test(
        lambda u: (u.is_authenticated if settings.MB_AUTH else True),
        login_url=reverse_lazy(url),
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def mb_processor(request):
    args={}
    args['mb_auth']=settings.MB_AUTH
    return args


def loginView(request):
    args = {}
    args.update(csrf(request))
    try:
        username = request.POST['username']
        password = request.POST['password']
    except KeyError:
        return render(request, 'mb_login.html', args)

    next_url = request.GET.get('next', reverse("home"))

    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return redirect(next_url)
        else:
            args['system_message'] = {'text': 'Ваш аккаунт не активирван!', 'type': 'alert-danger'}
            return handler403(request, args)
            # return render(request, 'sopds_login.html', args)
    else:
        args['system_message'] = {'text': 'Пользователь не существует, либо пароль неверен!', 'type': 'alert-danger'}
        return handler403(request, args)
        # return render(request, 'sopds_login.html', args)

    return handler403(request, args)
    # return render(request, 'sopds_login.html', args)

@mb_login(url='login')
def logoutView(request):
    logout(request)
    args = {}
    return redirect(reverse('home'))

def handler403(request, args):
    response = render(request, 'mb_login.html', args)
    response.status_code = 403
    return response
