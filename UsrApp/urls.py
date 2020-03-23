from django.conf.urls import url

from UsrApp import views

urlpatterns = [
    url(r'^register/', views.register, name='register'),
    url(r'^checkname/', views.checkname, name='checkname'),
    url(r'^checkemail/', views.checkemail),
    url(r'^login/', views.login,name='login'),
    url(r'^checklogin/', views.checklogin,name='checklogin'),
    url(r'^get_code/', views.get_code),
    url(r'^logout/', views.logout,name='logout'),
]
