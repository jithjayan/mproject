from django.urls import path
from . import views


urlpatterns=[
    path('',views.user_home),
    path('admin_home',views.admin_home),
    path('login',views.login),
    path('viewall',views.viewall),
    path('viewpic/<pid>',views.viewpic),
    path('add_image',views.add_image),
    path('demo',views.demo),

]