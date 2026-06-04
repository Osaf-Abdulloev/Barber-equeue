from django import forms
from .models import Service, Appointment, BusyTime, Work
from accounts.models import BarberProfile


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'price', 'duration', 'description']


class AppointmentForm(forms.Form):
    service = forms.ModelChoiceField(queryset=Service.objects.all(), label='Service')
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))


class BusyTimeForm(forms.ModelForm):
    class Meta:
        model = BusyTime
        fields = ['date', 'start_time', 'end_time']


class WorkForm(forms.ModelForm):
    class Meta:
        model = Work
        fields = ['image', 'description']
