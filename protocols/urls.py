from django.contrib import admin
from django.urls import path
from protocols import views

urlpatterns = [
    path('table/', views.proto_table, name='table'),
    path('add/', views.proto_update, name='add'),
    path('delete/<str:proto_id>/', views.proto_delete, name='delete'),
    path('update/<str:proto_id>/', views.proto_update, name='update'),
    path('copy/<str:proto_id>/', views.proto_copy, name='copy'),
    path('check/<str:proto_id>/', views.proto_check, name='check'),
]
