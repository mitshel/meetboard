# До Django 2.0
urlpatterns = [
    url('^test/(?P<number>[0-9]*)$', views.test, name='test'),
    url('^test/', views.page, name="page")
]
  
# Django 2.0
urlpatterns = [
    path('test/<int:testvar>/', views.test, name='test'),
    path('page/', views.page, name="page")
]

urlpatterns = [
path('', views.home, name='home'),
path('landing/', views.landing, name='landing'),
]