from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Appointment, Notification


@receiver(post_save, sender=Appointment)
def send_appointment_email(sender, instance, created, **kwargs):
    if created:
        subject = 'New Appointment Booking'
        message = f'Hello {instance.user.username},\n\nYou have booked an appointment with {instance.barber.user.username} on {instance.date} at {instance.time}.\n\nService: {instance.service.name}\n\nThank you!'
        
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [instance.user.email],
                fail_silently=False,
            )
        except:
            pass
        
        # Create notification for barber
        Notification.objects.create(
            user=instance.barber.user,
            barber=instance.barber,
            message=f'New appointment from {instance.user.username} on {instance.date} at {instance.time}'
        )
