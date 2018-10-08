from django.contrib import admin
from django.urls import path
from meetings import views

urlpatterns = [
    path('table/', views.meet_table, name='table'),
    path('add/', views.meet_update, name='add'),
    path('update/<str:meet_id>/', views.meet_update, name='update'),
    path('delete/<str:meet_id>/', views.meet_delete, name='delete'),
    path('copy/<str:meet_id>/', views.meet_copy, name='copy'),
    path('membersupd/', views.members_update, name='membersupd'),
    path('membersget/<str:meet_id>/', views.members_get, name='membersget'),
    path('itemsupd/', views.items_update, name='itemsupd'),
    path('itemsget/<str:meet_id>/', views.items_get, name='itemsget'),
    path('studiosupd/', views.studios_update, name='studiosupd'),
    path('studiosget/<str:meet_id>/', views.studios_get, name='studiosget'),
    path('studiosget_bydep/<str:dep_id>/', views.studios_get_bydep, name='studiosget_bydep'),
]
