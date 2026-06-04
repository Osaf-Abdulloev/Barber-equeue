from django import forms
from .models import *




class UserForm(forms.Form):
    username = forms.CharField(
        label = 'Username',

        
        )
    
    email = forms.EmailField(
        label='Email',
        
        
    )
    
    p1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput
    )
    
    p2 = forms.CharField(
        label='Try again password',
        widget=forms.PasswordInput

    )
    
    is_barber = forms.BooleanField(
        label='I`m barber',
        required=False
    )


class LoginForm(forms.Form):
    username = forms.CharField(
        label='username'
    )
    
    password = forms.CharField(
        label='password'
    )


class EmailConfirmForm(forms.Form):
    username = forms.CharField(
        label='username'
    )
    
    code = forms.CharField(
        label='code from gmail'
    )
    

class BarberProfileForm(forms.Form):
    bio = forms.CharField(
        widget=forms.Textarea,
        label='Bio'
    )
    
    stajikori = forms.IntegerField(
        min_value=0,
        max_value=100,
        label='Staji kori'
    )
    
    phone = forms.CharField(
        label='Phone number',
        max_length=13
    )
    
    age = forms.IntegerField(
        max_value=100,
        min_value=14
    )
    
    location = forms.CharField(
        label='Location'
    )
    
    img = forms.ImageField(
        label="Image (optional)",
        required=False
    )


class UserProfileForm(forms.Form):
    bio = forms.CharField(
        widget=forms.Textarea,
        label='Bio'
    )
    
    phone = forms.CharField(
        label='Phone number',
        max_length=13
    )
    
    adress = forms.CharField(
        label='adress'
    )
    
    age = forms.IntegerField(
        max_value=100,
        min_value=14
    )
    
    
    img = forms.ImageField(
        label="Image (optional)",
        required=False
        
    )


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(label='Email')


class ResetPasswordForm(forms.Form):
    code = forms.CharField(label='Code from email')
    new_password = forms.CharField(widget=forms.PasswordInput, label='New password')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirm password')


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput, label='Old password')
    new_password = forms.CharField(widget=forms.PasswordInput, label='New password')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirm password')

