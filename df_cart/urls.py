from django.conf.urls import url
from django.urls import path
from . import views


urlpatterns = [
    path('', views.cart),
    url(r'^add(\d+)_(\d+)/$', views.add),
    url(r'^edit(\d+)_(\d+)$', views.edit),
    url(r'^delete(\d+)/$', views.delete),
    url(r'^edit(\d+)_(\d+)/$', views.edit)
]