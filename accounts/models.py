from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.



class User(AbstractUser):
    is_barber = models.BooleanField(default = False)
    is_created = models.BooleanField(default=False)


class EmailConfirm(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    



class BarberProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='aaa')
    bio = models.TextField(null=True, blank=True)
    stajikori = models.PositiveIntegerField()
    phone = models.CharField(max_length=13, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    location = models.CharField(max_length=50)
    img = models.ImageField(upload_to='barbers/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    in_work = models.BooleanField(default=False)
    
    
    


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bbb')
    bio = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=13)
    adress = models.CharField(max_length=35)
    age = models.IntegerField()
    img = models.ImageField(upload_to='barbers/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class PasswordReset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.code}"
