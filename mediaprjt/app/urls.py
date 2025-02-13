from django.urls import path
from . import views


urlpatterns=[
    path('',views.user_home),
    path('admin_home',views.admin_home),
    path('login',views.login),
    path('viewall',views.viewall),

]