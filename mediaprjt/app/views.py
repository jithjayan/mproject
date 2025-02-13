from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from .models import *
# Create your views here.

def login(req):

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
        return render(req,'login.html')
    


# ----------------------------admin-------------------    
    
def admin_home(req):
    return render(req,'admin_home.html')

# ----------------------------user-------------------
def user_home(req):
    data=Images.objects.all()[::-1]
    return render(req,'user/user_home.html',{'data':data})

def viewall(req):
    data=Images.objects.all()
    return render(req,'user/viewall.html',{'data':data})

