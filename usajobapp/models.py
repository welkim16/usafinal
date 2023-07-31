from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


# class Type(models.Model):
#     type = models.TextField(max_length=200)
class Images(models.Model):
    image = models.URLField(max_length=1000)
class Salary(models.Model):
    salary = models.TextField(max_length=200)


class Cities(models.Model):
     cities = models.TextField(max_length=200)

# class JbImage(models.Model):
#     job_images = models.URLField(max_length=1000)

class UsJobs(models.Model):
    Title = models.CharField(max_length=10000)
    Job_link =models.URLField(max_length=10000)
    campany = models.CharField(max_length=1000)
    Date_posted = models.DateField(max_length=100)
    images =models.ForeignKey(Images, related_name='job_images', on_delete=models.CASCADE)
    # location = models.CharField(max_length=1000)
    cities = models.ForeignKey(Cities, related_name='job_cities', on_delete=models.CASCADE)
    # job_type = models.ForeignKey(Type, related_name='job_types', on_delete=models.CASCADE)
    job_salary = models.ForeignKey(Salary, related_name='job_salaries', on_delete=models.CASCADE)
    # jb_images = models.ForeignKey(JbImage, related_name='images', on_delete=models.CASCADE)

class JobDetails(models.Model):
    job = models.ForeignKey(UsJobs, related_name='job_details', on_delete=models.CASCADE)
    details = models.CharField(max_length=20000)
    bold = models.BooleanField(default=False)


from .managers import CustomUserManager
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    username = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)

    # username=None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

