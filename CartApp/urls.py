from django.conf.urls import url

from CartApp import views

urlpatterns = [
    url(r'^cart/', views.cart, name='cart'),
    url(r'^addToCart/', views.addToCart),
    url(r'^subfromcart/', views.subfromcart),
    url(r'^subgoods/', views.subgoods),
    url(r'^addgoods/', views.addgoods),
    url(r'^isselect/', views.isselect),
    url(r'^selectall/', views.selectall),
]
