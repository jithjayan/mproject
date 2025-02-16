from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from .models import *
import os
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
import mimetypes
from django.utils.crypto import get_random_string

# Create your views here.
    
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
            if User.objects.filter(email=email).exists():
                messages.warning(req, "Email already registered")
                return redirect(reg)
            otp = get_random_string(length=6, allowed_chars='0123456789')
            req.session['otp'] = otp
            req.session['email'] = email
            req.session['name'] = name
            req.session['password'] = password
            send_mail(
                'Your OTP Code',
                f'Your OTP is: {otp}',
                settings.EMAIL_HOST_USER, [email])
            messages.success(req, "OTP sent to your email")
            return redirect(verify_otp_reg)

    
        return render(req,'user/register.html')
        
def verify_otp_reg(req):
    if req.method == 'POST':
        entered_otp = req.POST['otp'] 
        stored_otp = req.session.get('otp')
        email = req.session.get('email')
        name = req.session.get('name')
        password = req.session.get('password')
        if entered_otp == stored_otp:
            user = User.objects.create_user(first_name=name,username=email,email=email,password=password)
            user.is_verified = True
            user.save()      
            messages.success(req, "Registration successful! You can now log in.")
            send_mail('User Registration Succesfull', 'Account Created Succesfully And Welcome To Photox', settings.EMAIL_HOST_USER, [email])
            return redirect(u_login)
        else:
            messages.warning(req, "Invalid OTP. Try again.")
            return redirect(verify_otp_reg)

    return render(req, 'verify_otp_reg.html')

def resend_otp_reg(req):
    email = req.session.get('email')
    if email:
        otp = get_random_string(length=6, allowed_chars='0123456789')
        req.session['otp'] = otp
        
        send_mail(
            'Your New OTP Code',
            f'Your OTP is: {otp}',
            settings.EMAIL_HOST_USER, [email]
        )
        messages.success(req, "OTP resent to your email")
    
    return redirect(verify_otp_reg)


def forgetpassword(req):
    if req.method == 'POST':
        email = req.POST['email']
        try:
            user = User.objects.get(email=email)
            otp = get_random_string(length=6, allowed_chars='0123456789')
            req.session['otp'] = otp
            req.session['email'] = email
            send_mail('Password Reset OTP', f'Your OTP is: {otp}', settings.EMAIL_HOST_USER, [email])
            messages.success(req, "OTP sent to your email")
            return redirect(verify_otp)
        except User.DoesNotExist:
            messages.warning(req, "Email not found")
            return redirect(forgetpassword)
    return render(req,'forgetpassword.html')


def verify_otp(req):
    if req.method == 'POST':
        otp = req.POST['otp']
        if otp == req.session.get('otp'):
            return redirect(resetpassword)
        else:
            messages.warning(req, "Invalid OTP")
            return redirect(verify_otp)
    return render(req, 'verify_otp.html')

def resend_otp(req):  
    email = req.session.get('email')
    if email:
        otp = get_random_string(length=6, allowed_chars='0123456789')
        req.session['otp'] = otp
        send_mail('Password Reset OTP', f'Your OTP is: {otp}', settings.EMAIL_HOST_USER, [email])
        messages.success(req, "OTP resent to your email")
    return redirect(verify_otp)

def resetpassword(req):
    if req.method == 'POST':
        password = req.POST['password']  
        email = req.session.get('email')
        try:
            user = User.objects.get(email=email)
            user.set_password(password)
            user.save()
            messages.success(req, "Password reset successfully")
            return redirect(u_login)
        except User.DoesNotExist:
            messages.warning(req, "Error resetting password")
            return redirect(resetpassword)
    return render(req, 'resetpassword.html')



def change_pswd(req):
    if 'user' in req.session:
        if req.method=='POST':
            user=User.objects.get(username=req.session['user'])
            old_password = req.POST['old_password']
            new_password = req.POST['new_password']
            if user.check_password(old_password):
                user.set_password(new_password)
                user.save()
                messages.success(req,"Password changed successfully")
                return redirect(change_pswd)
            else:
                messages.warning(req,"Old password is incorrect")
                return redirect(change_pswd)
        else:
            return render(req,'user/change_pswd.html')
    else:
        return redirect(u_login)




def home(req):
    return redirect(user_home)
# ----------------------------admin-------------------    
    
def admin_home(req):
    if 'admin' in req.session:
        data=Images.objects.all()[::-1]
        return render(req,'admin/admin_home.html',{'data':data})
    return render(req,'admin_home.html')

def admin_viewpic(req,pid):
    data=Images.objects.get(pk=pid)
    data2=data.user
    data3=Profile.objects.filter(user=data.user).first()
    return render(req,'admin/admin_viewpic.html',{'data':data,'data2':data2,'data3':data3})
def admin_delete_img(req,pid):
    if 'admin' in req.session:
        image=Images.objects.get(pk=pid)
        url=image.img.url
        og_path=url.split('/')[-1]
        os.remove('media/'+og_path)
        image.delete()
        print(og_path)
        return redirect(admin_home)
    else:
        return redirect(u_login)
    
def a_logout(req):
    req.session.flush()
    logout(req)
    return redirect(user_home) 
# ----------------------------user-------------------
def user_home(req):
    data=Images.objects.all()[::-1]

    return render(req,'user/user_home.html',{'data':data})

def user_prfl(req):
    if 'user' in req.session:
        user=User.objects.get(username=req.session['user'])

        if Profile.objects.filter(user=user).exists():
            uploads=Your_uplds.objects.filter(user=user)[::-1]
            profile=Profile.objects.get(user=user)
            return render(req,'user/user_prfl.html',{'uploads':uploads,'profile':profile})
        else:
            user=User.objects.get(username=req.session['user'])
            uploads=Your_uplds.objects.filter(user=user)[::-1]
            return render(req,'user/user_prfl.html',{'uploads':uploads})        
        # profile=Profile.objects.get(user=user)


    
def u_logout(req):
    req.session.flush()
    logout(req)
    return redirect(user_home)    

# def your_upld(req):
#         if 'user' in req.session:
#             user=User.objects.get(username=req.session['user'])
#             uploads=Your_uplds.objects.filter(user=user)
#             return render(req,'user/cart.html',{'uploads':uploads})
    

def viewall(req):
    data=Images.objects.all()
    return render(req,'user/viewall.html',{'data':data})


def viewpic(req,pid):
    data=Images.objects.get(pk=pid)
    data2=data.user
    data3=Profile.objects.filter(user=data.user).first()
    category_name = data.tag  # This could be dynamic, like from request.GET or URL parameters
    images = Images.objects.filter(tag__name=category_name).exclude(pk=pid)
    return render(req,'user/viewpic.html',{'data':data,'images': images,'data2':data2,'data3':data3})


def images_by_category(req,pid):
    category = Category.objects.get(pk=pid)
    images = Images.objects.filter(tag=category)
    return render(req, 'user/images_by_category.html', {'category': category, 'images': images})


def add_image(req):
    if 'user' in req.session:
        user=User.objects.get(username=req.session['user'])

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

            image = Images.objects.create(user=user,title=title, disp=disp, tags=tags, img=img,tag=categories[0])
            image.save()

            Your_uplds.objects.create(user=user, Images=image)

            return redirect(user_home)  

        return render(req, 'user/add_image.html')
    else:
        return redirect(u_login)



def delete_img(req,pid):
    if 'user' in req.session:
        image=Images.objects.get(pk=pid)
        url=image.img.url
        og_path=url.split('/')[-1]
        os.remove('media/'+og_path)
        image.delete()
        print(og_path)
        return redirect(all_uplds)
    else:
        return redirect(u_login)

def all_uplds(req):
    if 'user' in req.session:
        user=User.objects.get(username=req.session['user'])
        uploads=Your_uplds.objects.filter(user=user)[::-1]
        return render(req,'user/all_uplds.html',{'uploads':uploads})
    else:
        return redirect(u_login)

def user_pic(req,pid):
    data=Images.objects.get(pk=pid)
    return render(req,'user/user_pic.html',{'data':data})

def download(req, pid):
    image = Images.objects.get(pk=pid)  

    image_path = image.img.path
    if os.path.exists(image_path):
        mime_type, _ = mimetypes.guess_type(image_path)
        if not mime_type:
            mime_type = 'application/octet-stream'
        
        with open(image_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type=mime_type)
            response['Content-Disposition'] = f'attachment; filename="{image.img.name}"' 
            return response
    else:
        return HttpResponse("Image not found.", status=404)


def edit_prfl(req):
    if 'user' in req.session:
        user = User.objects.get(username=req.session['user'])
        profile, created = Profile.objects.get_or_create(user=user)
        
        if req.method == 'POST':
            first_name = req.POST['first_name']
            bio = req.POST['bio']
            profile_picture = req.FILES.get('profile_picture')  

            User.objects.filter(username=req.session['user']).update(first_name=first_name)

            profile.bio = bio  
            if profile_picture:  
                profile.profile_picture = profile_picture
            profile.save()  

            return redirect(edit_prfl)  

        return render(req, 'user/edit_prfl.html', {'profile': profile})
    else:
        return redirect(u_login)




def search(req):
    query = req.GET.get('query', '').strip()  
    if query:
        images = Images.objects.filter( Q(title__icontains=query)|Q(tags__icontains=query))
    else:
        images = [] 
    return render(req, 'user/search.html', {'images': images})