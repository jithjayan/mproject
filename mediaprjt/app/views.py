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


def viewpic(req,pid):
    data=Images.objects.get(pk=pid)
    data2=data.split(',')
    m=[]
    m.append(data2)
    data3=Images.objects.filter(tags__in=data2).exclude(pk=pid)
    data4=Category.objects.all()
    return render(req,'user/viewpic.html',{'data':data,'data2':data2,'data3':data3,'data4':data4})



# def viewpic(req,pid):
    # dt=[]
    # data=Images.objects.get(pk=pid)
    # tgs=Images.objects.get(pk=pid).tags
    # tgs=tgs.split(',')
    # for i in tgs:
    #     if i not in Category.objects.all():
    #         Category.objects.create(tag=Images.objects.get(pk=pid),name=i)
    #     else:
    #         pass    

    # dt.append(tgs)
    # data1=Category.objects.filter()
    # print(dt)
    # print()
    # return render(req,'user/viewpic.html',{'data':data,'data1':data1})

# def add_image(req):
#     if req.method=='POST':
#         title=req.POST['title']
#         disp=req.POST['disp']
#         tags=req.POST['tags']
#         img=req.FILES['img']
#         catg=[]
#         for i in tags.split(','):
#             i=i.strip()
#             catg.append(i)
#             print(catg)
#             if i not in Category.objects.all():
#                g= Category.objects.get_or_create(name=i)

#             else:
#                 pass
#             data=Images.objects.create(title=title,disp=disp,tags=tags,img=img)
#             data.save()
#         return redirect(user_home)
#     return render(req,'user/add_image.html')




# def add_image(req):
#     if req.method == 'POST':
#         title = req.POST['title']
#         disp = req.POST['disp']
#         tags = req.POST['tags'] 
#         img = req.FILES.get('img') 
#         dt=[]
        
#         for i in tags.split(','):
#             i=i.strip()
#             dt.append(i)
#             for j in dt:
#                 if j not in Category.objects.filter(name=j):
#                     Category.objects.create(name=j)
#                 else:
#                     pass
#                 data=Images.objects.create(title=title,disp=disp,tags=tags,img=img,tag=j)
#                 data.save()
#         return redirect(user_home)
    
#     return render(req,'user/add_image.html')

def add_image(req):
    if req.method == 'POST':
        title = req.POST['title']
        disp = req.POST['disp']
        tags = req.POST['tags'] 
        img = req.FILES.get('img') 
        
        # Step 1: Process tags
        tag_names = [tag.strip() for tag in tags.split(',')]
        
        # Step 2: Create or get existing Category instances
        categories = []
        for tag_name in tag_names:
            category, created = Category.objects.get_or_create(name=tag_name)
            categories.append(category)

        # Step 3: Create the image object with the first category
        image = Images.objects.create(title=title, disp=disp, tags=tags, img=img,tag=categories[0])
        
        # image.tag.set([tag])
        
        # Step 4: Optionally, you can add more tags to the image (many-to-many relationship).
        # In your model, if you want `Images` to have multiple categories (tags), you'd need a `ManyToManyField`.
        
        # Step 5: Redirect after saving
        return redirect(user_home)  # Assuming `user_home` is your URL name

    return render(req, 'user/add_image.html')


def demo(req):
    category_name = 'xx'  # This could be dynamic, like from request.GET or URL parameters
    images = Images.objects.filter(tag__name=category_name)
    return render(req, 'user/demoq.html', {'images': images})
    