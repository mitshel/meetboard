from django.contrib import admin
from django.urls import path
from meetings import views

urlpatterns = [
    path('table/', views.meet_table, name='table'),
    path('add/', views.meet_update, name='add'),
    path('update/<str:meet_id>/', views.meet_update, name='update'),
    path('delete/<str:meet_id>/', views.meet_delete, name='delete'),
    path('copy/<str:meet_id>/', views.meet_copy, name='copy'),
]
