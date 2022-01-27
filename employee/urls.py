from django.urls import path

from . import views

appname = 'employee'
urlpatterns = [
    path('', views.index, name='index'),
]