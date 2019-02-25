from django.conf.urls import url
from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.register),
    path('register_handle/', views.register_handle),
    path('login/', views.login),
    path('login_handle/', views.login_handle),
    path('info/', views.info),
    # path('order(\d+)/', views.order),
    url(r'^order/$', views.order),
    path('site/', views.site),
    path('register_exist/', views.register_exist),
    path('logout/', views.logout),
    path('verifyCode', views.verifyCode)
]