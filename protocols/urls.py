from django.contrib import admin
from django.urls import path
from protocols import views

urlpatterns = [
    path('table/', views.proto_table, name='table'),
    path('add/', views.proto_update, name='add'),
    path('delete/<str:proto_id>/', views.proto_delete, name='delete'),
    path('update/<str:proto_id>/', views.proto_update, name='update'),
    path('copy/<str:proto_id>/', views.proto_copy, name='copy'),
    path('decsupd/', views.decisions_update, name='decsupd'),
    path('decsget/<str:proto_id>/', views.decisions_get, name='decsget'),
    path('protodoc/<str:proto_id>/', views.proto_doc, name='doc'),
    path('check/<str:proto_id>/', views.proto_check, name='check'),
    path('checkupd/', views.check_update, name='checkupd'),
]
