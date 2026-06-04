from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('emailconfirm/', views.emailconfirm, name='emailconfirm'),
    path('barber_profile/', views.barber_profile, name='barber_profile'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('my_profile/<int:pk>', views.my_profile, name='my_profile'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('change_password/', views.change_password, name='change_password'),
]

