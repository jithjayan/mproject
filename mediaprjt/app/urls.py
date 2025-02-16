from django.urls import path
from . import views


urlpatterns=[
    path('',views.user_home),
    path('home',views.home),


    path('verify_otp',views.verify_otp),
    path('resend',views.resend_otp),
    path('forget',views.forgetpassword),
    path('reset',views.resetpassword),
    path('verify_otp_reg',views.verify_otp_reg),
    path('resend_otp_reg',views.resend_otp_reg ),
    path('change_pswd',views.change_pswd),



    path('admin_home',views.admin_home),
    path('admin_viewpic/<pid>',views.admin_viewpic),
    path('admin_delete_img/<pid>',views.admin_delete_img),
    path('a_logout',views.a_logout),
    path('login',views.u_login),
    path('reg',views.reg),
    path('user_prfl',views.user_prfl),
    path('viewall',views.viewall),
    path('viewpic/<pid>',views.viewpic),
    path('add_image',views.add_image),
    path('delete_img/<pid>',views.delete_img),
    # path('your_upld',views.your_upld),
    path('all_uplds',views.all_uplds),
    path('u_logout',views.u_logout),
    path('download/<pid>',views.download),
    path('edit_prfl',views.edit_prfl),
    path('images_by_category/<pid>',views.images_by_category),
    path('search',views.search),
    path('user_pic/<pid>',views.user_pic),
    

]