from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from .models import *
import os
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.

# def login(req):
#     if 'admin' in req.session:
#         return redirect(admin_home)
#     if 'user' in req.session:
#         return redirect(user_prfl)
#     if req.method=='POST':
#         uname=req.POST['username']
#         password=req.POST['password']
#         data=authenticate(username=uname,password=password)
#         if data:
#             if data.is_superuser:
#                 login(req,data)
#                 req.session['admin']=uname
#                 return redirect(admin_home)
#             else:
#                 login(req,data)
#                 req.session['user']=uname
#                 return redirect(user_home)
#     else:
#         return render(req,'login.html')
    
def u_login(req):
    if 'admin' in req.session:
        return redirect(admin_home)
    if 'user' in req.session:
        return redirect(user_prfl)
    if req.method=='POST':
        uname=req.POST['username']
        password=req.POST['password']
        data=authenticate(username=uname,password=password)
        if data:
            if data.is_superuser:
                login(req,data)
                req.session['admin']=uname
                return redirect(admin_home)
            else:
                login(req,data)
                req.session['user']=uname
                return redirect(user_home)
        else:
            messages.warning(req,"Invalid uname or password")
            return redirect(u_login)
    else:
        return render(req,'login.html')
    

def reg(req):
        if req.method=='POST':
            name=req.POST['name']
            email=req.POST['email']
            password=req.POST['password']
            try:
                # send_mail('user registration', 'account created', settings.EMAIL_HOST_USER, [email])
                data=User.objects.create_user(first_name=name,email=email,password=password,username=email)
                data.save()
                return redirect(login)
            except:
                # messages.warning(req,"Email not valid")
                return redirect(reg)
        else:
            return render(req,'user/register.html')
# ----------------------------admin-------------------    
    
def admin_home(req):
    return render(req,'admin_home.html')

# ----------------------------user-------------------
def user_prfl(req):
    data=Images.objects.all()
    return render(req,'user/user_prfl.html',{'data':data})

def user_home(req):
    data=Images.objects.all()[::-1]

    return render(req,'user/user_home.html',{'data':data})

def viewall(req):
    data=Images.objects.all()
    return render(req,'user/viewall.html',{'data':data})


def viewpic(req,pid):
    data=Images.objects.get(pk=pid)
    category_name = data.tag  # This could be dynamic, like from request.GET or URL parameters
    images = Images.objects.filter(tag__name=category_name).exclude(pk=pid)
    return render(req,'user/viewpic.html',{'data':data,'images': images})





def add_image(req):
    if req.method == 'POST':
        title = req.POST['title']
        disp = req.POST['disp']
        tags = req.POST['tags'] 
        img = req.FILES.get('img') 
        
       
        tag_names = [tag.strip() for tag in tags.split(',')]
        
      
        categories = []
        for tag_name in tag_names:
            category, created = Category.objects.get_or_create(name=tag_name)
            categories.append(category)

        image = Images.objects.create(title=title, disp=disp, tags=tags, img=img,tag=categories[0])
        
        return redirect(user_home)  

    return render(req, 'user/add_image.html')



    