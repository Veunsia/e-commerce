from django.conf.urls import url

from OrederApp import views

urlpatterns = [
    url(r'^can_create/', views.can_create),
    url(r'^orderDetail/', views.orderDetail),
    url(r'^testpay/' , views.testpay),
]