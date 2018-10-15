from django.contrib import admin
from django.urls import path
from protocols import views

urlpatterns = [
    path('table/', views.proto_table, name='table'),
]
