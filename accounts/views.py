from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import Group
from .models import *
from .forms import *
import random
from django.conf import settings
from django.core.mail import EmailMultiAlternatives

# Create your views here.



def sendcode(user):
    
    code = random.randint(100000, 999999)
    
    EmailConfirm.objects.create(user_id = user.id, code = code) 
    
    try:
        subject = 'Confirm Your Password | Abdullo barber'

        from_email = settings.DEFAULT_FROM_EMAIL
        
        to = [user.email]
        
        
        text_content = f'''
        Hello {user.username}
        
        Your confirmation code is: {code}
        '''
        
        
        html_content = f'''
        <div style="
            font-family: Arial;
            max-width: 600px;
            margin: auto;
            padding: 30px;
            background: #f4f4f4;
        ">
        
            <div style="
                background: white;
                padding: 30px;
                border-radius: 12px;
            ">
        
                <h1 style="color:#2563eb;">
                    JobFinder
                </h1>
        
                <h2>
                    Password Confirmation
                </h2>
        
                <p>
                    Hello <b>{user.username}</b>,
                </p>
        
                <p>
                    Use the confirmation code below:
                </p>
        
                <div style="
                    font-size: 32px;
                    font-weight: bold;
                    letter-spacing: 5px;
                    background:#eff6ff;
                    padding:20px;
                    border-radius:10px;
                    text-align:center;
                    color:#2563eb;
                ">
                    {code}
                </div>
        
                <p style="margin-top:25px;">
                    If you did not request this email,
                    you can safely ignore it.
                </p>
        
                <hr>
        
                <p style="color:gray;">
                    © JobFinder Team
                </p>
        
            </div>
        </div>
        '''
        
        
        msg = EmailMultiAlternatives(
            subject,
            text_content,
            from_email,
            to
        )
        
        msg.attach_alternative(html_content, "text/html")
        
        msg.send()
    except Exception as e:
         print(e, '============================================================================================================')


def register(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        
        if form.is_valid():
            if form.cleaned_data['p1'] != form.cleaned_data['p2']:
                return render(request, 'error.html', context={'error' : 'Passwords not equal!'})
            
            if User.objects.filter(username = form.cleaned_data['username']).exists():
                return render(request, 'error.html', context={'error' : 'Username already exists'})
            
            if User.objects.filter(email = form.cleaned_data['email']).exists():
                return render(request, 'error.html', context={'error' : 'email already exists'})
            
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['p1'],
                email=form.cleaned_data['email'],
            )
            
            user.is_barber = form.cleaned_data['is_barber']
            
            if user.is_barber:
                group = Group.objects.get(name = "barber")
                user.groups.add(group)
            else:
                group = Group.objects.get(name = "user")
                user.groups.add(group)
            
            user.is_active = False
            user.save()
            
            sendcode(user)
            
            return redirect('emailconfirm')
        
        return render(request, 'error.html', context={'error' : 'Invalid datas'})
    
    else:
        form = UserForm()
        return render(request, 'acc/register.html', context={'form' : form})
            
   
def login_user(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        
        if form.is_valid():
            
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            if User.objects.filter(username = username, is_active = False):
                return render(request, 'error.html', context={'error': 'Please confirm your email'})
            
            user = authenticate(request, username = username, password = password)
            
            if not user:
                return render(request, 'error.html', context={'error' : 'invalid username or password'})
            
            
            login(request, user)
            
            userr = User.objects.filter(username = user.username, is_created = True).first()
            
            if userr:
                return redirect('/')
            
            print(userr)
            
            if request.user.groups.filter(name = 'barber'):
                return redirect('barber_profile')
            
            if request.user.groups.filter(name = 'user'):
                return redirect('user_profile')
                
            
            return redirect('/')
        
        return render(request, 'error.html', context={'error' : 'Wrong datas'})
    
    else:
        form = LoginForm()
        return render(request, 'acc/login.html', context={'form' : form})


def emailconfirm(request):
    if request.method == "POST":
        form = EmailConfirmForm(request.POST)
        
        if form.is_valid():
            
            user = User.objects.filter(username = form.cleaned_data['username']).first()
            
            if not user:
                return render(request, 'error.html', context={'error' : 'Wrong username'})
            
            ccode = EmailConfirm.objects.get(user = user, code = form.cleaned_data['code'])
            
            if not ccode:
                return render(request, 'error.html', context={'error' : 'Incorrect code from gmail'})
            
            user.is_active = True
            user.save()
            ccode.delete()
            
            return redirect('login')
        
        return render(request, 'error.html', context={'error' : 'Wrong datas'})
    
    else:
        form = EmailConfirmForm()
        return render(request, 'acc/emailconfirm.html', context={'form' : form})


def barber_profile(request):
    if request.method == "POST":
        form = BarberProfileForm(request.POST, request.FILES)
        
        if form.is_valid():
            
            BarberProfile.objects.create(
                user = request.user,
                bio = form.cleaned_data['bio'],
                stajikori = form.cleaned_data['stajikori'],
                phone = form.cleaned_data['phone'],
                age = form.cleaned_data['age'],
                location = form.cleaned_data['location'],
                img = form.cleaned_data['img']
            )
            
            user = User.objects.get(username = request.user.username)
            user.is_created = True
            user.is_active = True
            user.save()
            
            
            return redirect('/')
        return render(request, 'error.html', context={'error' : 'Wrong datas'})
    
    else:
        form = BarberProfileForm()
        return render(request, 'acc/barber_profile_form.html', context={'form' : form})
            
    
def user_profile(request):
    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES)
        
        if form.is_valid():
            UserProfile.objects.create(
                user = request.user,
                bio = form.cleaned_data['bio'],
                phone = form.cleaned_data['phone'],
                adress = form.cleaned_data['adress'],
                age = form.cleaned_data['age'],
                img = form.cleaned_data['img'],
            )
            
            user = User.objects.get(username = request.user.username)
            user.is_created = True
            user.is_active = True
            user.save()
            
            return redirect('/')
        
        return render(request, 'error.html', context={'error' : 'Wrong datas'})

    else:
        form = UserProfileForm()
        return render(request, 'acc/user_profile_form.html', context={'form' : form})


def logout_user(request):
    logout(request)
    return redirect('/')


def my_profile(request, pk):
    
    user = get_object_or_404(User, pk=pk)
    
    is_user = UserProfile.objects.filter(user_id = user.id).select_related('user')
    is_barber = BarberProfile.objects.filter(user_id = user.id).select_related('user')
    
    if is_user:
        return render(request, 'acc/user_profile.html', context={'user' : is_user})
    
    if is_barber:
        return render(request, 'acc/barber_profile.html', context={'barber' : is_barber})
    
    return render(request, 'error.html', context={'error' : 'Profile not found'})


def forgot_password(request):
    if request.method == "POST":
        form = ForgotPasswordForm(request.POST)
        
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.filter(email = email).first()
            
            if not user:
                return render(request, 'error.html', context={'error' : 'Email not found'})
            
            code = random.randint(100000, 999999)
            
            PasswordReset.objects.create(user=user, code=code)
            
            try:
                subject = 'Password Reset Code'
                
                from_email = settings.DEFAULT_FROM_EMAIL
                to = [user.email]
                
                text_content = f'Hello {user.username},\n\nYour password reset code is: {code}'
                
                html_content = f'''
                <div style="font-family: Arial; max-width: 600px; margin: auto; padding: 30px; background: #f4f4f4;">
                    <div style="background: white; padding: 30px; border-radius: 12px;">
                        <h1 style="color:#2563eb;">Barber Booking</h1>
                        <h2>Password Reset</h2>
                        <p>Hello <b>{user.username}</b>,</p>
                        <p>Use the code below to reset your password:</p>
                        <div style="font-size: 32px; font-weight: bold; letter-spacing: 5px; background:#eff6ff; padding:20px; border-radius:10px; text-align:center; color:#2563eb;">
                            {code}
                        </div>
                        <p style="margin-top:25px;">If you did not request this, you can safely ignore it.</p>
                        <hr>
                        <p style="color:gray;">© Barber Booking Team</p>
                    </div>
                </div>
                '''
                
                msg = EmailMultiAlternatives(subject, text_content, from_email, to)
                msg.attach_alternative(html_content, "text/html")
                msg.send()
            except Exception as e:
                print(e)
            
            return redirect('reset_password')
        
        return render(request, 'error.html', context={'error' : 'Invalid data'})
    
    else:
        form = ForgotPasswordForm()
        return render(request, 'acc/forgot_password.html', context={'form' : form})


def reset_password(request):
    if request.method == "POST":
        form = ResetPasswordForm(request.POST)
        
        if form.is_valid():
            code = form.cleaned_data['code']
            new_password = form.cleaned_data['new_password']
            confirm_password = form.cleaned_data['confirm_password']
            
            if new_password != confirm_password:
                return render(request, 'error.html', context={'error' : 'Passwords do not match'})
            
            reset = PasswordReset.objects.filter(code=code).first()
            
            if not reset:
                return render(request, 'error.html', context={'error' : 'Invalid code'})
            
            user = reset.user
            user.set_password(new_password)
            user.save()
            reset.delete()
            
            return redirect('login')
        
        return render(request, 'error.html', context={'error' : 'Invalid data'})
    
    else:
        form = ResetPasswordForm()
        return render(request, 'acc/reset_password.html', context={'form' : form})

def change_password(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.method == "POST":
        form = ChangePasswordForm(request.POST)
        
        if form.is_valid():
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password']
            confirm_password = form.cleaned_data['confirm_password']
            
            if not request.user.check_password(old_password):
                return render(request, 'error.html', context={'error' : 'Old password is incorrect'})
            
            if new_password != confirm_password:
                return render(request, 'error.html', context={'error' : 'Passwords do not match'})
            
            request.user.set_password(new_password)
            request.user.save()
            
            return redirect('login')
        
        return render(request, 'error.html', context={'error' : 'Invalid data'})
    
    else:
        form = ChangePasswordForm()
        return render(request, 'acc/change_password.html', context={'form' : form})


