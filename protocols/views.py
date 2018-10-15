from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy

from mb_auth.views import mb_login

# Create your views here.
@mb_login(url='login')
def proto_table(request):
    args={}
    return redirect(reverse("home"))
