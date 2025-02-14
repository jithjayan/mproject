from django.urls import path
from . import views


urlpatterns=[
    path('',views.user_home),
    path('admin_home',views.admin_home),
    path('login',views.u_login),
    path('reg',views.reg),
    path('user_prfl',views.user_prfl),
    path('viewall',views.viewall),
    path('viewpic/<pid>',views.viewpic),
    path('add_image',views.add_image),

]