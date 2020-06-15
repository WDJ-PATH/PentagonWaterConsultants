# pages/urls.py
from django.urls import path

from . import views

app_name = "manager"

urlpatterns = [
    path('hidden/register', views.reg_index, name='register'),
    path('hidden/reg', views.manager_register, name='reg'),
    path('hidden/login', views.login_index, name='login'),
    path('hidden/loggedin', views.manager_login, name='loggedin'),
    path('hidden/loggedout', views.manager_logout, name='loggedout'),

    path('hidden/addnewtest', views.add_test, name='addnewtest'),

    path('hidden/<int:test_id>/updatetest', views.update_test, name='updatetest'),
    path('hidden/<int:test_id>/testupdated', views.update_test, name='updatetest'),

    path('hidden/banuser', views.ban_user_index, name='banuser'),
    path('hidden/banuserbypn', views.ban_user_by_search, name='banuserbypn'),
    path('hidden/banuserbydate', views.ban_user_by_date, name='banuser'),
    path('hidden/banned', views.ban_user, name='banuser'),

    path('hidden/viewuserindex', views.view_user_index, name='viewuser'),
    path('hidden/testadded', views.add_test, name='testadded'),
    path('hidden/userlist', views.view_user, name='userlist'),
    path('hidden/userlistbydate', views.view_user_bydate, name='userlistbydate'),

    path('hidden/<int:test_id>/printdata', views.print_data, name='printdata'),

    path('hidden/testlist', views.test_list, name='testlist'),
    path('hidden/testexport', views.test_export, name='testexport')
]