from django.db import models

# Create your models here.

class Category(models.Model):

    name=models.TextField()
    def __str__(self):
        return self.name


class Images(models.Model):
    img=models.FileField()
    title=models.TextField()
    tags=models.TextField()
    disp=models.TextField()
    date=models.DateTimeField(auto_now_add=True)
    # tag = models.ManyToManyField(Category, related_name='images')
    tag=models.ForeignKey(Category,on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    

    