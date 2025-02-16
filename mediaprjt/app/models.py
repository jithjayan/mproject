from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):

    name=models.TextField()
    def __str__(self):
        return self.name


class Images(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    img=models.FileField()
    title=models.TextField()
    tags=models.TextField()
    disp=models.TextField()
    date=models.DateTimeField(auto_now_add=True)
    # tag = models.ManyToManyField(Category, related_name='images')
    tag=models.ForeignKey(Category,on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
class Your_uplds(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    Images=models.ForeignKey(Images,on_delete=models.CASCADE)


class Profile(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    bio=models.TextField()
    profile_picture=models.FileField()





