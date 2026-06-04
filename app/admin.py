from django.contrib import admin
from .models import *



admin.site.register(Service)
admin.site.register(Appointment)
admin.site.register(ChatRoom)
admin.site.register(ChatMessage)
admin.site.register(Favorite)
admin.site.register(BusyTime)
admin.site.register(Work)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Notification)

# Register your models here.
