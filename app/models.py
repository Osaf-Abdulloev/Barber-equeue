from django.db import models
from accounts.models import User, BarberProfile
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

# Create your models here.


class Service(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.IntegerField(help_text='Duration in minutes')
    description = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.name


class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    barber = models.ForeignKey(BarberProfile, on_delete=models.CASCADE, related_name='appointments')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, default='pending', choices=[
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['barber', 'date', 'time']
    
    def __str__(self):
        return f"{self.user.username} - {self.barber.user.username} - {self.date} {self.time}"


class ChatRoom(models.Model):
    name = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_rooms')
    barber = models.ForeignKey(BarberProfile, on_delete=models.CASCADE, related_name='chat_rooms')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name


class ChatMessage(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='chat_images/', null=True, blank=True)
    voice = models.FileField(upload_to='chat_voice/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.sender.username} - {self.room.name}"


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    barber = models.ForeignKey(BarberProfile, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'barber']
    
    def __str__(self):
        return f"{self.user.username} - {self.barber.user.username}"


class BusyTime(models.Model):
    barber = models.ForeignKey(BarberProfile, on_delete=models.CASCADE, related_name='busy_times')
    start_time = models.TimeField()
    end_time = models.TimeField()
    date = models.DateField()
    
    def __str__(self):
        return f"{self.barber.user.username} - {self.date} {self.start_time}-{self.end_time}"


class Work(models.Model):
    barber = models.ForeignKey(BarberProfile, on_delete=models.CASCADE, related_name='works')
    image = models.ImageField(upload_to='works/')
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Work by {self.barber.user.username}"


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    work = models.ForeignKey(Work, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'work']
    
    def __str__(self):
        return f"{self.user.username} - {self.work.id}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    work = models.ForeignKey(Work, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.work.id}"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    barber = models.ForeignKey(BarberProfile, on_delete=models.CASCADE, related_name='notifications', null=True, blank=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.message[:20]}"
