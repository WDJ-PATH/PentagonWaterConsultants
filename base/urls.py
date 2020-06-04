# pages/urls.py
from django.urls import path

from .views import HomePageView
from . import views


app_name = "base"

urlpatterns = [
    path('register', views.reg_index, name='register'),
    path('reg', views.register, name='registered'),

    path('', HomePageView.as_view(), name='index'),
    path('login', views.login_index, name='login_index'),
    path('loggedin', views.login, name='loggedin'),
    path('loggedout', views.logout, name='loggedout'),

    path('mytests', views.all_my_tests, name='mytests'),
    path('<int:test_id>/viewtestdetails', views.view_test, name='testdetails'),
    path('<int:test_id>/printdata', views.print_data_unofficial, name='printdata'),

    path('enquiry', views.enquiry, name='enquiry'),
    path('passwordreset', views.password_reset, name='passwordreset')
]