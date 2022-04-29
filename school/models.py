from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
import datetime
import os

# Create your models here.

def filepath(request, filename):
    old_filename = filename
    timeNow = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = "%s%s" % (timeNow, old_filename)
    return os.path.join('images/', filename)
class Schools_Name(models.Model):
    school_name = models.CharField(max_length=100)

    def __str__(self):
        return self.school_name

class Schools_Profiles(models.Model):
    school_name = models.CharField(max_length=100)
    school_image = models.ImageField(upload_to = filepath)
    
    def __str__(self):
          return self.school_name

class School_images(models.Model):
    schools_profile = models.ForeignKey(Schools_Profiles, on_delete=models.CASCADE, null=True)
    image_title = models.CharField(max_length=100)
    school_image = models.ImageField(upload_to = filepath)

    def __str__(self):
        return self.image_title

class Student_admission_image(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    school_name = models.ForeignKey(Schools_Name, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to = filepath, null=True)
    
class Student_admission(models.Model):
    stud_admis = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    description = models.TextField()
    stud_image = models.ImageField(upload_to= filepath)
    School_name = models.ForeignKey(Schools_Name, on_delete=models.CASCADE, null=True)
    student_class = models.CharField(max_length=50)

class School_class(models.Model):
    school_name = models.ForeignKey(Schools_Name, on_delete=models.CASCADE, null=True)
    classes = models.CharField(max_length=50)
    price = models.IntegerField()

class Student(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    student_image = models.ImageField(upload_to = filepath)
    student_class = models.ForeignKey(School_class, on_delete=models.CASCADE, null=True)
    school = models.ForeignKey(Schools_Name, null=True, on_delete=models.CASCADE)
    pay = models.BooleanField( default=False)
    
class School_page(models.Model):
    school_Profiles = models.ForeignKey(Schools_Profiles, on_delete=models.CASCADE)
    host = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    school_description = models.TextField(null=True)

class Accepted_Admission(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    school_name = models.ForeignKey(Schools_Name, on_delete=models.CASCADE, null=True)

class Refuse_Admission(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    school_name = models.ForeignKey(Schools_Name, on_delete=models.CASCADE, null=True)
  
