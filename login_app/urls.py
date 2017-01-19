from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views

from . import views

app_name = 'login_app'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/', auth_views.login, {'template_name': 'login_app/login.html'}, name='login'),
    url(r'^logout/', auth_views.logout, name='logout')
]