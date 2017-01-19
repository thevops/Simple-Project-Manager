from django.conf.urls import url
from . import views

app_name = 'proman'
urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^wiadomosc/wyslij/$', views.message_send, name='message_send'),
    url(r'^wiadomosci/$', views.message_show, name='message_show'),
    url(r'^wiadomosci/(?P<friend_id>[0-9]+)/$', views.message_show, name='message_show'),

    url(r'^profile/(?P<user_id>[0-9]+)/$', views.user_profile, name='user_profile'),

    url(r'^projekty/$', views.projects, name='projects'),
    url(r'^projekty/edytuj/(?P<project_id>[0-9]+)/$', views.project_edit, name='project_edit'),
    url(r'^projekty/usun/(?P<project_id>[0-9]+)/$', views.project_remove, name='project_remove'),
    url(r'^projekty/przegladaj/(?P<project_id>[0-9]+)/$', views.project_show, name='project_show'),
    url(r'^projekty/dodaj/$', views.project_add, name='project_add'),

    url(r'^projekty/dolacz/$', views.project_join, name='project_join'),  # form with Access Code. User joins himself
    url(r'^projekty/dolacz/(?P<project_id>[0-9]+)/$',
        views.project_add_member, name='project_add_member'),  # owner joins others
    url(r'^projekty/dolacz/(?P<project_id>[0-9]+)/(?P<member_id>[0-9]*)/$',
        views.project_add_member, name='project_add_member'),  # owner joins others
    url(r'^projekty/odlacz/(?P<project_id>[0-9]+)/(?P<member_id>[0-9]+)/$',
        views.project_del_member, name='project_del_member'),
    url(r'^projekty/wagi/(?P<project_id>[0-9]+)/$', views.task_change_weight, name='task_change_weight'),

    url(r'^zadania/$', views.tasks, name='tasks'),
    url(r'^zadanie/przegladaj/(?P<task_id>[0-9]+)/$', views.task_show, name="task_show"),
    url(r'^zadanie/dodaj/(?P<project_id>[0-9]+)/$', views.task_add, name="task_add"),
    url(r'^zadanie/usun/(?P<task_id>[0-9]+)/$', views.task_remove, name='task_remove'),
    url(r'^zadanie/edytuj/(?P<task_id>[0-9]+)/$', views.task_edit, name='task_edit'),
    url(r'^zadanie/zrobione/(?P<task_id>[0-9]+)/$', views.task_done, name='task_done'),

]
