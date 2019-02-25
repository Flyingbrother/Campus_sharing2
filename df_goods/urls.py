from django.conf.urls import url
from . import views
from django.urls import path
from .views import *


urlpatterns = [
    # url('^$', views.index),
    # url('^list(\d+)_(\d+)_(\d+)/$', views.list),
    # url('^(\d+)/$', views.detail),
    path('', views.index),
    # path('list(\d+)_(\d+)_(\d+)/', views.list),
    # path('(\d+)/', views.detail)
    url('^list(\d+)_(\d+)_(\d+)/$', views.list),
    url('^(\d+)/$', views.detail),
    url(r'^search/', MySearchView()),

]