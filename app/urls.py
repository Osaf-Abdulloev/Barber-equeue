from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('book/<int:barber_id>/', views.book_appointment, name='book_appointment'),
    path('my_appointments/', views.my_appointments, name='my_appointments'),
    path('barber_appointments/', views.barber_appointments, name='barber_appointments'),
    path('add_service/', views.add_service, name='add_service'),
    path('add_busy_time/', views.add_busy_time, name='add_busy_time'),
    path('add_work/', views.add_work, name='add_work'),
    path('like/<int:work_id>/', views.like_work, name='like_work'),
    path('comment/<int:work_id>/', views.add_comment, name='add_comment'),
    path('favorite/<int:barber_id>/', views.add_favorite, name='add_favorite'),
    path('my_favorites/', views.my_favorites, name='my_favorites'),
    path('chat/<int:barber_id>/', views.chat_room, name='chat_room'),
    path('send_message/', views.send_message, name='send_message'),
    path('notifications/', views.notifications, name='notifications'),
    path('barber/<int:barber_id>/', views.barber_profile_detail, name='barber_profile_detail'),
    path('ai_consultant/', views.ai_consultant, name='ai_consultant'),
]








